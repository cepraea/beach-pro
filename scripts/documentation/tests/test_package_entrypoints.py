"""Protect the validator's two-stage migration from module to package."""

from __future__ import annotations

from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_INIT = REPOSITORY_ROOT / "scripts/__init__.py"
DOCUMENTATION_ROOT = REPOSITORY_ROOT / "scripts/documentation"
DOCUMENTATION_INIT = DOCUMENTATION_ROOT / "__init__.py"
LEGACY_ENTRYPOINT = DOCUMENTATION_ROOT / "validate_documentation.py"
PACKAGE_ROOT = DOCUMENTATION_ROOT / "validate_documentation"
PACKAGE_INIT = PACKAGE_ROOT / "__init__.py"
PACKAGE_MAIN = PACKAGE_ROOT / "__main__.py"
PACKAGE_MAP = PACKAGE_ROOT / "MAPA-VALIDADOR-DOC.md"
LEGACY_MAP = REPOSITORY_ROOT / ".inicio/MAPA-VALIDADOR-DOC.md"
PACKAGE_README = PACKAGE_ROOT / "README.md"
OPERATIONAL_README = REPOSITORY_ROOT / "docs/README.md"
WORKFLOW = REPOSITORY_ROOT / "docs/registry/workflow-documentacao.yaml"
REGISTRY = REPOSITORY_ROOT / "docs/registry/registro-documentos.yaml"
PYRIGHT_CONFIG = REPOSITORY_ROOT / "pyrightconfig.json"
HISTORICAL_GATE_ROOT = REPOSITORY_ROOT / "docs/evidence/gates"
LEGACY_REFERENCE = "scripts/documentation/validate_documentation.py"
MODULE_NAME = "scripts.documentation.validate_documentation"

from scripts.documentation import validate_documentation as validator
from scripts.documentation.validate_documentation import (
    approvals as approvals_module,
    config,
    contracts as contracts_module,
    front_matter as front_matter_module,
    ingestion as ingestion_module,
    instances as instances_module,
    links as links_module,
    provenance as provenance_module,
    registry as registry_module,
    reporter as reporter_module,
    workflow as workflow_module,
)
from scripts.documentation.validate_documentation.gates import (
    g_arch as g_arch_module,
    g0 as g0_module,
)


class PackageLayoutTests(unittest.TestCase):
    """Verify that the package is the implementation, not a parallel copy."""

    def test_module_entrypoint_exists(self) -> None:
        spec = importlib.util.find_spec(
            "scripts.documentation.validate_documentation"
        )

        if spec is None:
            self.fail("validator module cannot be resolved")
        self.assertTrue(SCRIPTS_INIT.is_file())
        self.assertTrue(DOCUMENTATION_INIT.is_file())
        self.assertEqual(PACKAGE_INIT, Path(spec.origin or ""))
        self.assertTrue(PACKAGE_MAIN.is_file())
        self.assertEqual(MODULE_NAME, validator.__name__)
        self.assertIs(validator, sys.modules[MODULE_NAME])
        self.assertNotIn("validate_documentation", sys.modules)

    def test_package_exports_main(self) -> None:
        self.assertTrue(callable(validator.main))
        self.assertIs(validator.Reporter, reporter_module.Reporter)
        self.assertIs(validator.load_json, contracts_module.load_json)
        self.assertIs(
            validator.validate_schema_definition,
            contracts_module.validate_schema_definition,
        )
        self.assertIs(
            validator.schema_validation_errors,
            contracts_module.schema_validation_errors,
        )
        self.assertIs(
            validator.validate_contract_schemas,
            contracts_module.validate_contract_schemas,
        )
        self.assertIs(
            validator.validate_yaml_instance,
            contracts_module.validate_yaml_instance,
        )
        self.assertIs(validator.valid_name, registry_module.valid_name)
        self.assertIs(
            validator.validate_top_level,
            registry_module.validate_top_level,
        )
        self.assertIs(
            validator.resolve_document_version,
            registry_module.resolve_document_version,
        )
        self.assertIs(validator.validate_record, registry_module.validate_record)
        self.assertIs(
            validator.validate_uniqueness,
            registry_module.validate_uniqueness,
        )
        self.assertIs(validator.managed_files, registry_module.managed_files)
        self.assertIs(
            validator.validate_canonical_registry,
            registry_module.validate_canonical_registry,
        )
        self.assertIs(validator.load_registry, registry_module.load_registry)
        self.assertIs(
            validator.validate_registry_integrity,
            registry_module.validate_registry_integrity,
        )
        self.assertIs(
            validator.validate_workflow_references,
            workflow_module.validate_workflow_references,
        )
        self.assertIs(
            validator.validate_approval_cross_references,
            approvals_module.validate_approval_cross_references,
        )
        self.assertIs(
            validator.validate_provenance_packages,
            provenance_module.validate_provenance_packages,
        )
        self.assertIs(
            validator.ingestion_records,
            ingestion_module.ingestion_records,
        )
        self.assertIs(
            validator.validate_ingestion_consistency,
            ingestion_module.validate_ingestion_consistency,
        )
        self.assertIs(
            validator.validate_document_instances,
            instances_module.validate_document_instances,
        )
        self.assertIs(
            validator.validate_workflow_instance,
            instances_module.validate_workflow_instance,
        )
        self.assertIs(
            validator.validate_gate_result_instances,
            instances_module.validate_gate_result_instances,
        )
        self.assertIs(
            validator.validate_evidence_instances,
            instances_module.validate_evidence_instances,
        )
        self.assertIs(
            validator.validate_instances,
            instances_module.validate_instances,
        )
        self.assertIs(
            validator.parse_front_matter,
            front_matter_module.parse_front_matter,
        )
        self.assertIs(
            validator.validate_governed,
            front_matter_module.validate_governed,
        )
        self.assertIs(
            validator.validate_feature_spec,
            front_matter_module.validate_feature_spec,
        )
        self.assertIs(
            validator.normalize_link_target,
            links_module.normalize_link_target,
        )
        self.assertIs(
            validator.validate_links,
            links_module.validate_links,
        )
        self.assertIs(validator.validate_garch, g_arch_module.validate_garch)
        self.assertIs(validator.validate_g0, g0_module.validate_g0)

    def test_package_workspace_root_is_repository_root(self) -> None:
        self.assertEqual(REPOSITORY_ROOT, config.WORKSPACE_ROOT)

    def test_legacy_entrypoint_is_removed(self) -> None:
        self.assertTrue(PACKAGE_INIT.is_file())
        self.assertFalse(LEGACY_ENTRYPOINT.exists())

    def test_maintenance_map_is_colocated_with_package(self) -> None:
        self.assertTrue(PACKAGE_MAP.is_file())
        self.assertFalse(LEGACY_MAP.exists())

    def test_package_readme_documents_tests(self) -> None:
        readme = PACKAGE_README.read_text(encoding="utf-8")

        self.assertIn("test_package_entrypoints.py", readme)
        self.assertIn(
            "scripts.documentation.tests.test_package_entrypoints",
            readme,
        )


