#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import dataclasses
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
import time
from typing import Any, Iterable

PASS = "PASS"
FAIL = "FAIL"
HARNESS_INVALID = "HARNESS_INVALID"

CONTROLLED_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")

STATIC_VECTOR_FRAGMENTS: dict[str, str] = {
    "STA-001-EVAL-DIRECT": 'eval "$payload"\n',
    "STA-002-EVAL-OBFUSCATED": 'e"v"al "$payload"\n',
    "STA-003-EVAL-BUILTIN": 'builtin eval "$payload"\n',
    "STA-004-SOURCE": 'source "$file"\n',
    "STA-005-DOT-SOURCE": '. "$file"\n',
    "STA-006-BASH-C": 'bash -c "$payload"\n',
    "STA-007-COMMAND-SUB": 'x=$(printf x)\n',
    "STA-008-BACKTICK": 'x=`printf x`\n',
    "STA-009-PROCESS-SUB": 'cat <(printf x)\n',
    "STA-010-INDIRECT": 'printf "%s\\n" "${!name}"\n',
    "STA-011-NAMEREF": 'declare -n ref=name\n',
    "STA-012-EXEC": 'exec "$tool" "${argv[@]}"\n',
    "STA-013-ERREXIT": 'set -e\n',
    "STA-014-SHELLCHECK-DISABLE": '# shellcheck disable=SC2086\nprintf "%s\\n" $x\n',
    "STA-015-SHELLCHECK-CLEAN": '#!/usr/bin/env bash\nset -u\nprintf "%s\\n" "$1"\n',
}


@dataclasses.dataclass
class Result:
    id: str
    suite: str
    status: str
    details: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


class HarnessPreconditionError(Exception):
    pass


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def read_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def which_required(name: str) -> str:
    resolved = shutil.which(name, path=CONTROLLED_PATH)
    if resolved is None:
        raise HarnessPreconditionError(f"required executable unavailable: {name}")
    return str(pathlib.Path(resolved).resolve(strict=True))


def import_bashlex() -> Any:
    try:
        import bashlex
    except Exception as exc:
        raise HarnessPreconditionError(f"bashlex unavailable: {exc}") from exc
    return bashlex


def check_runner_python_dependencies() -> None:
    env_tool = pathlib.Path("/usr/bin/env")
    if not env_tool.is_file():
        raise HarnessPreconditionError("/usr/bin/env unavailable")
    command = [
        str(env_tool),
        "-i",
        f"PATH={CONTROLLED_PATH}",
        "LC_ALL=C",
        "LANG=C",
        "python3",
        "-c",
        "import jsonschema, referencing",
    ]
    result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise HarnessPreconditionError(
            "runner Python environment lacks jsonschema/referencing: " + result.stderr.decode("utf-8", "replace").strip()
        )


def shell_word_source(script: str, node: Any) -> str:
    start, end = node.pos
    return script[start:end]


def normalize_static_word(raw: str) -> str | None:
    out: list[str] = []
    i = 0
    quote: str | None = None
    while i < len(raw):
        ch = raw[i]
        if quote is None:
            if ch in ("'", '"'):
                quote = ch
                i += 1
                continue
            if ch == "\\":
                i += 1
                if i >= len(raw):
                    return None
                out.append(raw[i])
                i += 1
                continue
            if ch in "$`":
                return None
            out.append(ch)
            i += 1
            continue
        if ch == quote:
            quote = None
            i += 1
            continue
        if quote == '"' and ch == "\\" and i + 1 < len(raw):
            i += 1
            out.append(raw[i])
            i += 1
            continue
        if quote == '"' and ch in "$`":
            return None
        out.append(ch)
        i += 1
    if quote is not None:
        return None
    return "".join(out)


def iter_nodes(node: Any) -> Iterable[Any]:
    yield node
    for attr in ("parts", "list", "command", "output", "input", "heredoc"):
        value = getattr(node, attr, None)
        if isinstance(value, list):
            for item in value:
                if hasattr(item, "kind"):
                    yield from iter_nodes(item)
        elif hasattr(value, "kind"):
            yield from iter_nodes(value)


def command_words(script: str, command_node: Any) -> list[str | None]:
    words: list[str | None] = []
    for part in getattr(command_node, "parts", []):
        if getattr(part, "kind", None) != "word":
            continue
        words.append(normalize_static_word(shell_word_source(script, part)))
    return words


def static_ast_findings(script: str) -> list[dict[str, Any]]:
    bashlex = import_bashlex()
    try:
        roots = bashlex.parse(script)
    except Exception as exc:
        return [{"rule": "PARSE_ERROR", "detail": str(exc)}]
    findings: list[dict[str, Any]] = []
    for root in roots:
        for node in iter_nodes(root):
            kind = getattr(node, "kind", None)
            raw = shell_word_source(script, node)
            if kind == "commandsubstitution":
                findings.append({"rule": "SA-004", "detail": raw})
            elif kind == "processsubstitution":
                findings.append({"rule": "SA-005", "detail": raw})
            elif kind == "parameter" and raw.startswith("${!"):
                findings.append({"rule": "SA-006", "detail": raw})
            elif kind == "command":
                words = command_words(script, node)
                if not words:
                    continue
                command = words[0]
                if command is None:
                    findings.append({"rule": "DYNAMIC_COMMAND_WORD", "detail": raw})
                    continue
                if command == "eval":
                    findings.append({"rule": "SA-001", "detail": raw})
                if command in ("source", "."):
                    findings.append({"rule": "SA-002", "detail": raw})
                if command == "exec":
                    findings.append({"rule": "SA-008", "detail": raw})
                if command == "builtin" and len(words) > 1 and words[1] == "eval":
                    findings.append({"rule": "SA-001", "detail": raw})
                if command in ("bash", "sh", "dash", "zsh", "ksh") and "-c" in words[1:]:
                    findings.append({"rule": "SA-003", "detail": raw})
                if command in ("declare", "local", "typeset") and "-n" in words[1:]:
                    findings.append({"rule": "SA-007", "detail": raw})
                if command == "set":
                    if "-e" in words[1:]:
                        findings.append({"rule": "SA-009", "detail": raw})
                    if len(words) >= 3 and words[1] == "-o" and words[2] == "errexit":
                        findings.append({"rule": "SA-009", "detail": raw})
    if "# shellcheck" in script.lower():
        findings.append({"rule": "SA-010", "detail": "inline ShellCheck directive"})
    return findings


