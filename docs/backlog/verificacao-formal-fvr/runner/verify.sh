#!/usr/bin/env bash
set -u
umask 077

if [[ ! -x /usr/bin/env ]]; then
    printf '%s\n' '{"runner_state":"RUNNER_INTERNAL_ERROR","reason":"/usr/bin/env unavailable"}' >&2
    exit 14
fi

/usr/bin/env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin LC_ALL=C LANG=C python3 - "$0" "$@" <<'PY_FVR_ENGINE'
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import decimal
import hashlib
import json
import os
import pathlib
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time
from typing import Any

EXIT_OK = 0
EXIT_PLAN_INVALID = 10
EXIT_CONTROL_INTEGRITY = 11
EXIT_POLICY = 12
EXIT_PACKAGE_INCOMPLETE = 13
EXIT_INTERNAL = 14

RUN_COMPLETED = "RUN_COMPLETED"
RUN_COMPLETED_FAILED = "RUN_COMPLETED_WITH_FAILED_ASSERTIONS"
PLAN_INVALID = "PLAN_INVALID"
CONTROL_FAILURE = "CONTROL_INTEGRITY_FAILURE"
POLICY_VIOLATION = "POLICY_VIOLATION"
PACKAGE_INCOMPLETE = "PACKAGE_INCOMPLETE"
RUNNER_INTERNAL_ERROR = "RUNNER_INTERNAL_ERROR"

HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
RUN_ID_RE = re.compile(r"^RUN-[A-Z0-9][A-Z0-9._-]{2,95}$")
ASSERTION_ID_RE = re.compile(r"^(?:AC|INV)-[0-9]{3}$")
CONTROLLED_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
TOOL_ALLOWLIST = {"npm", "npx", "node", "python", "python3", "pytest", "git", "devcontainer"}
DEVCONTAINER_TOOL_ALLOWLIST = TOOL_ALLOWLIST | {"claude"}
SAFE_TOOL_PREFIXES = (
    "/usr/bin/",
    "/usr/local/bin/",
    "/bin/",
    "/usr/sbin/",
    "/usr/local/sbin/",
    "/sbin/",
)
EXCLUDED_FINGERPRINT_PREFIX = ".ai-control/verification-package"


class FvrFailure(Exception):
    def __init__(self, state: str, exit_code: int, reason: str):
        super().__init__(reason)
        self.state = state
        self.exit_code = exit_code
        self.reason = reason


def fail(state: str, exit_code: int, reason: str) -> None:
    raise FvrFailure(state, exit_code, reason)


def emit_control_failure(state: str, reason: str) -> None:
    payload = {"runner_state": state, "reason": reason}
    sys.stderr.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
    sys.stderr.flush()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate object member: {key}")
        out[key] = value
    return out


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def load_json_bytes(path: pathlib.Path) -> Any:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError(f"invalid UTF-8 in {path}: {exc}") from exc
    return json.loads(
        text,
        object_pairs_hook=strict_pairs,
        parse_constant=reject_constant,
        parse_float=decimal.Decimal,
        parse_int=int,
    )


def decimal_default(value: Any) -> Any:
    if isinstance(value, decimal.Decimal):
        if value == value.to_integral_value():
            return int(value)
        return float(value)
    raise TypeError(type(value).__name__)


def json_dump_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            default=decimal_default,
        )
        + "\n"
    ).encode("utf-8")


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def now_rfc3339() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_hex64(name: str, value: str) -> None:
    if not HEX64_RE.fullmatch(value):
        fail(RUNNER_INTERNAL_ERROR, EXIT_INTERNAL, f"invalid {name}: expected 64 lowercase hex characters")


def ensure_under(root: pathlib.Path, candidate: pathlib.Path, *, require_exists: bool = False) -> pathlib.Path:
    try:
        resolved_root = root.resolve(strict=True)
        resolved_candidate = candidate.resolve(strict=require_exists)
    except OSError as exc:
        fail(POLICY_VIOLATION, EXIT_POLICY, f"path resolution failed: {candidate}: {exc}")
    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError:
        fail(POLICY_VIOLATION, EXIT_POLICY, f"path escapes workspace: {candidate}")
    return resolved_candidate


def resolve_workspace_path(workspace: pathlib.Path, relative: str, *, require_exists: bool = False) -> pathlib.Path:
    if relative.startswith("/") or "\x00" in relative:
        fail(POLICY_VIOLATION, EXIT_POLICY, f"invalid workspace-relative path: {relative!r}")
    pieces = pathlib.PurePosixPath(relative).parts
    if ".." in pieces:
        fail(POLICY_VIOLATION, EXIT_POLICY, f"parent traversal forbidden: {relative!r}")
    return ensure_under(workspace, workspace / relative, require_exists=require_exists)