class EntrypointBehaviorTests(unittest.TestCase):
    """Prove the package remains the only operational entrypoint."""

    @staticmethod
    def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *arguments],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_module_entrypoint_operates(self) -> None:
        package = self._run(
            "-m",
            MODULE_NAME,
            "--help",
        )

        self.assertEqual(0, package.returncode)
        self.assertIn("usage:", package.stdout)
        self.assertIn("G-ARCH", package.stdout)
        self.assertEqual("", package.stderr)

    def test_new_result_uses_package_evaluator_identity(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            status = reporter_module.Reporter().emit("yaml", "G1")

        payload = yaml.safe_load(output.getvalue())
        gate_result = payload["gate_result"]
        self.assertEqual(0, status)
        self.assertEqual(
            "scripts.documentation.validate_documentation",
            gate_result["evaluator"],
        )


class ConsumerMigrationTests(unittest.TestCase):
    """Protect all active consumers and controlled metadata after cutover."""

    def test_workflow_uses_module_entrypoint(self) -> None:
        payload = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        gates = payload["gates"]

        self.assertEqual("0.2.3", payload["workflow"]["version"])
        self.assertEqual(4, len(gates))
        for gate in gates:
            command = gate["evaluator"]["command"]
            self.assertEqual(
                ["python3", "-m", MODULE_NAME],
                command[:3],
            )
            self.assertNotIn(LEGACY_REFERENCE, command)

    def test_operational_docs_use_module_entrypoint(self) -> None:
        readme = OPERATIONAL_README.read_text(encoding="utf-8")

        self.assertIn("version: \"0.2.3\"", readme)
        self.assertIn(f"python3 -m {MODULE_NAME}", readme)
        self.assertNotIn(LEGACY_REFERENCE, readme)

    def test_no_active_reference_uses_legacy_entrypoint(self) -> None:
        active_files = [
            OPERATIONAL_README,
            WORKFLOW,
            PYRIGHT_CONFIG,
            PACKAGE_README,
            PACKAGE_MAP,
        ]

        for path in active_files:
            with self.subTest(path=path):
                self.assertNotIn(
                    LEGACY_REFERENCE,
                    path.read_text(encoding="utf-8"),
                )

    def test_historical_evaluator_references_are_preserved(self) -> None:
        result_paths = sorted(HISTORICAL_GATE_ROOT.glob("*.yaml"))
        historical_paths = [
            path
            for path in result_paths
            if f"evaluator: {LEGACY_REFERENCE}"
            in path.read_text(encoding="utf-8")
        ]

        self.assertEqual(34, len(historical_paths))

    def test_maintenance_map_has_no_active_legacy_location(self) -> None:
        self.assertFalse(LEGACY_MAP.exists())
        self.assertTrue(PACKAGE_MAP.is_file())
        self.assertNotIn(
            LEGACY_REFERENCE,
            PACKAGE_MAP.read_text(encoding="utf-8"),
        )

    def test_package_readme_documents_final_test_commands(self) -> None:
        readme = PACKAGE_README.read_text(encoding="utf-8")

        self.assertIn(
            "scripts.documentation.tests.test_package_entrypoints",
            readme,
        )
        self.assertIn("scripts/documentation/integration_tests", readme)
        self.assertNotIn(LEGACY_REFERENCE, readme)
        self.assertNotIn("Compatibilidade da Etapa 1", readme)

    def test_controlled_versions_and_hashes_match(self) -> None:
        registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
        documents = {
            document["document_id"]: document
            for document in registry["documents"]
        }
        expected = {
            "DOC-REG-ENTRADA-DOCUMENTACAO": (OPERATIONAL_README, "0.2.3"),
            "DOC-REG-WF-DOCUMENTACAO": (WORKFLOW, "0.2.3"),
        }

        for document_id, (path, version) in expected.items():
            with self.subTest(document_id=document_id):
                document = documents[document_id]
                content_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(version, document["version"])
                self.assertEqual(content_hash, document["content_hash"])
                self.assertEqual("RASCUNHO", document["workflow_status"])

    def test_pyright_targets_only_package_and_tests(self) -> None:
        config = json.loads(PYRIGHT_CONFIG.read_text(encoding="utf-8"))

        self.assertEqual(
            [
                "scripts/documentation/validate_documentation",
                "scripts/documentation/tests",
                "scripts/documentation/integration_tests",
            ],
            config["include"],
        )


if __name__ == "__main__":
    unittest.main()
