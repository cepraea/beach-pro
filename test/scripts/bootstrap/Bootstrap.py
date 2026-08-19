#!/usr/bin/env python3

import argparse
import json
import re
import subprocess
import sys
import tomllib
import hashlib
import tempfile
from dataclasses import dataclass, field, asdict
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Literal, Optional, Tuple, Type, Set

REPO_CANONICAL_ID = "cepraea/beach-pro"
ENTRYPOINT_FILES = ["AGENT_POLICY.md", "CLAUDE.md", "AGENTS.md"]


@dataclass(frozen=True)
class ChangedPath:
    path: str
    git_status: str
    tracked: bool
    staged: bool
    unstaged: bool
    untracked: bool
    new_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        # Converts the dataclass instance to a dictionary
        return asdict(self)


@dataclass(frozen=True)
class InventoryItem:
    path: str
    kind: Literal["file", "dir"]
    tracked: bool
    size_bytes: int
    sha256: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)



@dataclass(frozen=True)
class CheckResult:
    check_id: str
    result: Literal["PASS", "FAIL"]
    expected: Any
    observed: Any
    reason_codes: Tuple[str, ...] = field(default_factory=tuple)
    evidence: Tuple[Any, ...] = field(default_factory=tuple)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "check_id": self.check_id,
            "result": self.result,
            "expected": self.expected,
            "observed": self.observed,
            "reason_codes": list(self.reason_codes),
            "evidence": list(self.evidence),
        }


class Check:
    """Base class for a single bootstrap check."""
    check_id: str = "B00-BASE-CHECK"

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def run(self) -> CheckResult:
        raise NotImplementedError


class RepositoryObserver(Check):
    """B00 — Repository Identity"""
    check_id = "B00-REPOSITORY-IDENTITY"

    def run(self) -> CheckResult:
        try:
            remote_url_raw = subprocess.check_output(
                ['git', 'remote', 'get-url', 'origin'],
                text=True, cwd=self.repo_root, stderr=subprocess.PIPE
            ).strip()

            match = re.search(r'github\.com[/:]([^/]+/[^/]+?)(\.git)?$', remote_url_raw)
            if not match:
                return CheckResult(self.check_id, "FAIL", REPO_CANONICAL_ID, remote_url_raw, ("REMOTE_UNRESOLVABLE",))

            observed_id = match.group(1)
            if observed_id == REPO_CANONICAL_ID:
                return CheckResult(self.check_id, "PASS", REPO_CANONICAL_ID, observed_id)
            else:
                return CheckResult(self.check_id, "FAIL", REPO_CANONICAL_ID, observed_id, ("WRONG_REPOSITORY",))

        except subprocess.CalledProcessError as e:
            return CheckResult(self.check_id, "FAIL", REPO_CANONICAL_ID, None, ("REMOTE_UNRESOLVABLE",), (e.stderr.strip(),))
        except FileNotFoundError:
            return CheckResult(self.check_id, "FAIL", REPO_CANONICAL_ID, None, ("NOT_A_GIT_REPOSITORY",))


class EntrypointVerifier(Check):
    """B03 — Entry Points dos agentes"""
    check_id = "B03-ENTRYPOINTS"

    def run(self) -> CheckResult:
        missing_files: List[str] = []
        unreadable_files: List[str] = []
        empty_files: List[str] = []
        bootstrap_trigger_missing: List[str] = []

        for filename in ENTRYPOINT_FILES:
            f_path = self.repo_root / filename
            if not f_path.exists():
                missing_files.append(filename)
                continue
            if not f_path.is_file() or not f_path.stat().st_size > 0:
                empty_files.append(filename)
                continue
            try:
                content = f_path.read_text(encoding="utf-8")
                if filename in ("CLAUDE.md", "AGENTS.md") and "bootstrap" not in content.lower():
                     bootstrap_trigger_missing.append(filename)
            except OSError:
                unreadable_files.append(filename)

        reason_codes: List[str] = []
        if missing_files: reason_codes.append("ENTRYPOINT_MISSING")
        if empty_files: reason_codes.append("ENTRYPOINT_EMPTY")
        if unreadable_files: reason_codes.append("ENTRYPOINT_UNREADABLE")
        if bootstrap_trigger_missing: reason_codes.append("BOOTSTRAP_TRIGGER_MISSING")

        if not reason_codes:
            return CheckResult(self.check_id, "PASS", ENTRYPOINT_FILES, ENTRYPOINT_FILES)
        else:
            return CheckResult(self.check_id, "FAIL", ENTRYPOINT_FILES, {
                "missing": missing_files,
                "empty": empty_files,
                "unreadable": unreadable_files,
                "bootstrap_trigger_missing": bootstrap_trigger_missing,
            }, tuple(reason_codes))


class RoleVerifier(Check):
    """B04 — Coerência de papéis"""
    check_id = "B04-ROLE-CONSISTENCY"

    def _get_role(self, filename: str) -> Optional[str]:
        path = self.repo_root / filename
        if not path.is_file():
            return None
        content = path.read_text(encoding="utf-8")
        match = re.search(r"^\*\*Papel:\s*(EXECUTOR|REVIEWER)\*\*$", content, re.MULTILINE)
        return match.group(1) if match else None

    def run(self) -> CheckResult:
        claude_role = self._get_role("CLAUDE.md")
        codex_role = self._get_role("AGENTS.md")
        observed = {"CLAUDE.md": claude_role, "AGENTS.md": codex_role}
        expected = {"CLAUDE.md": "EXECUTOR", "AGENTS.md": "REVIEWER"}

        if claude_role == "EXECUTOR" and codex_role == "REVIEWER":
            return CheckResult(self.check_id, "PASS", expected, observed)
        else:
            return CheckResult(self.check_id, "FAIL", expected, observed, ("ROLE_CONFLICT",))