def resolve_artifact_path(tmp_run: pathlib.Path, relative: str) -> pathlib.Path:
    if not (relative.startswith("raw/") or relative.startswith("observations/")):
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, f"invalid artifact root: {relative}")
    target = tmp_run / pathlib.PurePosixPath(relative)
    resolved = target.resolve(strict=False)
    try:
        resolved.relative_to(tmp_run.resolve(strict=True))
    except ValueError:
        fail(POLICY_VIOLATION, EXIT_POLICY, f"artifact path escapes package: {relative}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def load_jsonschema_modules() -> tuple[Any, Any, Any, Any]:
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except Exception as exc:
        fail(RUNNER_INTERNAL_ERROR, EXIT_INTERNAL, f"required Python dependency unavailable: {exc}")
    return jsonschema, Draft202012Validator, Registry, Resource


def validate_plan_schema(plan: Any, schema_dir: pathlib.Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    jsonschema, Draft202012Validator, Registry, Resource = load_jsonschema_modules()
    try:
        assertion_schema = load_json_bytes(schema_dir / "assertion.schema.json")
        plan_schema = load_json_bytes(schema_dir / "verification-plan.schema.json")
        manifest_schema = load_json_bytes(schema_dir / "manifest.schema.json")
        Draft202012Validator.check_schema(assertion_schema)
        Draft202012Validator.check_schema(plan_schema)
        Draft202012Validator.check_schema(manifest_schema)
        registry = Registry().with_resources(
            [
                (assertion_schema["$id"], Resource.from_contents(assertion_schema)),
                (plan_schema["$id"], Resource.from_contents(plan_schema)),
                (manifest_schema["$id"], Resource.from_contents(manifest_schema)),
            ]
        )
        validator = Draft202012Validator(
            plan_schema,
            registry=registry,
            format_checker=jsonschema.FormatChecker(),
        )
        errors = sorted(validator.iter_errors(plan), key=lambda item: list(item.absolute_path))
    except FvrFailure:
        raise
    except Exception as exc:
        fail(RUNNER_INTERNAL_ERROR, EXIT_INTERNAL, f"schema initialization failed: {exc}")
    if errors:
        first = errors[0]
        location = "/" + "/".join(str(item) for item in first.absolute_path)
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, f"verification plan schema violation at {location}: {first.message}")
    return assertion_schema, plan_schema, manifest_schema


def contract_minimum(contract: Any) -> tuple[str, str, list[str]]:
    if not isinstance(contract, dict):
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, "contract must be a JSON object")
    metadata = contract.get("contract_metadata")
    if not isinstance(metadata, dict):
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, "contract.contract_metadata missing")
    contract_id = metadata.get("id")
    version = metadata.get("version")
    if not isinstance(contract_id, str) or not isinstance(version, str):
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, "contract id/version missing or not strings")
    ids: list[str] = []
    for collection_name in ("invariants", "acceptance_criteria"):
        collection = contract.get(collection_name, [])
        if not isinstance(collection, list):
            fail(PLAN_INVALID, EXIT_PLAN_INVALID, f"contract.{collection_name} must be an array")
        for item in collection:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                fail(PLAN_INVALID, EXIT_PLAN_INVALID, f"contract.{collection_name} item missing id")
            item_id = item["id"]
            if not ASSERTION_ID_RE.fullmatch(item_id):
                fail(PLAN_INVALID, EXIT_PLAN_INVALID, f"contract assertion id invalid: {item_id}")
            ids.append(item_id)
    if len(ids) != len(set(ids)):
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, "duplicate assertion id in contract")
    return contract_id, version, ids


def enforce_semantic_plan_rules(plan: dict[str, Any], contract: Any) -> None:
    contract_id, contract_version, contract_assertion_ids = contract_minimum(contract)
    metadata = plan["plan_metadata"]
    if metadata["contract_id"] != contract_id or metadata["contract_version"] != contract_version:
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, "plan contract id/version does not match frozen contract")
    assertion_ids = set(plan["assertions"].keys())
    if assertion_ids != set(contract_assertion_ids):
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, "plan assertion key set does not match frozen contract")
    policy = plan["policy"]
    steps = plan["steps"]
    if len(steps) > policy["max_steps"]:
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, "step count exceeds policy.max_steps")
    artifact_paths: list[str] = []
    for step in steps:
        timeout = step.get("timeout_seconds")
        if timeout is not None and timeout > policy["max_step_timeout_seconds"]:
            fail(PLAN_INVALID, EXIT_PLAN_INVALID, "step timeout exceeds policy.max_step_timeout_seconds")
        for field in ("stdout_artifact", "stderr_artifact"):
            value = step.get(field)
            if value is not None:
                artifact_paths.append(value)
    if len(artifact_paths) != len(set(artifact_paths)):
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, "artifact paths must be pairwise unique")


def controlled_tool(tool: str, *, devcontainer_exec: bool = False) -> pathlib.Path:
    allowlist = DEVCONTAINER_TOOL_ALLOWLIST if devcontainer_exec else TOOL_ALLOWLIST
    if tool not in allowlist:
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, f"unsupported tool: {tool}")
    resolved = shutil.which(tool, path=CONTROLLED_PATH)
    if resolved is None:
        fail(RUNNER_INTERNAL_ERROR, EXIT_INTERNAL, f"approved tool unavailable: {tool}")
    path = pathlib.Path(resolved).resolve(strict=True)
    path_text = str(path)
    if not any(path_text.startswith(prefix) for prefix in SAFE_TOOL_PREFIXES):
        fail(POLICY_VIOLATION, EXIT_POLICY, f"tool resolved outside approved system prefixes: {path_text}")
    return path


def ensure_bwrap() -> pathlib.Path:
    resolved = shutil.which("bwrap", path=CONTROLLED_PATH)
    if resolved is None:
        fail(RUNNER_INTERNAL_ERROR, EXIT_INTERNAL, "bubblewrap (bwrap) unavailable; host fallback is forbidden")
    path = pathlib.Path(resolved).resolve(strict=True)
    st = path.stat()
    if st.st_mode & stat.S_ISUID:
        fail(POLICY_VIOLATION, EXIT_POLICY, "setuid bubblewrap is not accepted by this implementation profile")
    return path