def extract_python_engine(runner_text: str) -> str:
    marker = "<<'PY_FVR_ENGINE'\n"
    start = runner_text.find(marker)
    if start < 0:
        raise ValueError("PY_FVR_ENGINE start marker missing")
    start += len(marker)
    end = runner_text.find("\nPY_FVR_ENGINE\n", start)
    if end < 0:
        raise ValueError("PY_FVR_ENGINE end marker missing")
    return runner_text[start:end]


def python_ast_findings(source: str) -> list[dict[str, Any]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [{"rule": "PY_PARSE_ERROR", "detail": str(exc)}]
    findings: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id in {"eval", "exec", "compile", "__import__"}:
            findings.append({"rule": "PY_DYNAMIC_EVALUATION", "detail": func.id, "line": node.lineno})
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            base = func.value.id
            name = func.attr
            if base == "os" and name in {"system", "popen"}:
                findings.append({"rule": "PY_SHELL_EXECUTION", "detail": f"os.{name}", "line": node.lineno})
            if base == "subprocess" and name in {"Popen", "run", "call", "check_call", "check_output"}:
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"rule": "PY_SHELL_TRUE", "detail": f"subprocess.{name}", "line": node.lineno})
    return findings


def run_shellcheck(runner: pathlib.Path) -> tuple[int, str, str]:
    shellcheck = which_required("shellcheck")
    env = {"PATH": CONTROLLED_PATH, "SHELLCHECK_OPTS": "", "LC_ALL": "C", "LANG": "C"}
    command = [
        shellcheck,
        "--norc",
        "--shell=bash",
        "--severity=style",
        "--enable=all",
        "--extended-analysis=true",
        "--format=json1",
        str(runner),
    ]
    result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
    return result.returncode, result.stdout.decode("utf-8", "replace"), result.stderr.decode("utf-8", "replace")