class GitAuthorityVerifier(Check):
    """B05 — Autoridade Git (Política Declarada)"""
    check_id = "B05-GIT-AUTHORITY"
    POLICY_FILE = "AGENT_POLICY.md"

    # Based on test/scripts/bootstrap/README.md section 14.1
    EXPECTED_READ_ONLY_COMMANDS = {'status', 'diff', 'log', 'show', 'rev-parse', 'ls-files'}
    EXPECTED_PRIVILEGED_COMMANDS = {
        'add', 'commit', 'push', 'pull', 'merge', 'rebase', 'cherry-pick', 'reset',
        'restore', 'checkout', 'switch', 'worktree', 'stash', 'clean', 'update-ref'
    }

    def run(self) -> CheckResult:
        policy_path = self.repo_root / self.POLICY_FILE
        if not policy_path.is_file():
            return CheckResult(self.check_id, "FAIL", f"Policy file '{self.POLICY_FILE}' exists", False, ("ENTRYPOINT_MISSING",))

        try:
            content = policy_path.read_text(encoding="utf-8")

            # Extract commands from the policy file
            permitted_match = re.search(r"PERMITIDO aos Agentes \(Inspeção - Read Only\):`([^`]+)`", content)
            prohibited_match = re.search(r"PROIBIDO aos Agentes \(Mutações - Exclusivo Humano\):.+?\(([^)]+)\)", content)

            observed_read_only = set(permitted_match.group(1).replace('`', '').split(', ')) if permitted_match else set()
            observed_privileged = set(prohibited_match.group(1).replace('`', '').replace(', etc.', '').split(', ')) if prohibited_match else set()

            missing_read_only = self.EXPECTED_READ_ONLY_COMMANDS - observed_read_only
            missing_privileged = self.EXPECTED_PRIVILEGED_COMMANDS - observed_privileged

            if not missing_read_only and not missing_privileged:
                return CheckResult(self.check_id, "PASS", "All expected Git commands are declared in the policy", {"read_only": sorted(list(observed_read_only)), "privileged": sorted(list(observed_privileged))})
            else:
                return CheckResult(self.check_id, "FAIL", "All expected Git commands are declared in the policy", {"missing_read_only": sorted(list(missing_read_only)), "missing_privileged": sorted(list(missing_privileged))}, ("AUTHORITY_POLICY_MISMATCH",))

        except OSError as e:
            return CheckResult(self.check_id, "FAIL", "Policy file is readable", False, ("FILE_READ_ERROR",), (str(e),))

class WorkingTreeObserver(Check):
    """B01 — Working Tree Observation & B02 — Changed Path Discovery"""
    check_id = "B01-B02-WORKING-TREE-OBSERVATION-AND-CHANGED-PATH-DISCOVERY"

    def run(self) -> CheckResult:
        try:
            # git status --porcelain=v1 --untracked-files=all
            # Output format: XY PATH or XY PATH -> PATH
            # X = index status, Y = working tree status
            # Examples:
            # M  file.txt (modified in index)
            #  M file.txt (modified in working tree)
            # AM file.txt (added to index, modified in working tree)
            # ?? untracked.txt (untracked)
            git_status_output = subprocess.check_output(
                ['git', 'status', '--porcelain=v1', '--untracked-files=all'],
                text=True, cwd=self.repo_root, stderr=subprocess.PIPE
            ).strip()

            changed_paths: List[Dict[str, Any]] = []
            for line in git_status_output.splitlines():
                if not line:
                    continue

                status_codes = line[0:2]
                path_info = line[3:]

                path = None
                new_path = None
                if "->" in path_info: # Renamed file
                    parts = path_info.split("->")
                    path = parts[0].strip()
                    new_path = parts[1].strip()
                else:
                    path = path_info.strip()

                staged_status = status_codes[0]
                unstaged_status = status_codes[1]

                is_untracked = status_codes == "??"
                is_tracked = not is_untracked

                is_staged = staged_status != ' ' and staged_status != '?'
                is_unstaged = unstaged_status != ' ' and unstaged_status != '?'

                changed_path_obj = ChangedPath(
                    path=path,
                    new_path=new_path,
                    git_status=status_codes,
                    tracked=is_tracked,
                    staged=is_staged,
                    unstaged=is_unstaged,
                    untracked=is_untracked,
                )
                changed_paths.append(changed_path_obj.to_dict())

            # As per B01.4, DIRTY_WORKTREE ≠ AUTOMATIC_FAIL. This check always passes if it can observe.
            return CheckResult(
                self.check_id, "PASS", "Observation of working tree state", changed_paths, evidence=(git_status_output,)
            )

        except subprocess.CalledProcessError as e:
            return CheckResult(self.check_id, "FAIL", "Successful observation of working tree state", None, ("GIT_STATUS_ERROR",), (e.stderr.strip(),))
        except FileNotFoundError:
            return CheckResult(self.check_id, "FAIL", "Git command available", None, ("GIT_COMMAND_NOT_FOUND",), ("Git command not found. Is Git installed and in PATH?",))