def safe_system_mounts() -> list[pathlib.Path]:
    candidates = ["/usr", "/bin", "/sbin", "/lib", "/lib64", "/etc", "/opt"]
    mounts: list[pathlib.Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        path = pathlib.Path(candidate)
        if not path.exists():
            continue
        real = path.resolve(strict=True)
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        mounts.append(path)
    return mounts


def copy_workspace(workspace: pathlib.Path, destination: pathlib.Path) -> None:
    def ignore(directory: str, names: list[str]) -> set[str]:
        rel = pathlib.Path(directory).resolve(strict=True).relative_to(workspace)
        if rel == pathlib.Path(".ai-control") and "verification-package" in names:
            return {"verification-package"}
        return set()
    shutil.copytree(workspace, destination, symlinks=True, ignore=ignore, dirs_exist_ok=False)


@dataclasses.dataclass
class Capture:
    path: pathlib.Path
    max_bytes: int
    stored_bytes: int = 0
    total_bytes: int = 0
    truncated: bool = False
    thread: threading.Thread | None = None

    def start(self, stream: Any) -> None:
        def reader() -> None:
            with self.path.open("wb") as output:
                while True:
                    chunk = stream.read(65536)
                    if not chunk:
                        break
                    self.total_bytes += len(chunk)
                    remaining = self.max_bytes - self.stored_bytes
                    if remaining > 0:
                        kept = chunk[:remaining]
                        output.write(kept)
                        self.stored_bytes += len(kept)
                    if len(chunk) > max(remaining, 0):
                        self.truncated = True
                output.flush()
                os.fsync(output.fileno())
        self.thread = threading.Thread(target=reader, daemon=True)
        self.thread.start()

    def join(self) -> None:
        if self.thread is not None:
            self.thread.join()

    def metadata(self, relative: str, media_type: str = "text/plain") -> dict[str, Any]:
        return {
            "path": relative,
            "sha256": sha256_file(self.path),
            "bytes": self.path.stat().st_size,
            "truncated": self.truncated,
            "media_type": media_type,
        }


def terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    try:
        pgid = os.getpgid(process.pid)
    except ProcessLookupError:
        return
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=2)
        return
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        fail(RUNNER_INTERNAL_ERROR, EXIT_INTERNAL, "child process group survived SIGKILL")


def run_captured(
    argv: list[str],
    stdout_path: pathlib.Path,
    stderr_path: pathlib.Path,
    timeout_seconds: int,
    max_log_bytes: int,
    env: dict[str, str] | None = None,
) -> tuple[str, int | None, str, Capture, Capture]:
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    process = subprocess.Popen(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        start_new_session=True,
        close_fds=True,
    )
    if process.stdout is None or process.stderr is None:
        fail(RUNNER_INTERNAL_ERROR, EXIT_INTERNAL, "failed to create child telemetry pipes")
    out_cap = Capture(stdout_path, max_log_bytes)
    err_cap = Capture(stderr_path, max_log_bytes)
    out_cap.start(process.stdout)
    err_cap.start(process.stderr)
    timed_out = False
    try:
        child_rc = process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        terminate_process_group(process)
        child_rc = None
    finally:
        out_cap.join()
        err_cap.join()
    if timed_out:
        return "TIMED_OUT", None, "TIMEOUT", out_cap, err_cap
    return "COMPLETED", child_rc, "EXITED", out_cap, err_cap


def sandbox_command(
    bwrap: pathlib.Path,
    workspace: pathlib.Path,
    workcopy: pathlib.Path,
    step: dict[str, Any],
    plan_env: dict[str, str],
) -> list[str]:
    tool = controlled_tool(step["tool"])
    relative_cwd = step["cwd"]
    resolve_workspace_path(workspace, relative_cwd, require_exists=True)
    work_cwd = (workcopy / relative_cwd).resolve(strict=True)
    try:
        work_cwd.relative_to(workcopy.resolve(strict=True))
    except ValueError:
        fail(POLICY_VIOLATION, EXIT_POLICY, f"sandbox cwd escapes working copy: {relative_cwd}")
    argv: list[str] = [
        str(bwrap),
        "--die-with-parent",
        "--new-session",
        "--unshare-user",
        "--unshare-ipc",
        "--unshare-pid",
        "--unshare-net",
        "--unshare-uts",
        "--clearenv",
        "--cap-drop",
        "ALL",
        "--uid",
        "65534",
        "--gid",
        "65534",
        "--dir",
        "/fvr",
        "--dir",
        "/fvr/source",
        "--dir",
        "/fvr/work",
        "--dir",
        "/tmp",
        "--dir",
        "/proc",
        "--dir",
        "/dev",
    ]
    for mount in safe_system_mounts():
        argv.extend(["--ro-bind", str(mount), str(mount)])
    argv.extend(["--remount-ro", "/"])
    argv.extend(["--ro-bind", str(workspace), "/fvr/source"])
    argv.extend(["--bind", str(workcopy), "/fvr/work"])
    argv.extend(["--tmpfs", "/tmp", "--proc", "/proc", "--dev", "/dev"])
    if step["network"] == "allow":
        argv.append("--share-net")
    sandbox_cwd = "/fvr/work"
    if relative_cwd not in ("", "."):
        sandbox_cwd = "/fvr/work/" + relative_cwd.strip("/")
    argv.extend(["--chdir", sandbox_cwd])
    argv.extend(["--setenv", "PATH", CONTROLLED_PATH])
    argv.extend(["--setenv", "HOME", "/tmp/fvr-home"])
    argv.extend(["--setenv", "TMPDIR", "/tmp"])
    for key in sorted(plan_env):
        argv.extend(["--setenv", key, plan_env[key]])
    argv.append(str(tool))
    argv.extend(step["argv"])
    return argv