def static_suite(runner: pathlib.Path) -> list[Result]:
    results: list[Result] = []
    text = runner.read_text(encoding="utf-8")
    bash = which_required("bash")
    syntax = subprocess.run([bash, "--noprofile", "--norc", "-n", str(runner)], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    results.append(Result("STATIC-RUNNER-BASH-N", "STATIC_ANALYSIS", PASS if syntax.returncode == 0 else FAIL, {"exit_code": syntax.returncode, "stderr": syntax.stderr.decode("utf-8", "replace")}))
    sc_rc, sc_out, sc_err = run_shellcheck(runner)
    findings_count = None
    if sc_rc == 0:
        try:
            parsed = json.loads(sc_out or '{"comments":[]}')
            if isinstance(parsed, dict) and isinstance(parsed.get("comments"), list):
                findings_count = len(parsed["comments"])
            elif isinstance(parsed, list):
                findings_count = len(parsed)
        except Exception:
            findings_count = None
    shellcheck_pass = sc_rc == 0 and findings_count in (0, None) and not sc_err.strip()
    results.append(Result("STATIC-RUNNER-SHELLCHECK", "STATIC_ANALYSIS", PASS if shellcheck_pass else FAIL, {"exit_code": sc_rc, "findings_count": findings_count, "stdout": sc_out, "stderr": sc_err}))
    ast_findings = static_ast_findings(text)
    results.append(Result("STATIC-RUNNER-AST", "STATIC_ANALYSIS", PASS if not ast_findings else FAIL, {"findings": ast_findings}))
    try:
        py_source = extract_python_engine(text)
        py_findings = python_ast_findings(py_source)
    except Exception as exc:
        py_findings = [{"rule": "PY_ENGINE_EXTRACTION", "detail": str(exc)}]
    results.append(Result("STATIC-RUNNER-EMBEDDED-PYTHON-AST", "STATIC_ANALYSIS", PASS if not py_findings else FAIL, {"findings": py_findings}))
    for vector_id, fragment in STATIC_VECTOR_FRAGMENTS.items():
        if vector_id == "STA-015-SHELLCHECK-CLEAN":
            findings = static_ast_findings(fragment)
            subject_rejected = bool(findings)
            status = FAIL if subject_rejected else PASS
            results.append(Result(vector_id, "STATIC_ANALYSIS", status, {"subject_expected": "PASS", "findings": findings}))
            continue
        findings = static_ast_findings(fragment)
        subject_rejected = bool(findings)
        results.append(Result(vector_id, "STATIC_ANALYSIS", PASS if subject_rejected else FAIL, {"subject_expected": "FAIL", "findings": findings}))
    return results


def git_init_repo(root: pathlib.Path) -> None:
    git = which_required("git")
    env = {"PATH": CONTROLLED_PATH, "LC_ALL": "C", "LANG": "C"}
    commands = [
        [git, "init", "-q"],
        [git, "config", "user.email", "fvr@example.invalid"],
        [git, "config", "user.name", "FVR Harness"],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode != 0:
            raise HarnessPreconditionError(f"git fixture setup failed: {command}: {result.stderr.decode('utf-8','replace')}")
    (root / "fixture.txt").write_text("fixture\n", encoding="utf-8")
    for command in ([git, "add", "fixture.txt"], [git, "commit", "-qm", "fixture"]):
        result = subprocess.run(command, cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode != 0:
            raise HarnessPreconditionError(f"git fixture commit failed: {result.stderr.decode('utf-8','replace')}")


def make_repo(base: pathlib.Path, runner_source: pathlib.Path, schema_dir: pathlib.Path, name: str) -> pathlib.Path:
    root = base / name
    root.mkdir(parents=True)
    git_init_repo(root)
    runner_dir = root / ".ai-control" / "runner"
    schema_target = root / ".ai-control" / "schema"
    runner_dir.mkdir(parents=True)
    schema_target.mkdir(parents=True)
    shutil.copy2(runner_source, runner_dir / "verify.sh")
    os.chmod(runner_dir / "verify.sh", 0o755)
    for filename in ("assertion.schema.json", "verification-plan.schema.json", "manifest.schema.json", "normative-semantics.json"):
        shutil.copy2(schema_dir / filename, schema_target / filename)
    return root


def minimal_contract(contract_id: str, assertion_ids: list[str]) -> dict[str, Any]:
    acceptance = [{"id": item} for item in assertion_ids if item.startswith("AC-")]
    invariants = [{"id": item} for item in assertion_ids if item.startswith("INV-")]
    return {"contract_metadata": {"id": contract_id, "version": "1.0"}, "invariants": invariants, "acceptance_criteria": acceptance}


def make_plan(root: pathlib.Path, step: dict[str, Any], assertion: dict[str, Any], *, allow_network: bool = False, allow_container: bool = False, plan_id: str = "VP-HARNESS-001", contract_id: str = "CTR-HARNESS-001") -> tuple[pathlib.Path, pathlib.Path, dict[str, str]]:
    runner = root / ".ai-control" / "runner" / "verify.sh"
    contract_path = root / ".ai-control" / "contract.json"
    contract = minimal_contract(contract_id, ["AC-001"])
    write_json(contract_path, contract)
    contract_hash = sha256_file(contract_path)
    runner_hash = sha256_file(runner)
    plan = {
        "schema_version": "FVR-1.0",
        "plan_metadata": {"plan_id": plan_id, "contract_id": contract_id, "contract_version": "1.0"},
        "control": {"runner_policy_version": "FVR-1.0", "expected_contract_sha256": contract_hash, "expected_runner_sha256": runner_hash},
        "workspace": {"root": "."},
        "policy": {
            "fail_closed": True,
            "network_default": "deny",
            "allow_network": allow_network,
            "allow_container_lifecycle": allow_container,
            "allow_host_process_execution": False,
            "max_step_timeout_seconds": 30,
            "max_log_bytes": 1048576,
            "max_steps": 8,
        },
        "environment": {"inherit": [], "set": {"CI": "true"}},
        "steps": [step],
        "assertions": {"AC-001": {"mandatory": True, "expression": assertion}},
    }
    plan_path = root / ".ai-control" / "verification-plan.json"
    write_json(plan_path, plan)
    anchors = {"plan": sha256_file(plan_path), "contract": contract_hash, "runner": runner_hash}
    return plan_path, contract_path, anchors


def runner_command(root: pathlib.Path, plan_path: pathlib.Path, contract_path: pathlib.Path, anchors: dict[str, str], run_id: str) -> list[str]:
    return [
        str(root / ".ai-control" / "runner" / "verify.sh"),
        "--plan", str(plan_path),
        "--contract", str(contract_path),
        "--schema-dir", str(root / ".ai-control" / "schema"),
        "--expected-plan-sha256", anchors["plan"],
        "--expected-contract-sha256", anchors["contract"],
        "--expected-runner-sha256", anchors["runner"],
        "--run-id", run_id,
    ]


def run_runner(root: pathlib.Path, command: list[str], timeout: float = 60) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"PATH": CONTROLLED_PATH, "LC_ALL": "C", "LANG": "C"}, timeout=timeout, check=False)


def load_manifest(root: pathlib.Path, run_id: str) -> dict[str, Any] | None:
    path = root / ".ai-control" / "verification-package" / run_id / "manifest.json"
    if not path.is_file():
        return None
    return read_json(path)


def process_step(code: str, *, timeout: int = 5, network: str = "deny", parser: str = "none", name: str = "case") -> dict[str, Any]:
    return {
        "operation": "process.run",
        "execution_target": "sandbox",
        "tool": "python3",
        "argv": ["-c", code],
        "cwd": ".",
        "timeout_seconds": timeout,
        "network": network,
        "stdout_artifact": f"raw/{name}.stdout",
        "stderr_artifact": f"raw/{name}.stderr",
        "result_parser": {"type": parser},
    }


def eq_exit_zero() -> dict[str, Any]:
    return {"operator": "eq", "actual": {"ref": "/steps/0/exit_code"}, "expected": {"literal": 0}}


def sandbox_suite(base: pathlib.Path, runner: pathlib.Path, schema_dir: pathlib.Path) -> list[Result]:
    results: list[Result] = []
    bwrap = pathlib.Path(which_required("bwrap"))
    if bwrap.stat().st_mode & stat.S_ISUID:
        raise HarnessPreconditionError("bwrap is setuid; implementation profile rejects setuid bubblewrap")
    probes = {
        "SBX-001-NETWORK": r'''import json,socket,sys
names=[]
for line in open("/proc/net/dev",encoding="utf-8").read().splitlines()[2:]:
    if ":" in line:names.append(line.split(":",1)[0].strip())
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.settimeout(1.0);rc=s.connect_ex(("198.51.100.1",9))
print(json.dumps({"interfaces":sorted(names),"connect_ex":rc},sort_keys=True))
sys.exit(0 if set(names).issubset({"lo"}) and rc!=0 else 71)''',
        "SBX-002-SOURCE-READ-ONLY": r'''import errno,sys
p="/fvr/source/.fvr-write-probe"
try:open(p,"wb").write(b"x")
except OSError as e:sys.exit(0 if e.errno in (errno.EROFS,errno.EACCES,errno.EPERM) else 72)
sys.exit(73)''',
        "SBX-003-ROOT-READ-ONLY": r'''import errno,os,sys
ro=bool(os.statvfs("/").f_flag & os.ST_RDONLY)
try:open("/etc/.fvr-root-write-probe","wb").write(b"x");failed=False
except OSError:failed=True
print(int(ro),int(failed));sys.exit(0 if ro and failed else 74)''',
        "SBX-004-WORK-COPY-EPHEMERAL": r'''from pathlib import Path
p=Path("/fvr/work/.fvr-work-probe");p.write_text("work-only",encoding="utf-8");print(p.read_text(encoding="utf-8"))''',
        "SBX-005-PRIVILEGE": r'''import os,sys,json
status={}
for line in open("/proc/self/status",encoding="utf-8"):
    if ":" in line:k,v=line.split(":",1);status[k]=v.strip()
failed=False
try:os.setuid(0)
except PermissionError:failed=True
ok=os.geteuid()!=0 and status.get("NoNewPrivs")=="1" and status.get("CapEff")=="0000000000000000" and failed
print(json.dumps({"euid":os.geteuid(),"NoNewPrivs":status.get("NoNewPrivs"),"CapEff":status.get("CapEff"),"setuid_failed":failed},sort_keys=True));sys.exit(0 if ok else 75)''',
        "SBX-006-TTY-STDIN": r'''import os,sys,json
b=sys.stdin.buffer.read(1);v={"stdin_eof":b==b"","tty0":os.isatty(0),"tty1":os.isatty(1),"tty2":os.isatty(2)};print(json.dumps(v,sort_keys=True));sys.exit(0 if v["stdin_eof"] and not v["tty0"] and not v["tty1"] and not v["tty2"] else 76)''',
        "SBX-007-SECRET": r'''import os,sys
present="FVR_SECRET_SENTINEL" in os.environ;print("present" if present else "absent");sys.exit(77 if present else 0)''',
    }
    for number, (vector_id, code) in enumerate(probes.items(), start=1):
        root = make_repo(base, runner, schema_dir, f"sandbox-{number:02d}")
        step = process_step(code, name=vector_id.lower())
        plan_path, contract_path, anchors = make_plan(root, step, eq_exit_zero(), plan_id=f"VP-SBX-{number:03d}", contract_id=f"CTR-SBX-{number:03d}")
        run_id = f"RUN-SBX-{number:03d}"
        env = {"PATH": CONTROLLED_PATH, "LC_ALL": "C", "LANG": "C", "FVR_SECRET_SENTINEL": "TOPSECRET"}
        process = subprocess.run(runner_command(root, plan_path, contract_path, anchors, run_id), cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=30, check=False)
        manifest = load_manifest(root, run_id)
        ok = process.returncode == 0 and manifest is not None and manifest["steps"][0]["exit_code"] == 0
        details: dict[str, Any] = {"runner_exit_code": process.returncode, "stderr": process.stderr.decode("utf-8", "replace")}
        if manifest is not None:
            details["step"] = manifest["steps"][0]
        if vector_id == "SBX-002-SOURCE-READ-ONLY":
            ok = ok and not (root / ".fvr-write-probe").exists()
        if vector_id == "SBX-004-WORK-COPY-EPHEMERAL":
            ok = ok and not (root / ".fvr-work-probe").exists()
        if vector_id == "SBX-007-SECRET" and manifest is not None:
            raw = root / ".ai-control" / "verification-package" / run_id / manifest["steps"][0]["stdout"]["path"]
            ok = ok and raw.read_text(encoding="utf-8").strip() == "absent"
        results.append(Result(vector_id, "SANDBOX_ENFORCEMENT", PASS if ok else FAIL, details))
    return results


def telemetry_suite(base: pathlib.Path, runner: pathlib.Path, schema_dir: pathlib.Path) -> list[Result]:
    results: list[Result] = []
    cases: list[tuple[str, str, int, dict[str, Any], dict[str, Any], str]] = []
    code1 = 'import sys;sys.stdout.write("STDOUT_SENTINEL\\n");sys.stdout.flush();sys.stderr.write("STDERR_SENTINEL\\n");sys.stderr.flush();sys.exit(1)'
    cases.append(("TEL-001-CHILD-EXIT-1", code1, 5, eq_exit_zero(), {"runner_rc": 0, "step_state": "COMPLETED", "step_rc": 1, "termination": "EXITED", "assertion": "FAIL"}, "none"))
    code2 = 'import sys,time;print("OUT_BEFORE",flush=True);print("ERR_BEFORE",file=sys.stderr,flush=True);time.sleep(30)'
    cases.append(("TEL-002-TIMEOUT", code2, 1, eq_exit_zero(), {"runner_rc": 0, "step_state": "TIMED_OUT", "step_rc": None, "termination": "TIMEOUT"}, "none"))
    metas = ['$(touch /fvr/work/SHELL_REINTERPRETED)', ';', '&&', '>', '|', '`id`']
    code3 = 'import json,sys;print(json.dumps(sys.argv[1:]))'
    step3 = process_step(code3, name="tel-003")
    step3["argv"].extend(metas)
    root3 = make_repo(base, runner, schema_dir, "telemetry-03")
    plan3, contract3, anchor3 = make_plan(root3, step3, eq_exit_zero(), plan_id="VP-TEL-003", contract_id="CTR-TEL-003")
    proc3 = run_runner(root3, runner_command(root3, plan3, contract3, anchor3, "RUN-TEL-003"), timeout=30)
    man3 = load_manifest(root3, "RUN-TEL-003")
    ok3 = proc3.returncode == 0 and man3 is not None and man3["steps"][0]["exit_code"] == 0
    if man3 is not None:
        outpath = root3 / ".ai-control" / "verification-package" / "RUN-TEL-003" / man3["steps"][0]["stdout"]["path"]
        try:
            observed_args = json.loads(outpath.read_text(encoding="utf-8"))
        except Exception:
            observed_args = None
        ok3 = ok3 and observed_args == metas and not (root3 / "SHELL_REINTERPRETED").exists()
    else:
        observed_args = None
    results.append(Result("TEL-003-ARGV-LITERAL", "TELEMETRY", PASS if ok3 else FAIL, {"runner_exit_code": proc3.returncode, "observed_args": observed_args, "stderr": proc3.stderr.decode("utf-8", "replace")}))
    for number, (vector_id, code, timeout_seconds, assertion, expected, parser) in enumerate(cases, start=1):
        root = make_repo(base, runner, schema_dir, f"telemetry-{number:02d}")
        step = process_step(code, timeout=timeout_seconds, name=vector_id.lower(), parser=parser)
        plan, contract, anchors = make_plan(root, step, assertion, plan_id=f"VP-TEL-{number:03d}", contract_id=f"CTR-TEL-{number:03d}")
        run_id = f"RUN-TEL-{number:03d}"
        proc = run_runner(root, runner_command(root, plan, contract, anchors, run_id), timeout=35)
        manifest = load_manifest(root, run_id)
        ok = proc.returncode == expected["runner_rc"] and manifest is not None
        details: dict[str, Any] = {"runner_exit_code": proc.returncode, "stderr": proc.stderr.decode("utf-8", "replace")}
        if manifest is not None:
            step_result = manifest["steps"][0]
            ok = ok and step_result["state"] == expected["step_state"] and step_result["exit_code"] == expected["step_rc"] and step_result["termination_reason"] == expected["termination"]
            if "assertion" in expected:
                ok = ok and manifest["assertions"]["AC-001"]["status"] == expected["assertion"]
            package = root / ".ai-control" / "verification-package" / run_id
            stdout_bytes = (package / step_result["stdout"]["path"]).read_bytes()
            stderr_bytes = (package / step_result["stderr"]["path"]).read_bytes()
            ok = ok and step_result["stdout"]["sha256"] == hashlib.sha256(stdout_bytes).hexdigest()
            ok = ok and step_result["stderr"]["sha256"] == hashlib.sha256(stderr_bytes).hexdigest()
            if vector_id == "TEL-002-TIMEOUT":
                ok = ok and b"OUT_BEFORE" in stdout_bytes and b"ERR_BEFORE" in stderr_bytes
            details["step"] = step_result
        results.append(Result(vector_id, "TELEMETRY", PASS if ok else FAIL, details))
    # TEL-004 reuses child-exit-1 raw artifacts and proves exact stream separation/digests.
    source = next((result for result in results if result.id == "TEL-001-CHILD-EXIT-1"), None)
    ok4 = source is not None and source.status == PASS
    details4: dict[str, Any] = {"reuses": "TEL-001-CHILD-EXIT-1"}
    if ok4:
        root = base / "telemetry-01"
        manifest = load_manifest(root, "RUN-TEL-001")
        if manifest is None:
            ok4 = False
        else:
            package = root / ".ai-control" / "verification-package" / "RUN-TEL-001"
            out = (package / manifest["steps"][0]["stdout"]["path"]).read_bytes()
            err = (package / manifest["steps"][0]["stderr"]["path"]).read_bytes()
            expected_out = b"STDOUT_SENTINEL\n"
            expected_err = b"STDERR_SENTINEL\n"
            ok4 = out == expected_out and err == expected_err and hashlib.sha256(out).hexdigest() != hashlib.sha256(err).hexdigest()
            details4.update({"stdout_sha256": hashlib.sha256(out).hexdigest(), "stderr_sha256": hashlib.sha256(err).hexdigest()})
    results.append(Result("TEL-004-STREAM-HASHES", "TELEMETRY", PASS if ok4 else FAIL, details4))
    return results


def control_integrity_suite(base: pathlib.Path, runner: pathlib.Path, schema_dir: pathlib.Path) -> list[Result]:
    results: list[Result] = []
    base_code = 'print("NO_STEP_SHOULD_RUN")'
    mutations = [
        ("CTL-001-CONTRACT-HASH-MISMATCH", "contract", "0" * 64),
        ("CTL-002-PLAN-HASH-MISMATCH", "plan", "0" * 64),
        ("CTL-003-RUNNER-HASH-START-MISMATCH", "runner", "0" * 64),
    ]
    for index, (vector_id, key, bad_hash) in enumerate(mutations, start=1):
        root = make_repo(base, runner, schema_dir, f"control-{index:02d}")
        plan, contract, anchors = make_plan(root, process_step(base_code, name=vector_id.lower()), eq_exit_zero(), plan_id=f"VP-CTL-{index:03d}", contract_id=f"CTR-CTL-{index:03d}")
        anchors[key] = bad_hash
        proc = run_runner(root, runner_command(root, plan, contract, anchors, f"RUN-CTL-{index:03d}"))
        ok = proc.returncode == 11 and load_manifest(root, f"RUN-CTL-{index:03d}") is None
        results.append(Result(vector_id, "CONTROL_INTEGRITY", PASS if ok else FAIL, {"runner_exit_code": proc.returncode, "stderr": proc.stderr.decode("utf-8", "replace")}))
    # Runner end mutation.
    root = make_repo(base, runner, schema_dir, "control-04")
    step = process_step('import time;print("START",flush=True);time.sleep(5)', timeout=10, name="ctl004")
    plan, contract, anchors = make_plan(root, step, eq_exit_zero(), plan_id="VP-CTL-004", contract_id="CTR-CTL-004")
    run_id = "RUN-CTL-004"
    command = runner_command(root, plan, contract, anchors, run_id)
    proc = subprocess.Popen(command, cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"PATH": CONTROLLED_PATH, "LC_ALL": "C", "LANG": "C"}, start_new_session=True)
    temp_stdout = root / ".ai-control" / "verification-package" / ".tmp" / run_id / "raw" / "ctl004.stdout"
    deadline = time.time() + 15
    observed = False
    while time.time() < deadline:
        if temp_stdout.is_file() and b"START" in temp_stdout.read_bytes():
            observed = True
            break
        if proc.poll() is not None:
            break
        time.sleep(0.05)
    if observed:
        runner_copy = root / ".ai-control" / "runner" / "verify.sh"
        with runner_copy.open("ab") as handle:
            handle.write(b"\n")
            handle.flush()
            os.fsync(handle.fileno())
    try:
        stdout, stderr = proc.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        stdout, stderr = proc.communicate()
    ok = observed and proc.returncode == 11 and load_manifest(root, run_id) is None
    results.append(Result("CTL-004-RUNNER-HASH-END-MUTATION", "CONTROL_INTEGRITY", PASS if ok else FAIL, {"observed_start": observed, "runner_exit_code": proc.returncode, "stdout": stdout.decode("utf-8", "replace"), "stderr": stderr.decode("utf-8", "replace")}))
    # Symlink escape.
    root = make_repo(base, runner, schema_dir, "control-05")
    (root / "escape").symlink_to("/etc", target_is_directory=True)
    step = {"operation": "file.stat", "path": "escape/passwd"}
    plan, contract, anchors = make_plan(root, step, {"operator": "exists", "actual": {"ref": "/steps/0/observation"}}, plan_id="VP-PATH-001", contract_id="CTR-PATH-001")
    proc = run_runner(root, runner_command(root, plan, contract, anchors, "RUN-PATH-001"))
    ok = proc.returncode == 12 and load_manifest(root, "RUN-PATH-001") is None
    results.append(Result("PATH-001-SYMLINK-ESCAPE", "CONTROL_INTEGRITY", PASS if ok else FAIL, {"runner_exit_code": proc.returncode, "stderr": proc.stderr.decode("utf-8", "replace")}))
    # Unknown operation/operator are schema-invalid and must execute zero steps.
    for offset, vector_id in enumerate(("PLAN-001-UNKNOWN-OPERATION", "PLAN-002-UNKNOWN-OPERATOR"), start=6):
        root = make_repo(base, runner, schema_dir, f"control-{offset:02d}")
        plan_path, contract_path, anchors = make_plan(root, {"operation": "git.head"}, {"operator": "exists", "actual": {"ref": "/steps/0/observation"}}, plan_id=f"VP-PLAN-{offset:03d}", contract_id=f"CTR-PLAN-{offset:03d}")
        plan_obj = read_json(plan_path)
        if vector_id.endswith("OPERATION"):
            plan_obj["steps"][0]["operation"] = "repository.do_whatever"
        else:
            plan_obj["assertions"]["AC-001"]["expression"] = {"operator": "approximately_equal", "actual": {"literal": 1}, "expected": {"literal": 1}}
        write_json(plan_path, plan_obj)
        anchors["plan"] = sha256_file(plan_path)
        proc = run_runner(root, runner_command(root, plan_path, contract_path, anchors, f"RUN-PLAN-{offset:03d}"))
        ok = proc.returncode == 10 and load_manifest(root, f"RUN-PLAN-{offset:03d}") is None
        results.append(Result(vector_id, "CONTROL_INTEGRITY", PASS if ok else FAIL, {"runner_exit_code": proc.returncode, "stderr": proc.stderr.decode("utf-8", "replace")}))
    return results