class ControlPlaneVerifier(Check):
    """B08 — Control Plane"""
    check_id = "B08-CONTROL-PLANE"
    CONTROL_PLANE_DIR = ".ai/control"
    CONTROL_PLANE_FILES = [
        "task-proposal.schema.json",
        "validate-task-proposal.mjs",
        "verification-plan.schema.json",
    ]

    def run(self) -> CheckResult:
        reason_codes: List[str] = []
        evidence: List[str] = []
        control_plane_path = self.repo_root / self.CONTROL_PLANE_DIR

        # Check for Node.js runtime
        try:
            node_version_proc = subprocess.run(['node', '--version'], capture_output=True, text=True, check=True, encoding='utf-8')
            evidence.append(f"Node.js runtime found: {node_version_proc.stdout.strip()}")
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            reason_codes.append("VALIDATOR_UNAVAILABLE")
            evidence.append(f"Node.js runtime not found or failed: {e}")

        for filename in self.CONTROL_PLANE_FILES:
            file_path = control_plane_path / filename
            if not file_path.is_file():
                reason_codes.append("CONTROL_PLANE_MISSING")
                evidence.append(f"Missing control plane file: {self.CONTROL_PLANE_DIR}/{filename}")
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
                if filename.endswith(".json"):
                    data = json.loads(content)
                    if filename == "task-proposal.schema.json" and data.get("schema_version") != "2.0":
                        reason_codes.append("CONTROL_PLANE_INVALID")
                        evidence.append(f"Unsupported schema version in {filename}: expected 2.0, got {data.get('schema_version')}")
                elif filename.endswith(".mjs") and "VALIDATOR_UNAVAILABLE" not in reason_codes:
                    # Check syntax of the validator script
                    syntax_check_proc = subprocess.run(['node', '--check', str(file_path)], capture_output=True, text=True, check=True, encoding='utf-8')
                    evidence.append(f"Validator script syntax OK: {filename}")

            except json.JSONDecodeError as e:
                reason_codes.append("CONTROL_PLANE_INVALID_JSON")
                evidence.append(f"Invalid JSON in {filename}: {e}")
            except subprocess.CalledProcessError as e:
                reason_codes.append("VALIDATOR_SYNTAX_ERROR")
                evidence.append(f"Syntax error in validator {filename}: {e.stderr}")
            except OSError as e:
                reason_codes.append("FILE_READ_ERROR")
                evidence.append(f"Could not read file {filename}: {e}")

        if reason_codes:
            return CheckResult(self.check_id, "FAIL", "Control plane is valid and available", {"files_checked": self.CONTROL_PLANE_FILES}, tuple(reason_codes), tuple(evidence))
        return CheckResult(self.check_id, "PASS", "Control plane is valid and available", {"files_checked": self.CONTROL_PLANE_FILES})

class VerifierSelfTester(Check):
    """B13 — Verifier Self-Tests for Task Proposal Validator"""
    check_id = "B13-VERIFIER-SELF-TEST"

    def __init__(self, repo_root: Path, control_plane_check: Optional[CheckResult]):
        super().__init__(repo_root)
        self.control_plane_check = control_plane_check

    def _run_validator(self, validator_path: Path, fixture_path: Path) -> subprocess.CompletedProcess:
        """Executes the Node.js validator against a given fixture file."""
        return subprocess.run(
            ['node', str(validator_path), str(fixture_path)],
            capture_output=True, text=True, encoding='utf-8'
        )

    def run(self) -> CheckResult:
        # This check depends on the control plane being available.
        if not self.control_plane_check or self.control_plane_check.result == "FAIL":
            return CheckResult(self.check_id, "FAIL", "Validator self-test capability", "Control plane check failed or was not run", ("DEPENDENCY_FAILED",))

        validator_path = self.repo_root / ".ai/control/validate-task-proposal.mjs"
        known_good_path = self.repo_root / ".ai/task-proposal.example.json"

        if not validator_path.is_file() or not known_good_path.is_file():
            return CheckResult(self.check_id, "FAIL", "Validator and known-good fixture exist", False, ("CONTROL_PLANE_MISSING",))

        reason_codes: List[str] = []
        evidence: List[str] = []

        try:
            with tempfile.TemporaryDirectory(prefix="cepraea-bootstrap-") as tmpdir:
                temp_dir_path = Path(tmpdir)

                # 1. Test with KNOWN_GOOD fixture
                proc_good = self._run_validator(validator_path, known_good_path)
                if proc_good.returncode != 0:
                    reason_codes.append("VERIFIER_FALSE_NEGATIVE")
                    evidence.append(f"Known-good fixture was REJECTED. Stderr: {proc_good.stderr.strip()}")
                else:
                    evidence.append("Known-good fixture was ACCEPTED as expected.")

                # 2. Create and test with KNOWN_BAD fixture
                known_bad_fixture_path = temp_dir_path / "known-bad-proposal.json"
                try:
                    good_data = json.loads(known_good_path.read_text(encoding="utf-8"))
                    del good_data['task_id'] # Mutate by removing a required field
                    known_bad_fixture_path.write_text(json.dumps(good_data), encoding="utf-8")
                except (KeyError, json.JSONDecodeError, OSError) as e:
                     return CheckResult(self.check_id, "FAIL", "Creation of known-bad fixture", f"Failed to create fixture: {e}", ("FIXTURE_CREATION_FAILED",))

                proc_bad = self._run_validator(validator_path, known_bad_fixture_path)
                if proc_bad.returncode == 0:
                    reason_codes.append("VERIFIER_FALSE_POSITIVE")
                    evidence.append(f"Known-bad fixture was ACCEPTED. Stdout: {proc_bad.stdout.strip()}")
                else:
                    evidence.append("Known-bad fixture was REJECTED as expected.")

        except (OSError, subprocess.SubprocessError) as e:
            return CheckResult(self.check_id, "FAIL", "Validator self-test execution", f"An error occurred: {e}", ("SELF_TEST_EXECUTION_ERROR",))

        if reason_codes:
            return CheckResult(self.check_id, "FAIL", "Known-good accepted and known-bad rejected", "One or more self-tests failed", tuple(reason_codes), tuple(evidence))
        return CheckResult(self.check_id, "PASS", "Known-good accepted and known-bad rejected", "All self-tests passed", evidence=tuple(evidence))