def git_command(workspace: pathlib.Path, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    tool = controlled_tool("git")
    result = subprocess.run(
        [str(tool), "-C", str(workspace), *args],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={"PATH": CONTROLLED_PATH, "LC_ALL": "C", "LANG": "C"},
        check=False,
    )
    if check and result.returncode != 0:
        fail(RUNNER_INTERNAL_ERROR, EXIT_INTERNAL, f"git command failed: {args!r}: rc={result.returncode}")
    return result


def repository_head(workspace: pathlib.Path) -> str | None:
    result = git_command(workspace, ["rev-parse", "--verify", "HEAD"], check=False)
    if result.returncode != 0:
        return None
    value = result.stdout.decode("ascii", "strict").strip()
    if re.fullmatch(r"[0-9a-f]{40}", value):
        return value
    return None


def repository_initial_diff(workspace: pathlib.Path) -> str:
    if repository_head(workspace) is None:
        return ""
    result = git_command(workspace, ["diff", "--binary", "HEAD"], check=True)
    return result.stdout.decode("utf-8", "surrogateescape")


def workspace_fingerprint(workspace: pathlib.Path) -> str:
    digest = hashlib.sha256()
    head = repository_head(workspace)
    if head is not None:
        digest.update(b"FVR-GIT-WORKTREE-1\0")
        status = git_command(workspace, ["status", "--porcelain=v1", "-z", "--untracked-files=all"], check=True).stdout
        diff = git_command(workspace, ["diff", "--binary", "HEAD"], check=True).stdout
        digest.update(status)
        digest.update(b"\0DIFF\0")
        digest.update(diff)
        untracked = git_command(workspace, ["ls-files", "--others", "--exclude-standard", "-z"], check=True).stdout
        names = [item for item in untracked.split(b"\0") if item]
        for raw_name in sorted(names):
            name = raw_name.decode("utf-8", "surrogateescape")
            if name == EXCLUDED_FINGERPRINT_PREFIX or name.startswith(EXCLUDED_FINGERPRINT_PREFIX + "/"):
                continue
            path = resolve_workspace_path(workspace, name, require_exists=True)
            if path.is_symlink():
                target = os.readlink(path)
                digest.update(b"L\0" + raw_name + b"\0" + target.encode("utf-8", "surrogateescape") + b"\0")
            elif path.is_file():
                digest.update(b"F\0" + raw_name + b"\0")
                digest.update(bytes.fromhex(sha256_file(path)))
        return digest.hexdigest()
    digest.update(b"FVR-FILETREE-1\0")
    for path in sorted(workspace.rglob("*"), key=lambda item: item.as_posix()):
        rel = path.relative_to(workspace).as_posix()
        if rel == EXCLUDED_FINGERPRINT_PREFIX or rel.startswith(EXCLUDED_FINGERPRINT_PREFIX + "/"):
            continue
        if path.is_symlink():
            digest.update(b"L\0" + rel.encode() + b"\0" + os.readlink(path).encode() + b"\0")
        elif path.is_file():
            digest.update(b"F\0" + rel.encode() + b"\0")
            digest.update(bytes.fromhex(sha256_file(path)))
    return digest.hexdigest()


def manifest_artifact(relative: str, path: pathlib.Path, truncated: bool = False, media_type: str = "application/octet-stream") -> dict[str, Any]:
    return {
        "path": relative,
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "truncated": truncated,
        "media_type": media_type,
    }


def parse_structured_output(parser_type: str, stdout_path: pathlib.Path, truncated: bool) -> tuple[Any, str | None]:
    if parser_type == "none":
        return None, None
    if truncated:
        return None, "EVIDENCE_TRUNCATED"
    raw = stdout_path.read_bytes()
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError:
        return None, "PARSER_FAILURE"
    try:
        if parser_type == "json":
            value = json.loads(text, object_pairs_hook=strict_pairs, parse_constant=reject_constant)
            if not observation_shape_allowed(value):
                return None, "UNSUPPORTED_RUNTIME_VALUE"
            return value, None
        if parser_type == "jsonl":
            records: list[Any] = []
            for line in text.splitlines():
                if not line.strip():
                    continue
                value = json.loads(line, object_pairs_hook=strict_pairs, parse_constant=reject_constant)
                if not is_json_scalar(value):
                    return None, "UNSUPPORTED_RUNTIME_VALUE"
                records.append(value)
            return records, None
        if parser_type == "junit_xml":
            import xml.etree.ElementTree as ET
            root = ET.fromstring(text)
            cases = root.findall(".//testcase")
            test_ids: list[str] = []
            failures = 0
            errors = 0
            skipped = 0
            for case in cases:
                classname = case.attrib.get("classname", "")
                name = case.attrib.get("name", "")
                test_ids.append(f"{classname}::{name}" if classname else name)
                if case.find("failure") is not None:
                    failures += 1
                if case.find("error") is not None:
                    errors += 1
                if case.find("skipped") is not None:
                    skipped += 1
            return {
                "tests": len(cases),
                "failures": failures,
                "errors": errors,
                "skipped": skipped,
                "test_ids": sorted(set(test_ids)),
            }, None
        if parser_type == "tap":
            total = 0
            failed = 0
            skipped = 0
            test_ids: list[str] = []
            for line in text.splitlines():
                stripped = line.strip()
                match = re.match(r"^(not ok|ok)\b(?:\s+\d+)?(?:\s*-\s*)?(.*)$", stripped)
                if match is None:
                    continue
                total += 1
                status_word = match.group(1)
                remainder = match.group(2)
                if status_word == "not ok":
                    failed += 1
                if "# SKIP" in remainder.upper():
                    skipped += 1
                name = remainder.split("#", 1)[0].strip()
                if name:
                    test_ids.append(name)
            return {"tests": total, "failed": failed, "skipped": skipped, "test_ids": sorted(set(test_ids))}, None
    except Exception:
        return None, "PARSER_FAILURE"
    return None, "PARSER_FAILURE"


def is_json_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (bool, str, int, float, decimal.Decimal))


def observation_shape_allowed(value: Any) -> bool:
    if is_json_scalar(value):
        return True
    if isinstance(value, list):
        return len(value) == len({typed_key(item) for item in value}) and all(is_json_scalar(item) for item in value)
    if isinstance(value, dict):
        for item in value.values():
            if is_json_scalar(item):
                continue
            if isinstance(item, list) and all(is_json_scalar(element) for element in item):
                continue
            return False
        return True
    return False