def provenance_suite(base: pathlib.Path, runner: pathlib.Path, schema_dir: pathlib.Path) -> list[Result]:
    results: list[Result] = []
    # Raw digest.
    root = make_repo(base, runner, schema_dir, "provenance-01")
    step = process_step('import sys;print("RAW_STDOUT");print("RAW_STDERR",file=sys.stderr)', name="prov1")
    plan, contract, anchors = make_plan(root, step, eq_exit_zero(), plan_id="VP-PROV-001", contract_id="CTR-PROV-001")
    proc = run_runner(root, runner_command(root, plan, contract, anchors, "RUN-PROV-001"))
    manifest = load_manifest(root, "RUN-PROV-001")
    ok = proc.returncode == 0 and manifest is not None
    details: dict[str, Any] = {"runner_exit_code": proc.returncode}
    if manifest is not None:
        package = root / ".ai-control" / "verification-package" / "RUN-PROV-001"
        for field in ("stdout", "stderr"):
            meta = manifest["steps"][0][field]
            actual = sha256_file(package / meta["path"])
            ok = ok and actual == meta["sha256"]
            details[field] = {"manifest": meta["sha256"], "recalculated": actual}
    results.append(Result("PROV-001-RAW-DIGEST", "PROVENANCE", PASS if ok else FAIL, details))
    # Narrative cannot pass.
    root = make_repo(base, runner, schema_dir, "provenance-02")
    step = process_step('import sys;print("AC-001 PASS");sys.exit(1)', name="prov2")
    plan, contract, anchors = make_plan(root, step, eq_exit_zero(), plan_id="VP-PROV-002", contract_id="CTR-PROV-002")
    proc = run_runner(root, runner_command(root, plan, contract, anchors, "RUN-PROV-002"))
    manifest = load_manifest(root, "RUN-PROV-002")
    ok = proc.returncode == 0 and manifest is not None and manifest["steps"][0]["exit_code"] == 1 and manifest["assertions"]["AC-001"]["status"] == "FAIL"
    results.append(Result("PROV-002-NARRATIVE-CANNOT-PASS", "PROVENANCE", PASS if ok else FAIL, {"runner_exit_code": proc.returncode, "manifest_assertion": manifest["assertions"]["AC-001"] if manifest else None}))
    # Runtime type mismatch through structured JSON parser.
    root = make_repo(base, runner, schema_dir, "provenance-03")
    step = process_step('import json;print(json.dumps({"value":"0"}))', name="prov3", parser="json")
    assertion = {"operator": "lt", "actual": {"ref": "/steps/0/observation/value"}, "expected": {"literal": 1}}
    plan, contract, anchors = make_plan(root, step, assertion, plan_id="VP-ASSRT-001", contract_id="CTR-ASSRT-001")
    proc = run_runner(root, runner_command(root, plan, contract, anchors, "RUN-ASSRT-001"))
    manifest = load_manifest(root, "RUN-ASSRT-001")
    ok = proc.returncode == 0 and manifest is not None and manifest["assertions"]["AC-001"]["status"] == "NOT_VERIFIED" and manifest["assertions"]["AC-001"]["reason_code"] == "TYPE_MISMATCH"
    results.append(Result("ASSRT-001-RUNTIME-TYPE-MISMATCH", "PROVENANCE", PASS if ok else FAIL, {"runner_exit_code": proc.returncode, "assertion": manifest["assertions"]["AC-001"] if manifest else None}))
    return results