class RunbookCatalogVerifier(Check):
    """B09 — Runbook Catalog"""
    check_id = "B09-RUNBOOK-CATALOG"
    CATALOG_FILE = "runbooks/README.md"

    def run(self) -> CheckResult:
        catalog_path = self.repo_root / self.CATALOG_FILE
        if not catalog_path.is_file():
            return CheckResult(self.check_id, "FAIL", f"Runbook catalog '{self.CATALOG_FILE}' exists", False, ("RUNBOOK_CATALOG_MISSING",))

        try:
            content = catalog_path.read_text(encoding="utf-8")
            # Regex to find all markdown links like [text](./path/to/file.md)
            runbook_paths_relative = re.findall(r'\[.*?\]\(\.(.*?)\)', content)

            dangling_paths: List[str] = []
            for rel_path in runbook_paths_relative:
                # The link is relative to the runbooks/ dir, so we join it
                full_path = self.repo_root / "runbooks" / rel_path.lstrip('/')
                if not full_path.is_file():
                    dangling_paths.append(f"runbooks/{rel_path.lstrip('/')}")

            if dangling_paths:
                return CheckResult(self.check_id, "FAIL", "All declared runbooks resolve", {"dangling_paths": dangling_paths}, ("RUNBOOK_REFERENCE_BROKEN",))

            return CheckResult(self.check_id, "PASS", "All declared runbooks resolve", {"found_runbooks": len(runbook_paths_relative)})

        except OSError as e:
            return CheckResult(self.check_id, "FAIL", "Runbook catalog is readable", False, ("FILE_READ_ERROR",), (str(e),))

class ClaudeConfigVerifier(Check):
    """B10 — Configuração Claude Code"""
    check_id = "B10-CLAUDE-CONFIGURATION"
    SETTINGS_FILE = ".devcontainer/control-plane/claude-managed-settings.json"
    MCP_FILE = ".devcontainer/control-plane/claude-managed-mcp.json"

    CRITICAL_DENY_RULES = {
        'sudo', 'docker', 'git add', 'git commit', 'git push', 'git pull',
        'git merge', 'git rebase', 'git cherry-pick', 'git reset', 'git restore',
        'git checkout', 'git switch', 'git worktree', 'git clean', 'git stash',
        'git update-ref'
    }

    def run(self) -> CheckResult:
        reason_codes: List[str] = []
        evidence: List[str] = []
        
        settings_path = self.repo_root / self.SETTINGS_FILE
        mcp_path = self.repo_root / self.MCP_FILE

        # Check 1: claude-managed-settings.json
        if not settings_path.is_file():
            reason_codes.append("CLAUDE_CONFIG_MISSING")
            evidence.append(f"Missing settings file: {self.SETTINGS_FILE}")
        else:
            try:
                settings_data = json.loads(settings_path.read_text(encoding="utf-8"))
                
                for key, expected_value in [("allowManagedHooksOnly", True), ("allowManagedPermissionRulesOnly", True), ("disableBypassPermissionsMode", True)]:
                    if settings_data.get(key) is not expected_value:
                        reason_codes.append("CLAUDE_CONFIG_INVALID")
                        evidence.append(f"Expected '{key}' to be {expected_value} in {self.SETTINGS_FILE}, but was {settings_data.get(key)}")

                # Verify critical deny rules
                permission_rules = settings_data.get("permissionRules", [])
                denied_commands = {rule.get("command") for rule in permission_rules if rule.get("effect") == "deny"}
                missing_denials = self.CRITICAL_DENY_RULES - denied_commands
                if missing_denials:
                    reason_codes.append("CLAUDE_CRITICAL_DENY_MISSING")
                    evidence.append(f"Missing critical deny rules for commands: {sorted(list(missing_denials))}")

            except (json.JSONDecodeError, OSError) as e:
                reason_codes.append("CLAUDE_CONFIG_INVALID_JSON")
                evidence.append(f"Could not parse {self.SETTINGS_FILE}: {e}")

        if reason_codes:
            return CheckResult(self.check_id, "FAIL", "Claude configuration is valid and secure", {"checked_files": [self.SETTINGS_FILE, self.MCP_FILE]}, tuple(reason_codes), tuple(evidence))
        return CheckResult(self.check_id, "PASS", "Claude configuration is valid and secure", {"checked_files": [self.SETTINGS_FILE, self.MCP_FILE]})