def typed_key(value: Any) -> tuple[str, Any]:
    kind = json_kind(value)
    if kind == "number":
        return kind, decimal.Decimal(str(value))
    return kind, value


def json_kind(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float, decimal.Decimal)) and not isinstance(value, bool):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "unsupported"


class MissingReference(Exception):
    pass


class TypeMismatch(Exception):
    pass


def pointer_get(document: Any, pointer: str) -> Any:
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise MissingReference(pointer)
    current = document
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token not in current:
                raise MissingReference(pointer)
            current = current[token]
        elif isinstance(current, list):
            if not token.isdigit():
                raise MissingReference(pointer)
            index = int(token)
            if index < 0 or index >= len(current):
                raise MissingReference(pointer)
            current = current[index]
        else:
            raise MissingReference(pointer)
    return current


def operand_value(operand: dict[str, Any], document: dict[str, Any]) -> Any:
    if "literal" in operand:
        return operand["literal"]
    return pointer_get(document, operand["ref"])


def strict_equal(left: Any, right: Any) -> bool:
    left_kind = json_kind(left)
    right_kind = json_kind(right)
    if left_kind != right_kind:
        return False
    if left_kind == "number":
        return decimal.Decimal(str(left)) == decimal.Decimal(str(right))
    if left_kind == "array":
        return len(left) == len(right) and all(strict_equal(a, b) for a, b in zip(left, right))
    if left_kind == "object":
        if set(left.keys()) != set(right.keys()):
            return False
        return all(strict_equal(left[key], right[key]) for key in left)
    return left == right


def require_number(value: Any) -> decimal.Decimal:
    if json_kind(value) != "number":
        raise TypeMismatch
    return decimal.Decimal(str(value))


def require_string(value: Any) -> str:
    if not isinstance(value, str):
        raise TypeMismatch
    return value


def require_array(value: Any) -> list[Any]:
    if not isinstance(value, list):
        raise TypeMismatch
    return value


def array_subset(left: list[Any], right: list[Any]) -> bool:
    right_keys = {typed_key(item) for item in right}
    return all(typed_key(item) in right_keys for item in left)


def evaluate_expression(expression: dict[str, Any], document: dict[str, Any]) -> tuple[str, Any, str]:
    operator = expression["operator"]
    try:
        if operator in ("all", "any"):
            results = [evaluate_expression(item, document)[0] for item in expression["expressions"]]
            if operator == "all":
                if "FAIL" in results:
                    return "FAIL", results, "CONDITION_FALSE"
                if "NOT_VERIFIED" in results:
                    return "NOT_VERIFIED", results, "MISSING_REFERENCE"
                return "PASS", results, "CONDITION_TRUE"
            if "PASS" in results:
                return "PASS", results, "CONDITION_TRUE"
            if "NOT_VERIFIED" in results:
                return "NOT_VERIFIED", results, "MISSING_REFERENCE"
            return "FAIL", results, "CONDITION_FALSE"
        if operator == "not":
            status, observed, reason = evaluate_expression(expression["expression"], document)
            if status == "PASS":
                return "FAIL", observed, "CONDITION_FALSE"
            if status == "FAIL":
                return "PASS", observed, "CONDITION_TRUE"
            return "NOT_VERIFIED", observed, reason
        actual = operand_value(expression["actual"], document)
        if operator in ("exists", "not_exists"):
            result = operator == "exists"
            return ("PASS" if result else "FAIL"), actual, ("CONDITION_TRUE" if result else "CONDITION_FALSE")
        expected = operand_value(expression["expected"], document)
        if operator == "eq":
            result = strict_equal(actual, expected)
        elif operator == "neq":
            result = not strict_equal(actual, expected)
        elif operator in ("lt", "lte", "gt", "gte"):
            a_num = require_number(actual)
            e_num = require_number(expected)
            result = {"lt": a_num < e_num, "lte": a_num <= e_num, "gt": a_num > e_num, "gte": a_num >= e_num}[operator]
        elif operator in ("contains", "not_contains", "starts_with", "ends_with"):
            a_text = require_string(actual)
            e_text = require_string(expected)
            if operator == "contains":
                result = e_text in a_text
            elif operator == "not_contains":
                result = e_text not in a_text
            elif operator == "starts_with":
                result = a_text.startswith(e_text)
            else:
                result = a_text.endswith(e_text)
        elif operator.startswith("length_"):
            if not isinstance(actual, (str, list, dict)):
                raise TypeMismatch
            e_num = require_number(expected)
            length = decimal.Decimal(len(actual))
            result = {
                "length_eq": length == e_num,
                "length_lt": length < e_num,
                "length_lte": length <= e_num,
                "length_gt": length > e_num,
                "length_gte": length >= e_num,
            }[operator]
        elif operator in ("contains_all", "contains_none"):
            left = require_array(actual)
            right = require_array(expected)
            subset = array_subset(right, left)
            if operator == "contains_all":
                result = subset
            else:
                left_keys = {typed_key(item) for item in left}
                result = all(typed_key(item) not in left_keys for item in right)
        elif operator in ("set_equal", "set_subset", "set_superset", "set_disjoint"):
            left = require_array(actual)
            right = require_array(expected)
            if operator == "set_equal":
                result = array_subset(left, right) and array_subset(right, left)
            elif operator == "set_subset":
                result = array_subset(left, right)
            elif operator == "set_superset":
                result = array_subset(right, left)
            else:
                right_keys = {typed_key(item) for item in right}
                result = all(typed_key(item) not in right_keys for item in left)
        elif operator == "digest_eq":
            a_text = require_string(actual)
            e_text = require_string(expected)
            if HEX64_RE.fullmatch(a_text) is None or HEX64_RE.fullmatch(e_text) is None:
                raise TypeMismatch
            result = a_text == e_text
        else:
            raise TypeMismatch
        return ("PASS" if result else "FAIL"), actual, ("CONDITION_TRUE" if result else "CONDITION_FALSE")
    except MissingReference:
        if operator == "not_exists":
            return "PASS", None, "CONDITION_TRUE"
        if operator == "exists":
            return "FAIL", None, "CONDITION_FALSE"
        return "NOT_VERIFIED", None, "MISSING_REFERENCE"
    except TypeMismatch:
        return "NOT_VERIFIED", None, "TYPE_MISMATCH"