def manifest_schema_valid(manifest: dict[str, Any], schema_dir: pathlib.Path) -> tuple[bool, str | None]:
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except Exception as exc:
        raise HarnessPreconditionError(f"harness jsonschema unavailable: {exc}") from exc
    schema = read_json(schema_dir / "manifest.schema.json")
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        errors = sorted(validator.iter_errors(manifest), key=lambda item: list(item.absolute_path))
    except Exception as exc:
        raise HarnessPreconditionError(f"manifest schema validation setup failed: {exc}") from exc
    if errors:
        first = errors[0]
        return False, first.message
    return True, None


def crash_suite(base: pathlib.Path, runner: pathlib.Path, schema_dir: pathlib.Path) -> list[Result]:
    results: list[Result] = []
    # Kill during execution.
    root = make_repo(base, runner, schema_dir, "crash-01")
    step = process_step('import time;print("START",flush=True);time.sleep(30)', timeout=40, name="crash1")
    plan, contract, anchors = make_plan(root, step, eq_exit_zero(), plan_id="VP-CC-001", contract_id="CTR-CC-001")
    run_id = "RUN-CC-001"
    proc = subprocess.Popen(runner_command(root, plan, contract, anchors, run_id), cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"PATH": CONTROLLED_PATH, "LC_ALL": "C", "LANG": "C"}, start_new_session=True)
    temp_stdout = root / ".ai-control" / "verification-package" / ".tmp" / run_id / "raw" / "crash1.stdout"
    final_path = root / ".ai-control" / "verification-package" / run_id
    observed = False
    deadline = time.time() + 15
    while time.time() < deadline:
        if temp_stdout.is_file() and b"START" in temp_stdout.read_bytes():
            observed = True
            break
        if proc.poll() is not None:
            break
        time.sleep(0.05)
    if observed:
        os.killpg(proc.pid, signal.SIGKILL)
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait(timeout=5)
    ok = observed and not final_path.exists()
    results.append(Result("CC-001-KILL-DURING-EXECUTION", "CRASH_CONSISTENCY", PASS if ok else FAIL, {"observed_start": observed, "runner_returncode": proc.returncode, "final_path_exists": final_path.exists()}))
    # Publication syscall trace.
    strace = which_required("strace")
    root = make_repo(base, runner, schema_dir, "crash-02")
    step = {"operation": "git.head"}
    assertion = {"operator": "exists", "actual": {"ref": "/steps/0/observation"}}
    plan, contract, anchors = make_plan(root, step, assertion, plan_id="VP-CC-002", contract_id="CTR-CC-002")
    run_id = "RUN-CC-002"
    trace_base = root / "strace.log"
    command = [strace, "-ff", "-yy", "-s", "4096", "-e", "trace=rename,renameat,renameat2,openat,mkdir,write", "-o", str(trace_base), *runner_command(root, plan, contract, anchors, run_id)]
    proc2 = subprocess.run(command, cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"PATH": CONTROLLED_PATH, "LC_ALL": "C", "LANG": "C"}, timeout=30, check=False)
    traces = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in sorted(root.glob("strace.log*")))
    temp_text = f".ai-control/verification-package/.tmp/{run_id}"
    final_text = f".ai-control/verification-package/{run_id}"
    rename_lines = [line for line in traces.splitlines() if ("rename(" in line or "renameat(" in line or "renameat2(" in line) and temp_text in line and final_text in line]
    publication_index = None
    lines = traces.splitlines()
    for idx, line in enumerate(lines):
        if line in rename_lines:
            publication_index = idx
            break
    premature = []
    if publication_index is not None:
        for line in lines[:publication_index]:
            if final_text in line and any(token in line for token in ("openat(", "mkdir(", "write(")):
                premature.append(line)
    final_manifest = load_manifest(root, run_id)
    same_fs = os.stat(root / ".ai-control" / "verification-package" / ".tmp").st_dev == os.stat(root / ".ai-control" / "verification-package").st_dev
    manifest_valid = False
    manifest_error = None
    if final_manifest is not None:
        manifest_valid, manifest_error = manifest_schema_valid(final_manifest, schema_dir)
    ok2 = proc2.returncode == 0 and same_fs and len(rename_lines) == 1 and not premature and final_manifest is not None and manifest_valid
    results.append(Result("CC-002-PUBLICATION-SYSCALL", "CRASH_CONSISTENCY", PASS if ok2 else FAIL, {"runner_exit_code": proc2.returncode, "same_filesystem": same_fs, "publication_rename_count": len(rename_lines), "premature_final_path_accesses": premature[:20], "manifest_valid": manifest_valid, "manifest_error": manifest_error, "strace_stderr": proc2.stderr.decode("utf-8", "replace")}))
    return results