class CodexConfigVerifier(Check):
    """B11 — Configuração Codex Reviewer"""
    check_id = "B11-CODEX-CONFIGURATION"
    CONFIG_FILE = ".codex/config.toml"
    REQUIREMENTS_FILE = ".devcontainer/control-plane/codex-requirements.toml"

    def run(self) -> CheckResult:
        reason_codes: List[str] = []
        evidence: List[str] = []

        config_path = self.repo_root / self.CONFIG_FILE
        reqs_path = self.repo_root / self.REQUIREMENTS_FILE

        # Check 1: .codex/config.toml
        if not config_path.is_file():
            reason_codes.append("CODEX_CONFIG_MISSING")
            evidence.append(f"Missing config file: {self.CONFIG_FILE}")
        else:
            try:
                config_data = tomllib.loads(config_path.read_text(encoding="utf-8"))
                if config_data.get('approval_policy') != 'never':
                    reason_codes.append("CODEX_CONFIG_INVALID")
                    evidence.append(f"Expected 'approval_policy' to be 'never', but was '{config_data.get('approval_policy')}'")
                if config_data.get('permissions', {}).get('cepraea-review', {}).get('filesystem', {}).get(':workspace_roots', {}).get('.') != 'read':
                    reason_codes.append("CODEX_CONFIG_INVALID")
                    evidence.append("Expected workspace root filesystem permission to be 'read'.")
                if config_data.get('permissions', {}).get('cepraea-review', {}).get('network', {}).get('enabled') is not False:
                    reason_codes.append("CODEX_CONFIG_INVALID")
                    evidence.append("Expected network to be disabled for cepraea-review profile.")
            except (tomllib.TOMLDecodeError, OSError) as e:
                reason_codes.append("CODEX_CONFIG_INVALID_TOML")
                evidence.append(f"Could not parse {self.CONFIG_FILE}: {e}")

        # Check 2: codex-requirements.toml (existence and validity)
        if not reqs_path.is_file():
            reason_codes.append("CODEX_CONFIG_MISSING")
            evidence.append(f"Missing requirements file: {self.REQUIREMENTS_FILE}")

        if reason_codes:
            return CheckResult(self.check_id, "FAIL", "Codex configuration is valid and secure", {"checked_files": [self.CONFIG_FILE, self.REQUIREMENTS_FILE]}, tuple(reason_codes), tuple(evidence))
        return CheckResult(self.check_id, "PASS", "Codex configuration is valid and secure", {"checked_files": [self.CONFIG_FILE, self.REQUIREMENTS_FILE]})

class DevContainerVerifier(Check):
    """B12 — Dev Container e enforcement structure"""
    check_id = "B12-DEVCONTAINER-STRUCTURE"
    DEVCONTAINER_DIR = ".devcontainer"
    REQUIRED_PATHS = [
        "Dockerfile",
        "devcontainer.json",
        "control-plane/",
        "guards/",
        "reviewer/",
        "scripts/",
    ]

    def run(self) -> CheckResult:
        reason_codes: List[str] = []
        evidence: List[str] = []
        devcontainer_root = self.repo_root / self.DEVCONTAINER_DIR

        if not devcontainer_root.is_dir():
            return CheckResult(self.check_id, "FAIL", "'.devcontainer' directory exists", False, ("DEVCONTAINER_CONFIG_MISSING",), (f"Base directory {self.DEVCONTAINER_DIR} not found.",))

        # Check for required paths' existence
        for rel_path_str in self.REQUIRED_PATHS:
            path = devcontainer_root / rel_path_str
            if not path.exists():
                reason_codes.append("DEVCONTAINER_CONFIG_MISSING")
                evidence.append(f"Missing required path in .devcontainer: {rel_path_str}")

        # Validate devcontainer.json structure and references
        devcontainer_json_path = devcontainer_root / "devcontainer.json"
        if devcontainer_json_path.is_file():
            try:
                devcontainer_data = json.loads(devcontainer_json_path.read_text(encoding="utf-8"))
                # Check that referenced files in mounts exist
                for mount in devcontainer_data.get("mounts", []):
                    if "source=${localWorkspaceFolder}/" in mount:
                        source_path_str = mount.split("source=${localWorkspaceFolder}/")[1].split(',')[0]
                        if not (self.repo_root / source_path_str).exists():
                            reason_codes.append("DEVCONTAINER_DANGLING_REFERENCE")
                            evidence.append(f"Mount source path does not exist: {source_path_str}")
            except (json.JSONDecodeError, OSError) as e:
                reason_codes.append("DEVCONTAINER_CONFIG_INVALID")
                evidence.append(f"Could not parse devcontainer.json: {e}")

        if reason_codes:
            return CheckResult(self.check_id, "FAIL", "Dev Container structure is valid", {"checked_paths": self.REQUIRED_PATHS}, tuple(reason_codes), tuple(evidence))
        return CheckResult(self.check_id, "PASS", "Dev Container structure is valid", {"checked_paths": self.REQUIRED_PATHS})