def execute_observation_step(
    index: int,
    step: dict[str, Any],
    workspace: pathlib.Path,
    initial_diff: str,
) -> dict[str, Any]:
    operation = step["operation"]
    started = now_rfc3339()
    start_ns = time.monotonic_ns()
    observation: Any = None
    if operation.startswith("file.") or operation == "directory.list":
        path = resolve_workspace_path(workspace, step["path"], require_exists=False)
        if operation == "file.exists":
            observation = path.exists()
        elif operation == "file.stat":
            if not path.exists() and not path.is_symlink():
                observation = None
            else:
                st = path.lstat()
                observation = {
                    "size": st.st_size,
                    "mode": stat.S_IMODE(st.st_mode),
                    "mtime_ns": st.st_mtime_ns,
                    "is_file": stat.S_ISREG(st.st_mode),
                    "is_dir": stat.S_ISDIR(st.st_mode),
                    "is_symlink": stat.S_ISLNK(st.st_mode),
                }
        elif operation == "file.sha256":
            if not path.is_file():
                observation = None
            else:
                observation = sha256_file(path)
        else:
            if not path.is_dir():
                observation = None
            else:
                if step["recursive"]:
                    items = [item.relative_to(path).as_posix() for item in path.rglob("*")]
                else:
                    items = [item.name for item in path.iterdir()]
                observation = sorted(set(items))
    elif operation.startswith("git."):
        if operation == "git.head":
            observation = repository_head(workspace)
        elif operation == "git.status":
            result = git_command(workspace, ["status", "--porcelain=v1", "--untracked-files=all"], check=True)
            observation = sorted(set(line for line in result.stdout.decode("utf-8", "surrogateescape").splitlines() if line))
        elif operation == "git.diff":
            if step["baseline"] == "WORKTREE_BEFORE":
                observation = initial_diff
            else:
                result = git_command(workspace, ["diff", "--binary", "HEAD"], check=True)
                observation = result.stdout.decode("utf-8", "surrogateescape")
        elif operation == "git.diff_names":
            if step["baseline"] == "WORKTREE_BEFORE":
                result = git_command(workspace, ["diff", "--name-only", "HEAD"], check=True)
            else:
                result = git_command(workspace, ["diff", "--name-only", "HEAD"], check=True)
            observation = sorted(set(line for line in result.stdout.decode("utf-8", "surrogateescape").splitlines() if line))
        elif operation == "git.tracked_files":
            result = git_command(workspace, ["ls-files", "-z"], check=True)
            observation = sorted(set(item.decode("utf-8", "surrogateescape") for item in result.stdout.split(b"\0") if item))
    duration_ms = max(0, (time.monotonic_ns() - start_ns) // 1_000_000)
    return {
        "index": index,
        "operation": operation,
        "state": "COMPLETED",
        "started_at": started,
        "finished_at": now_rfc3339(),
        "duration_ms": duration_ms,
        "exit_code": 0,
        "termination_reason": "EXITED",
        "observation": observation,
    }


def execute_process_step(
    index: int,
    step: dict[str, Any],
    workspace: pathlib.Path,
    workcopy: pathlib.Path,
    tmp_run: pathlib.Path,
    plan: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if step["network"] == "allow" and not plan["policy"]["allow_network"]:
        fail(POLICY_VIOLATION, EXIT_POLICY, "step requested network without policy authorization")
    bwrap = ensure_bwrap()
    command = sandbox_command(bwrap, workspace, workcopy, step, plan["environment"]["set"])
    stdout_path = resolve_artifact_path(tmp_run, step["stdout_artifact"])
    stderr_path = resolve_artifact_path(tmp_run, step["stderr_artifact"])
    started = now_rfc3339()
    start_ns = time.monotonic_ns()
    state, child_rc, termination, out_cap, err_cap = run_captured(
        command,
        stdout_path,
        stderr_path,
        step["timeout_seconds"],
        plan["policy"]["max_log_bytes"],
        env={"PATH": CONTROLLED_PATH, "LC_ALL": "C", "LANG": "C"},
    )
    duration_ms = max(0, (time.monotonic_ns() - start_ns) // 1_000_000)
    parser = step.get("result_parser", {"type": "none"})["type"]
    observation, parser_error = parse_structured_output(parser, stdout_path, out_cap.truncated)
    result = {
        "index": index,
        "operation": step["operation"],
        "state": state,
        "started_at": started,
        "finished_at": now_rfc3339(),
        "duration_ms": duration_ms,
        "exit_code": child_rc,
        "termination_reason": termination,
        "stdout": out_cap.metadata(step["stdout_artifact"]),
        "stderr": err_cap.metadata(step["stderr_artifact"]),
    }
    if parser != "none":
        result["observation"] = observation
        if parser_error is not None:
            result["observation"] = {"parser_error": parser_error}
    return result, [result["stdout"], result["stderr"]]


def execute_devcontainer_step(
    index: int,
    step: dict[str, Any],
    workspace: pathlib.Path,
    tmp_run: pathlib.Path,
    plan: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not plan["policy"]["allow_container_lifecycle"]:
        fail(POLICY_VIOLATION, EXIT_POLICY, "devcontainer lifecycle not authorized")
    devcontainer = controlled_tool("devcontainer")
    cwd = resolve_workspace_path(workspace, step["cwd"], require_exists=True)
    operation = step["operation"]
    command = [str(devcontainer)]
    if operation == "devcontainer.build":
        command.extend(["build", "--workspace-folder", str(cwd)])
    elif operation == "devcontainer.up":
        command.extend(["up", "--workspace-folder", str(cwd)])
    elif operation == "devcontainer.exec":
        if step["tool"] not in DEVCONTAINER_TOOL_ALLOWLIST:
            fail(PLAN_INVALID, EXIT_PLAN_INVALID, f"unsupported devcontainer tool: {step['tool']}")
        command.extend(["exec", "--workspace-folder", str(cwd), step["tool"], *step["argv"]])
    else:
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, f"unknown devcontainer operation: {operation}")
    stdout_path = resolve_artifact_path(tmp_run, step["stdout_artifact"])
    stderr_path = resolve_artifact_path(tmp_run, step["stderr_artifact"])
    started = now_rfc3339()
    start_ns = time.monotonic_ns()
    state, child_rc, termination, out_cap, err_cap = run_captured(
        command,
        stdout_path,
        stderr_path,
        step["timeout_seconds"],
        plan["policy"]["max_log_bytes"],
        env={"PATH": CONTROLLED_PATH, "LC_ALL": "C", "LANG": "C", **plan["environment"]["set"]},
    )
    duration_ms = max(0, (time.monotonic_ns() - start_ns) // 1_000_000)
    result = {
        "index": index,
        "operation": operation,
        "state": state,
        "started_at": started,
        "finished_at": now_rfc3339(),
        "duration_ms": duration_ms,
        "exit_code": child_rc,
        "termination_reason": termination,
        "stdout": out_cap.metadata(step["stdout_artifact"]),
        "stderr": err_cap.metadata(step["stderr_artifact"]),
    }
    return result, [result["stdout"], result["stderr"]]


def evaluate_assertions(plan: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for assertion_id in sorted(plan["assertions"]):
        assertion = plan["assertions"][assertion_id]
        status, observed, reason = evaluate_expression(assertion["expression"], manifest)
        results[assertion_id] = {
            "mandatory": assertion["mandatory"],
            "status": status,
            "observed": observed,
            "reason_code": reason,
        }
    return results


def validate_manifest(manifest: dict[str, Any], manifest_schema: dict[str, Any]) -> None:
    jsonschema, Draft202012Validator, _, _ = load_jsonschema_modules()
    validator = Draft202012Validator(manifest_schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(validator.iter_errors(manifest), key=lambda item: list(item.absolute_path))
    if errors:
        first = errors[0]
        location = "/" + "/".join(str(item) for item in first.absolute_path)
        fail(PACKAGE_INCOMPLETE, EXIT_PACKAGE_INCOMPLETE, f"manifest schema violation at {location}: {first.message}")


def atomic_publish(tmp_run: pathlib.Path, final_run: pathlib.Path) -> None:
    if final_run.exists():
        fail(PACKAGE_INCOMPLETE, EXIT_PACKAGE_INCOMPLETE, f"final package already exists: {final_run}")
    if tmp_run.parent.parent.stat().st_dev != final_run.parent.stat().st_dev:
        fail(PACKAGE_INCOMPLETE, EXIT_PACKAGE_INCOMPLETE, "temporary and final package paths are on different filesystems")
    os.rename(tmp_run, final_run)


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--schema-dir", required=True)
    parser.add_argument("--expected-plan-sha256", required=True)
    parser.add_argument("--expected-contract-sha256", required=True)
    parser.add_argument("--expected-runner-sha256", required=True)
    parser.add_argument("--run-id")
    try:
        return parser.parse_args(argv)
    except SystemExit:
        fail(RUNNER_INTERNAL_ERROR, EXIT_INTERNAL, "invalid runner invocation")


def main() -> int:
    self_path = pathlib.Path(sys.argv[1]).resolve(strict=True)
    args = parse_cli(sys.argv[2:])
    for name, value in (
        ("expected plan sha256", args.expected_plan_sha256),
        ("expected contract sha256", args.expected_contract_sha256),
        ("expected runner sha256", args.expected_runner_sha256),
    ):
        ensure_hex64(name, value)
    workspace = pathlib.Path.cwd().resolve(strict=True)
    plan_path = pathlib.Path(args.plan).resolve(strict=True)
    contract_path = pathlib.Path(args.contract).resolve(strict=True)
    schema_dir = pathlib.Path(args.schema_dir).resolve(strict=True)
    actual_runner_start = sha256_file(self_path)
    actual_plan = sha256_file(plan_path)
    actual_contract = sha256_file(contract_path)
    if actual_runner_start != args.expected_runner_sha256:
        fail(CONTROL_FAILURE, EXIT_CONTROL_INTEGRITY, "runner start hash mismatch")
    if actual_plan != args.expected_plan_sha256:
        fail(CONTROL_FAILURE, EXIT_CONTROL_INTEGRITY, "verification plan hash mismatch")
    if actual_contract != args.expected_contract_sha256:
        fail(CONTROL_FAILURE, EXIT_CONTROL_INTEGRITY, "contract hash mismatch")
    try:
        plan = load_json_bytes(plan_path)
        contract = load_json_bytes(contract_path)
    except Exception as exc:
        fail(PLAN_INVALID, EXIT_PLAN_INVALID, f"strict JSON parsing failed: {exc}")
    _, _, manifest_schema = validate_plan_schema(plan, schema_dir)
    if plan["control"]["expected_contract_sha256"] != args.expected_contract_sha256:
        fail(CONTROL_FAILURE, EXIT_CONTROL_INTEGRITY, "plan expected_contract_sha256 differs from external anchor")
    if plan["control"]["expected_runner_sha256"] != args.expected_runner_sha256:
        fail(CONTROL_FAILURE, EXIT_CONTROL_INTEGRITY, "plan expected_runner_sha256 differs from external anchor")
    enforce_semantic_plan_rules(plan, contract)
    run_id = args.run_id
    if run_id is None:
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_id = f"RUN-{stamp}-{os.getpid()}"
    if RUN_ID_RE.fullmatch(run_id) is None:
        fail(RUNNER_INTERNAL_ERROR, EXIT_INTERNAL, f"invalid run id: {run_id}")
    package_root = workspace / ".ai-control" / "verification-package"
    tmp_parent = package_root / ".tmp"
    final_run = package_root / run_id
    tmp_run = tmp_parent / run_id
    package_root.mkdir(parents=True, exist_ok=True)
    tmp_parent.mkdir(parents=True, exist_ok=True)
    if tmp_run.exists() or final_run.exists():
        fail(PACKAGE_INCOMPLETE, EXIT_PACKAGE_INCOMPLETE, f"run id already exists: {run_id}")
    tmp_run.mkdir(parents=False)
    (tmp_run / "raw").mkdir()
    (tmp_run / "observations").mkdir()
    run_started = now_rfc3339()
    head_before = repository_head(workspace)
    tree_before = workspace_fingerprint(workspace)
    initial_diff = repository_initial_diff(workspace)
    steps: list[dict[str, Any]] = []
    package_artifacts: list[dict[str, Any]] = []
    sandbox_parent: pathlib.Path | None = None
    sandbox_work: pathlib.Path | None = None
    try:
        for index, step in enumerate(plan["steps"]):
            operation = step["operation"]
            if operation == "process.run":
                if sandbox_work is None:
                    sandbox_parent = pathlib.Path(tempfile.mkdtemp(prefix="fvr-sandbox-", dir="/tmp"))
                    sandbox_work = sandbox_parent / "work"
                    copy_workspace(workspace, sandbox_work)
                result, artifacts = execute_process_step(index, step, workspace, sandbox_work, tmp_run, plan)
                steps.append(result)
                package_artifacts.extend(artifacts)
            elif operation.startswith("devcontainer."):
                result, artifacts = execute_devcontainer_step(index, step, workspace, tmp_run, plan)
                steps.append(result)
                package_artifacts.extend(artifacts)
            else:
                steps.append(execute_observation_step(index, step, workspace, initial_diff))
        actual_runner_end = sha256_file(self_path)
        if actual_runner_end != args.expected_runner_sha256 or actual_runner_end != actual_runner_start:
            fail(CONTROL_FAILURE, EXIT_CONTROL_INTEGRITY, "runner end hash mismatch")
        head_after = repository_head(workspace)
        tree_after = workspace_fingerprint(workspace)
        manifest: dict[str, Any] = {
            "schema_version": "FVR-MANIFEST-1.0",
            "protocol": {"name": "FVR", "version": "1.0", "assurance_level": "E1_DETERMINISTIC_LOCAL"},
            "run": {"run_id": run_id, "started_at": run_started, "finished_at": now_rfc3339()},
            "control": {
                "contract_id": plan["plan_metadata"]["contract_id"],
                "contract_version": plan["plan_metadata"]["contract_version"],
                "contract_sha256": actual_contract,
                "verification_plan_sha256": actual_plan,
                "runner_sha256_start": actual_runner_start,
                "runner_sha256_end": actual_runner_end,
            },
            "repository": {
                "head_before": head_before,
                "head_after": head_after,
                "working_tree_before_sha256": tree_before,
                "working_tree_after_sha256": tree_after,
            },
            "runner": {"state": RUN_COMPLETED},
            "steps": steps,
            "assertions": {},
            "package_artifacts": package_artifacts,
        }
        manifest["assertions"] = evaluate_assertions(plan, manifest)
        if any(item["mandatory"] and item["status"] != "PASS" for item in manifest["assertions"].values()):
            manifest["runner"]["state"] = RUN_COMPLETED_FAILED
        validate_manifest(manifest, manifest_schema)
        manifest_path = tmp_run / "manifest.json"
        with manifest_path.open("wb") as handle:
            handle.write(json_dump_bytes(manifest))
            handle.flush()
            os.fsync(handle.fileno())
        manifest_digest_path = tmp_run / "manifest.sha256"
        with manifest_digest_path.open("w", encoding="ascii", newline="\n") as handle:
            handle.write(sha256_file(manifest_path) + "  manifest.json\n")
            handle.flush()
            os.fsync(handle.fileno())
        actual_runner_final = sha256_file(self_path)
        if actual_runner_final != args.expected_runner_sha256:
            fail(CONTROL_FAILURE, EXIT_CONTROL_INTEGRITY, "runner changed after manifest generation")
        atomic_publish(tmp_run, final_run)
        sys.stdout.write(json.dumps({"runner_state": manifest["runner"]["state"], "package": str(final_run)}, sort_keys=True) + "\n")
        sys.stdout.flush()
        return EXIT_OK
    finally:
        if sandbox_parent is not None:
            shutil.rmtree(sandbox_parent, ignore_errors=True)


try:
    raise SystemExit(main())
except FvrFailure as exc:
    emit_control_failure(exc.state, exc.reason)
    raise SystemExit(exc.exit_code)
except KeyboardInterrupt:
    emit_control_failure(RUNNER_INTERNAL_ERROR, "runner interrupted")
    raise SystemExit(EXIT_INTERNAL)
except Exception as exc:
    emit_control_failure(RUNNER_INTERNAL_ERROR, f"unhandled runner error: {type(exc).__name__}: {exc}")
    raise SystemExit(EXIT_INTERNAL)
PY_FVR_ENGINE
runner_rc=$?
exit "$runner_rc"