def calculate_ac_results(results: list[Result], map_path: pathlib.Path) -> dict[str, Any]:
    mapping = read_json(map_path)["criteria"]
    result_by_id = {item.id: item for item in results}
    # Static SA-* policy rules are represented by STATIC-RUNNER-AST plus explicit vectors.
    ac_results: dict[str, Any] = {}
    for ac_id, config in mapping.items():
        referenced: list[dict[str, Any]] = []
        statuses: list[str] = []
        for ref in config["covered_by"]:
            if ref.startswith("SA-"):
                runner_ast = result_by_id.get("STATIC-RUNNER-AST")
                status = runner_ast.status if runner_ast is not None else HARNESS_INVALID
                referenced.append({"id": ref, "status": status, "evidence": "STATIC-RUNNER-AST"})
                statuses.append(status)
            else:
                item = result_by_id.get(ref)
                status = item.status if item is not None else HARNESS_INVALID
                referenced.append({"id": ref, "status": status})
                statuses.append(status)
        if HARNESS_INVALID in statuses:
            status = HARNESS_INVALID
        elif all(item == PASS for item in statuses):
            status = PASS
        else:
            status = FAIL
        ac_results[ac_id] = {"status": status, "checks": referenced}
    return ac_results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", type=pathlib.Path, required=True)
    parser.add_argument("--schema-dir", type=pathlib.Path, required=True)
    parser.add_argument("--spec-dir", type=pathlib.Path, required=True)
    parser.add_argument("--report", type=pathlib.Path, required=True)
    parser.add_argument("--keep-workdir", action="store_true")
    args = parser.parse_args()
    runner = args.runner.resolve(strict=True)
    schema_dir = args.schema_dir.resolve(strict=True)
    spec_dir = args.spec_dir.resolve(strict=True)
    results: list[Result] = []
    preconditions: dict[str, Any] = {}
    try:
        for command in ("bash", "git", "shellcheck", "bwrap", "strace"):
            preconditions[command] = which_required(command)
        import_bashlex()
        preconditions["bashlex"] = "available"
        check_runner_python_dependencies()
        preconditions["runner_python_jsonschema"] = "available"
    except HarnessPreconditionError as exc:
        report = {
            "schema_version": "FVR-RUNNER-CONFORMANCE-REPORT-1.0",
            "verdict": HARNESS_INVALID,
            "reason": str(exc),
            "preconditions": preconditions,
            "results": [],
            "ac_results": {},
        }
        write_json(args.report, report)
        print(json.dumps(report, indent=2))
        return 2
    work = pathlib.Path(tempfile.mkdtemp(prefix="fvr-conformance-"))
    try:
        results.extend(static_suite(runner))
        results.extend(control_integrity_suite(work, runner, schema_dir))
        results.extend(sandbox_suite(work, runner, schema_dir))
        results.extend(telemetry_suite(work, runner, schema_dir))
        results.extend(provenance_suite(work, runner, schema_dir))
        results.extend(crash_suite(work, runner, schema_dir))
        ac_results = calculate_ac_results(results, spec_dir / "ac-fvr-conformance-map.json")
        if any(item.status == HARNESS_INVALID for item in results):
            verdict = HARNESS_INVALID
        elif all(item.status == PASS for item in results) and all(value["status"] == PASS for value in ac_results.values()):
            verdict = "CONFORMANT"
        else:
            verdict = "NON_CONFORMANT"
        report = {
            "schema_version": "FVR-RUNNER-CONFORMANCE-REPORT-1.0",
            "verdict": verdict,
            "runner_sha256": sha256_file(runner),
            "preconditions": preconditions,
            "results": [item.as_dict() for item in results],
            "ac_results": ac_results,
        }
        write_json(args.report, report)
        print(json.dumps(report, indent=2))
        return 0 if verdict == "CONFORMANT" else 1
    except HarnessPreconditionError as exc:
        report = {
            "schema_version": "FVR-RUNNER-CONFORMANCE-REPORT-1.0",
            "verdict": HARNESS_INVALID,
            "reason": str(exc),
            "preconditions": preconditions,
            "results": [item.as_dict() for item in results],
            "ac_results": {},
        }
        write_json(args.report, report)
        print(json.dumps(report, indent=2))
        return 2
    finally:
        if args.keep_workdir:
            print(f"workdir preserved: {work}", file=sys.stderr)
        else:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