class PhysicalInventoryBuilder(Check):
    """B06 — Inventário físico"""
    check_id = "B06-PHYSICAL-INVENTORY"

    def run(self) -> CheckResult:
        inventory: List[InventoryItem] = []
        reason_codes: List[str] = []
        evidence: List[str] = []

        try:
            # Get tracked files using git ls-files -z for null-terminated output
            tracked_files_output = subprocess.check_output(
                ['git', 'ls-files', '-z'],
                text=True, cwd=self.repo_root, stderr=subprocess.PIPE, encoding="utf-8"
            ).strip('\0')
            tracked_paths_str = tracked_files_output.split('\0') if tracked_files_output else []

            # Collect all unique directory paths from tracked files
            tracked_dirs: Set[str] = set()
            for p_str in tracked_paths_str:
                current_path = PurePosixPath(p_str)
                while str(current_path) != '.' and str(current_path.parent) != '.':
                    current_path = current_path.parent
                    if str(current_path) != '.':
                        tracked_dirs.add(str(current_path))

            # Add files to inventory
            for p_str in sorted(tracked_paths_str):
                file_path = self.repo_root / p_str
                if file_path.is_file():
                    try:
                        file_bytes = file_path.read_bytes()
                        sha256_hash = hashlib.sha256(file_bytes).hexdigest()
                        inventory.append(InventoryItem(
                            path=p_str,
                            kind="file",
                            tracked=True,
                            size_bytes=file_path.stat().st_size,
                            sha256=sha256_hash
                        ))
                    except OSError as e:
                        reason_codes.append("FILE_READ_ERROR")
                        evidence.append(f"Could not read file {p_str}: {e}")
                else:
                    # This case should ideally not happen for git ls-files output, but for robustness
                    reason_codes.append("INVENTORY_ITEM_NOT_FILE")
                    evidence.append(f"Tracked path {p_str} is not a file.")

            # Add directories to inventory
            for d_str in sorted(list(tracked_dirs)):
                inventory.append(InventoryItem(
                    path=d_str,
                    kind="dir",
                    tracked=True,
                    size_bytes=0, # Directories don't have content size in this context
                    sha256=None
                ))

            if reason_codes:
                return CheckResult(self.check_id, "FAIL", "Physical inventory built without errors", [item.to_dict() for item in inventory], tuple(reason_codes), tuple(evidence))
            else:
                return CheckResult(self.check_id, "PASS", "Physical inventory built successfully", [item.to_dict() for item in inventory])

        except subprocess.CalledProcessError as e:
            return CheckResult(self.check_id, "FAIL", "Git command available and successful", None, ("GIT_LS_FILES_ERROR",), (e.stderr.strip(),))
        except FileNotFoundError:
            return CheckResult(self.check_id, "FAIL", "Git command available", None, ("GIT_COMMAND_NOT_FOUND",), ("Git command not found. Is Git installed and in PATH?",))


