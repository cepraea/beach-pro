"""Behavioral contract for marker-based workspace discovery (BEH-01)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.documentation.validate_documentation import config


class WorkspaceDiscoveryTests(unittest.TestCase):
    """Require all canonical markers before accepting a repository root."""

    expected_error = (
        "Não foi possível localizar o workspace documental. "
        "Marcadores obrigatórios: "
        "docs/registry/registro-documentos.yaml, "
        "docs/registry/workflow-documentacao.yaml, "
        "docs/contracts/schemas/documento.schema.json, "
        "scripts/documentation/validate_documentation"
    )

    def _materialize_workspace(self, root: Path) -> None:
        """Create only the four markers authorized by BEH-01."""
        file_markers = (
            Path("docs/registry/registro-documentos.yaml"),
            Path("docs/registry/workflow-documentacao.yaml"),
            Path("docs/contracts/schemas/documento.schema.json"),
        )
        for marker in file_markers:
            path = root / marker
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n", encoding="utf-8")
        (root / "scripts/documentation/validate_documentation").mkdir(
            parents=True
        )

    def test_finds_workspace_from_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._materialize_workspace(root)

            self.assertEqual(root, config.find_workspace_root(root))

    def test_finds_workspace_from_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._materialize_workspace(root)
            start = root / "docs/registry/registro-documentos.yaml"

            self.assertEqual(root, config.find_workspace_root(start))

    def test_finds_workspace_from_subdirectory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._materialize_workspace(root)
            start = root / "docs/derived/specs"
            start.mkdir(parents=True)

            self.assertEqual(root, config.find_workspace_root(start))

    def test_rejects_partial_markers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._materialize_workspace(root)
            (
                root / "docs/contracts/schemas/documento.schema.json"
            ).unlink()

            with self.assertRaisesRegex(
                RuntimeError,
                f"^{self.expected_error}$",
            ):
                config.find_workspace_root(root)

    def test_rejects_total_marker_absence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(
                RuntimeError,
                f"^{self.expected_error}$",
            ):
                config.find_workspace_root(Path(directory))

    def test_resolves_symlink_before_searching_ancestors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            container = Path(directory)
            root = container / "repository"
            root.mkdir()
            self._materialize_workspace(root)
            nested = root / "docs/derived"
            nested.mkdir()
            symlink = container / "workspace-link"
            try:
                symlink.symlink_to(nested, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"symlink not supported: {error}")

            self.assertEqual(root, config.find_workspace_root(symlink))