@dataclass(frozen=True)
class ManifestAsset:
    path: str
    type: str
    purpose: str
    consumers: List[str]
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ManifestVerifier(Check):
    """B07 — Manifest Verification"""
    check_id = "B07-MANIFEST-VERIFICATION"
    MANIFEST_FILE = "manifest.json"
    CRITICAL_UNDECLARED_PATHS = [
        "AGENT_POLICY.md", "CLAUDE.md", "AGENTS.md", "manifest.json",
        "runbooks/README.md", ".ai/AGENT_BOOTSTRAP.md", ".ai/control/",
        ".codex/config.toml", ".devcontainer/devcontainer.json",
        ".devcontainer/control-plane/", "test/scripts/bootstrap/Bootstrap.py",
    ]

    def __init__(self, repo_root: Path, physical_inventory: List[InventoryItem]):
        super().__init__(repo_root)
        self.physical_inventory = physical_inventory
        self.inventory_paths = {item.path for item in physical_inventory}
        self.manifest_path = self.repo_root / self.MANIFEST_FILE

    def run(self) -> CheckResult:
        reason_codes: List[str] = []
        evidence: List[str] = []
        manifest_data: Optional[Dict[str, Any]] = None
        declared_assets: List[ManifestAsset] = []
        declared_paths: Set[str] = set()

        # 1. Validate JSON syntax and load manifest
        if not self.manifest_path.exists():
            return CheckResult(self.check_id, "FAIL", f"Manifest file '{self.MANIFEST_FILE}' exists", False, ("MANIFEST_MISSING",))
        if not self.manifest_path.is_file():
            return CheckResult(self.check_id, "FAIL", f"Manifest file '{self.MANIFEST_FILE}' is a file", False, ("MANIFEST_NOT_FILE",))

        try:
            manifest_data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            return CheckResult(self.check_id, "FAIL", "Manifest JSON is valid", False, ("MANIFEST_INVALID_JSON",), (str(e),))
        except OSError as e:
            return CheckResult(self.check_id, "FAIL", "Manifest file is readable", False, ("MANIFEST_READ_ERROR",), (str(e),))

        # 2. Verify minimum structure (e.g., 'assets' key)
        if not isinstance(manifest_data, dict) or "assets" not in manifest_data or not isinstance(manifest_data["assets"], list):
            return CheckResult(self.check_id, "FAIL", "Manifest has 'assets' list", False, ("MANIFEST_MALFORMED_STRUCTURE",))

        # Parse declared assets and check for duplicates
        for asset_raw in manifest_data["assets"]:
            try:
                asset = ManifestAsset(**asset_raw)
                if asset.path in declared_paths:
                    reason_codes.append("MANIFEST_DUPLICATE_PATH")
                    evidence.append(f"Duplicate path '{asset.path}' found in manifest.")
                declared_assets.append(asset)
                declared_paths.add(asset.path)
            except TypeError as e: # Catches missing required fields in ManifestAsset
                reason_codes.append("MANIFEST_ASSET_MALFORMED")
                evidence.append(f"Malformed asset entry: {asset_raw} - {e}")
            except Exception as e:
                reason_codes.append("MANIFEST_ASSET_PARSE_ERROR")
                evidence.append(f"Error parsing asset entry: {asset_raw} - {e}")

        # 3. & 4. Compare each declared asset with observed inventory
        for asset in declared_assets:
            # Check if declared path exists in physical inventory
            if asset.path not in self.inventory_paths:
                reason_codes.append("MANIFEST_DECLARED_PATH_MISSING_IN_INVENTORY")
                evidence.append(f"Manifest declares path '{asset.path}' but it's missing in physical inventory.")
                continue # Skip further checks for this asset if path doesn't exist

            # Check declared type matches observed kind (basic check)
            inventory_item = next((item for item in self.physical_inventory if item.path == asset.path), None)
            if inventory_item and asset.type == "file" and inventory_item.kind != "file":
                reason_codes.append("MANIFEST_TYPE_MISMATCH")
                evidence.append(f"Manifest declares '{asset.path}' as file, but inventory shows it as {inventory_item.kind}.")
            if inventory_item and asset.type == "dir" and inventory_item.kind != "dir":
                reason_codes.append("MANIFEST_TYPE_MISMATCH")
                evidence.append(f"Manifest declares '{asset.path}' as dir, but inventory shows it as {inventory_item.kind}.")

            # Check if asset status is permitted (e.g., "active" is generally good)
            # This is a basic check, can be expanded based on policy
            if asset.status not in ["active", "in_progress", "stub", "reference"]: # Example permitted statuses
                reason_codes.append("MANIFEST_UNPERMITTED_STATUS")
                evidence.append(f"Manifest declares '{asset.path}' with unpermitted status '{asset.status}'.")

            # Further checks like 'required consumer values are recognized' would need a list of valid consumers.
            # For now, we assume any string is a valid consumer.

        # 5. Critical undeclared artifact check
        for critical_path_str in self.CRITICAL_UNDECLARED_PATHS:
            critical_path = Path(critical_path_str)
            # Check if the critical path exists in the physical inventory
            if critical_path_str in self.inventory_paths:
                # If it exists in inventory, check if it's declared in the manifest
                if critical_path_str not in declared_paths:
                    reason_codes.append("CRITICAL_UNDECLARED_ARTIFACT")
                    evidence.append(f"Critical path '{critical_path_str}' exists in repository but is not declared in manifest.json.")
            # If it's a directory, check if any file within it is undeclared
            elif critical_path.is_dir(): # Check if it's a directory in the actual filesystem
                for item in self.physical_inventory:
                    if item.path.startswith(critical_path_str + "/") and item.path not in declared_paths:
                        reason_codes.append("CRITICAL_UNDECLARED_ARTIFACT_IN_DIR")
                        evidence.append(f"File '{item.path}' within critical directory '{critical_path_str}' is not declared in manifest.json.")


        if reason_codes:
            return CheckResult(self.check_id, "FAIL", "Manifest verification successful", {"manifest": manifest_data, "declared_assets": [a.to_dict() for a in declared_assets]}, tuple(reason_codes), tuple(evidence))
        else:
            return CheckResult(self.check_id, "PASS", "Manifest verification successful", {"manifest": manifest_data, "declared_assets": [a.to_dict() for a in declared_assets]})


class BootstrapRunner:
    def __init__(self, mode: Literal["full", "revalidate"]):
        self.mode = mode
        self.results: List[CheckResult] = []
        self.repo_root = self._find_repo_root()
        self.final_verdict: Literal["PASS", "FAIL"] = "FAIL"

    def _find_repo_root(self) -> Path:
        try:
            toplevel = subprocess.check_output(
                ['git', 'rev-parse', '--show-toplevel'],
                text=True, stderr=subprocess.PIPE
            ).strip()
            return Path(toplevel)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("FAIL: NOT_A_GIT_REPOSITORY. O script deve ser executado dentro de um repositório Git.", file=sys.stderr)
            sys.exit(2)

    def run_checks(self):
        if self.mode == 'full':
            results_by_id: Dict[str, CheckResult] = {}

            def run_and_store(check_instance: Check) -> CheckResult:
                result = check_instance.run()
                results_by_id[result.check_id] = result
                self.results.append(result)
                return result

            # Stage 1: Independent checks
            independent_checks: List[Type[Check]] = [
                RepositoryObserver,         # B00
                EntrypointVerifier,         # B03
                RoleVerifier,               # B04
                GitAuthorityVerifier,       # B05
                WorkingTreeObserver,        # B01-B02
                PhysicalInventoryBuilder,   # B06
                ControlPlaneVerifier,       # B08
                RunbookCatalogVerifier,     # B09
                ClaudeConfigVerifier,       # B10
                CodexConfigVerifier,        # B11
                DevContainerVerifier,       # B12
            ]

            for check_cls in independent_checks:
                result = run_and_store(check_cls(self.repo_root))
                if result.result == "FAIL":
                    # Critical fail-fast check
                    if result.check_id == "B00-REPOSITORY-IDENTITY":
                        return

            # Stage 2: Dependent checks
            # B13 depends on B08
            control_plane_result = results_by_id.get(ControlPlaneVerifier.check_id)
            run_and_store(VerifierSelfTester(self.repo_root, control_plane_result))

            # B07 depends on B06
            physical_inventory_result = results_by_id.get(PhysicalInventoryBuilder.check_id)
            if physical_inventory_result and physical_inventory_result.result == "PASS" and isinstance(physical_inventory_result.observed, list):
                inventory_items = [InventoryItem(**item_dict) for item_dict in physical_inventory_result.observed] # type: ignore
                manifest_verifier = ManifestVerifier(self.repo_root, inventory_items)
                run_and_store(manifest_verifier)
            else:
                # If dependency failed, ManifestVerifier fails automatically
                run_and_store(ManifestVerifier(self.repo_root, []))

        else: # revalidate
            print("Modo 'revalidate' ainda não implementado.", file=sys.stderr)
            # For revalidate, we might still want to run some checks or exit.
            # For now, it will just print the message and report an empty result set.
            # This will lead to a FAIL verdict if no checks are added.
            pass

    def report(self):
        all_passed = all(r.result == "PASS" for r in self.results)
        self.final_verdict = "PASS" if all_passed and self.results else "FAIL"

        output = {
            "schema_version": "1.0",
            "mode": self.mode,
            "repository": {
                "root": str(self.repo_root),
                # Placeholder for more repo data
            },
            "checks": [r.to_dict() for r in self.results],
            "reason_codes": list(set(code for r in self.results for code in r.reason_codes)),
            "candidate_fingerprint": None,  # Placeholder for B14
            "repository_mutations": 0, # Placeholder for B01/B02 analysis
            "verdict": self.final_verdict,
        }
        print(json.dumps(output, indent=2))

        if self.final_verdict == "FAIL":
            sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verificador de Bootstrap do Agente para o repositório CEPRAEA/beach-pro.")
    parser.add_argument(
        "mode",
        choices=["full", "revalidate"],
        help="Modo de execução: 'full' para verificação completa, 'revalidate' para verificação rápida contra baseline."
    )
    args = parser.parse_args()

    runner = BootstrapRunner(mode=args.mode)
    runner.run_checks()
    runner.report()
                    check_id=ManifestVerifier.check_id,
                    result="FAIL",
                    expected="Physical inventory available for verification",
                    observed="Physical inventory not available or failed",
                    reason_codes=("DEPENDENCY_FAILED", "PHYSICAL_INVENTORY_FAILED")
                ))
        else: # revalidate
            print("Modo 'revalidate' ainda não implementado.", file=sys.stderr)
            # For revalidate, we might still want to run some checks or exit.
            # For now, it will just print the message and report an empty result set.
            # This will lead to a FAIL verdict if no checks are added.
            pass

        # Check for repository mutation after all checks
        if self.mode == 'full': # Only check for mutation in full mode
            post_run_git_state = self._get_git_state()
            if pre_run_git_state != post_run_git_state:
                self.results.append(CheckResult(
                    check_id="BXX-NON-MUTATION-INVARIANT",
                    result="FAIL",
                    expected="Repository state to remain unchanged",
                    observed="Repository state was mutated",
                    reason_codes=("BOOTSTRAP_MUTATED_REPOSITORY",),
                    evidence=(f"Pre-run state: {pre_run_git_state}", f"Post-run state: {post_run_git_state}")
                ))
            pass

    def report(self):
        all_passed = all(r.result == "PASS" for r in self.results)
        self.final_verdict = "PASS" if all_passed and self.results else "FAIL"

        output = {
            "schema_version": "1.0",
            "mode": self.mode,
            "repository": {
                "root": str(self.repo_root),
                # Placeholder for more repo data
            },
            "checks": [r.to_dict() for r in self.results],
            "reason_codes": list(set(code for r in self.results for code in r.reason_codes)),
            "verdict": self.final_verdict,
        }
        print(json.dumps(output, indent=2))

        if self.final_verdict == "FAIL":
            sys.exit(1)
        else:
            # If all checks passed, ensure no mutation was detected
            if any(r.check_id == "BXX-NON-MUTATION-INVARIANT" and r.result == "FAIL" for r in self.results):
                sys.exit(1) # Should not happen if final_verdict is PASS, but as a safeguard

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verificador de Bootstrap do Agente para o repositório CEPRAEA/beach-pro.")
    parser.add_argument(
        "mode",
        choices=["full", "revalidate"],
        help="Modo de execução: 'full' para verificação completa, 'revalidate' para verificação rápida contra baseline."
    )
    args = parser.parse_args()

    runner = BootstrapRunner(mode=args.mode)
    runner.run_checks()
    runner.report()
