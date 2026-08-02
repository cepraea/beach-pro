"""Tests for G-FM front matter parsing and validation."""

import unittest
from pathlib import Path
from typing import Any

from scripts.documentation.validate_documentation import (
    front_matter as front_matter_module,
    reporter as reporter_module,
)
from scripts.documentation.validate_documentation.json_types import JsonObject

# ── Helpers ───────────────────────────────────────────────────────────────────


def _tmp(tmp_path: Path, content: str, name: str = "doc.md") -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


def _governed_record(**overrides: Any) -> JsonObject:
    base: JsonObject = {
        "document_id": "DOC-CEPRAEA-DEC-019-MVP-SINTETICO",
        "title": "DEC-019 — Recorte e autorização do MVP sintético",
        "document_type": "decisao",
        "version": "0.1.1",
        "workflow_status": "CANONICA_VIGENTE",
        "responsible": "Davi Sermenho",
        "authority_scope": {
            "subjects": ["recorte_do_mvp"],
            "permitted_uses": ["decisao_vigente"],
            "prohibited_uses": ["aprovacao_por_inferencia", "dados_reais"],
        },
    }
    base.update(overrides)
    return base


VALID_GOVERNED = (
    "---\n"
    "document_id: DOC-CEPRAEA-DEC-019-MVP-SINTETICO\n"
    'title: "DEC-019 — Recorte e autorização do MVP sintético"\n'
    "document_type: decisao\n"
    "version: '0.1.1'\n"
    "workflow_status: CANONICA_VIGENTE\n"
    "responsible: Davi Sermenho\n"
    "permitted_uses:\n"
    "  - decisao_vigente\n"
    "prohibited_uses:\n"
    "  - aprovacao_por_inferencia\n"
    "  - dados_reais\n"
    "---\n"
    "\n"
    "# Body text preserved byte for byte.\n"
)

VALID_FEATURE_INCLUDED = (
    "---\n"
    "feature_id: FT-PRESENCAS\n"
    'title: "Feature: Controle de presenças"\n'
    "type: feature_spec\n"
    "mvp_status: INCLUIDO\n"
    "milestones: [M3]\n"
    "authorized_units: [MVP-05]\n"
    "authorized_requirements: [RF-018]\n"
    "authorized_by: DOC-CEPRAEA-DEC-MAPA-FEATURES\n"
    "derived_from: [DOC-CEPRAEA-DEC-019-MVP-SINTETICO]\n"
    "---\n"
    "\n"
    "# Body\n"
)

VALID_FEATURE_ADIADO = (
    "---\n"
    "feature_id: FT-JOGOS\n"
    'title: "Feature: Gestão de jogos"\n'
    "type: feature_spec\n"
    "mvp_status: ADIADO\n"
    "milestones: []\n"
    "---\n"
    "\n"
    "# Body\n"
)


# ── parse_front_matter: governed ──────────────────────────────────────────────


class TestParseGoverned(unittest.TestCase):
    def setUp(self) -> None:
        import tempfile

        self._tmp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_dir.name)

    def tearDown(self) -> None:
        self._tmp_dir.cleanup()

    def _parse(
        self,
        content: str,
    ) -> tuple[JsonObject | None, reporter_module.Reporter]:
        r = reporter_module.Reporter()
        path = _tmp(self.tmp, content)
        result = front_matter_module.parse_front_matter(path, "governed", r)
        return result, r

    def test_valid_document(self) -> None:
        data, r = self._parse(VALID_GOVERNED)
        self.assertIsNotNone(data)
        self.assertEqual(r.errors, [])

    def test_front_matter_absent(self) -> None:
        _, r = self._parse("# No front matter\n\nJust body.\n")
        self.assertTrue(any("front matter absent" in e for e in r.errors))

    def test_yaml_invalid(self) -> None:
        _, r = self._parse("---\nkey: [unclosed\n---\n# body\n")
        self.assertTrue(any("invalid YAML" in e for e in r.errors))

    def test_invalid_utf8_reports_file_and_stops_validation(self) -> None:
        path = self.tmp / "invalid-utf8.md"
        path.write_bytes(b"---\ntitle: \xff\n---\n# body\n")
        reporter = reporter_module.Reporter()

        data = front_matter_module.parse_front_matter(
            path,
            "governed",
            reporter,
        )

        self.assertIsNone(data)
        self.assertTrue(
            any(
                str(path) in error and "invalid UTF-8" in error
                for error in reporter.errors
            ),
            msg=f"expected controlled UTF-8 error, got: {reporter.errors}",
        )

    def test_missing_closing_delimiter(self) -> None:
        _, r = self._parse(
            "---\ndocument_id: DOC-CEPRAEA-DEC-019-MVP-SINTETICO\n# no closing\n"
        )
        self.assertTrue(any("missing closing delimiter" in e for e in r.errors))

    def test_duplicate_key_top_level(self) -> None:
        content = (
            "---\n"
            "document_id: DOC-CEPRAEA-DEC-019-MVP-SINTETICO\n"
            "document_id: DOC-CEPRAEA-DEC-019-MVP-SINTETICO\n"
            "title: title\n"
            "---\n# body\n"
        )
        _, r = self._parse(content)
        self.assertTrue(
            any("duplicate key" in e for e in r.errors),
            msg=f"expected duplicate key error, got: {r.errors}",
        )

    def test_duplicate_key_nested(self) -> None:
        content = (
            "---\n"
            "document_id: DOC-CEPRAEA-DEC-019-MVP-SINTETICO\n"
            "nested:\n"
            "  key: a\n"
            "  key: b\n"
            "---\n# body\n"
        )
        _, r = self._parse(content)
        self.assertTrue(
            any("duplicate key" in e for e in r.errors),
            msg=f"expected duplicate key error in nested, got: {r.errors}",
        )

    def test_complex_mapping_key_reports_controlled_yaml_error(self) -> None:
        data, reporter = self._parse(
            "---\n"
            "? [document_id, version]\n"
            ": invalid-complex-key\n"
            "---\n"
            "# body\n"
        )

        self.assertIsNone(data)
        self.assertTrue(
            any(
                "invalid YAML" in error and "mapping key" in error
                for error in reporter.errors
            ),
            msg=f"expected controlled complex-key error, got: {reporter.errors}",
        )

    def test_unknown_field_rejected(self) -> None:
        content = (
            "---\n"
            "document_id: DOC-CEPRAEA-DEC-019-MVP-SINTETICO\n"
            "title: t\ndocument_type: decisao\nversion: '0.1.0'\n"
            "workflow_status: RASCUNHO\n"
            "permitted_uses: []\nprohibited_uses: []\n"
            "unknown_field: value\n"
            "---\n# body\n"
        )
        _, r = self._parse(content)
        self.assertTrue(r.errors, "expected schema error for unknown field")

    def test_body_preserved(self) -> None:
        body_marker = "UNIQUE_BODY_MARKER_XYZ"
        content = VALID_GOVERNED + f"\n{body_marker}\n"
        path = _tmp(self.tmp, content, "body_test.md")
        raw = path.read_text(encoding="utf-8")
        self.assertIn(body_marker, raw)


# ── validate_governed: sync with registry ─────────────────────────────────────


class TestValidateGoverned(unittest.TestCase):
    def setUp(self) -> None:
        import tempfile

        self._tmp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_dir.name)

    def tearDown(self) -> None:
        self._tmp_dir.cleanup()

    def _run(
        self,
        content: str,
        record: JsonObject,
    ) -> reporter_module.Reporter:
        path = _tmp(self.tmp, content)
        record = dict(record)
        record["current_path"] = str(path)
        r = reporter_module.Reporter()
        front_matter_module.validate_governed(record, r)
        return r

    def test_valid_sync(self) -> None:
        r = self._run(VALID_GOVERNED, _governed_record())
        self.assertEqual(r.errors, [])

    def test_field_diverges_document_type(self) -> None:
        record = _governed_record(document_type="contexto")
        r = self._run(VALID_GOVERNED, record)
        self.assertTrue(any("document_type" in e for e in r.errors))

    def test_workflow_status_diverges(self) -> None:
        record = _governed_record(workflow_status="RASCUNHO")
        r = self._run(VALID_GOVERNED, record)
        self.assertTrue(any("workflow_status" in e for e in r.errors))

    def test_responsible_present_matches(self) -> None:
        r = self._run(VALID_GOVERNED, _governed_record())
        self.assertEqual(r.errors, [])

    def test_responsible_absent_in_registry(self) -> None:
        record = _governed_record()
        record.pop("responsible")
        path = _tmp(self.tmp, VALID_GOVERNED, "resp_test.md")
        record["current_path"] = str(path)
        r = reporter_module.Reporter()
        front_matter_module.validate_governed(record, r)
        self.assertTrue(
            any("responsible" in e for e in r.errors),
            msg="FM has responsible but registry does not — should error",
        )

    def test_excessive_permitted_use(self) -> None:
        content = VALID_GOVERNED.replace(
            "  - decisao_vigente\n",
            "  - decisao_vigente\n  - uso_nao_autorizado\n",
        )
        r = self._run(content, _governed_record())
        self.assertTrue(any("permitted_uses" in e for e in r.errors))

    def test_missing_prohibited_use(self) -> None:
        content = VALID_GOVERNED.replace(
            "  - aprovacao_por_inferencia\n  - dados_reais\n",
            "  - aprovacao_por_inferencia\n",
        )
        r = self._run(content, _governed_record())
        self.assertTrue(any("prohibited_uses" in e for e in r.errors))

    def test_registry_exclusive_field_rejected(self) -> None:
        content = VALID_GOVERNED.replace(
            "responsible: Davi Sermenho\n",
            "responsible: Davi Sermenho\ncontent_hash: abc123\n",
        )
        r = self._run(content, _governed_record())
        self.assertTrue(r.errors, "content_hash is a registry-exclusive field")


# ── validate_feature_spec ─────────────────────────────────────────────────────


class TestValidateFeatureSpec(unittest.TestCase):
    def setUp(self) -> None:
        import tempfile

        self._tmp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_dir.name)

    def tearDown(self) -> None:
        self._tmp_dir.cleanup()

    def _run(self, content: str) -> reporter_module.Reporter:
        path = _tmp(self.tmp, content)
        r = reporter_module.Reporter()
        front_matter_module.validate_feature_spec(path, r)
        return r

    def test_valid_incluido(self) -> None:
        r = self._run(VALID_FEATURE_INCLUDED)
        self.assertEqual(r.errors, [])

    def test_valid_adiado_empty_milestones(self) -> None:
        r = self._run(VALID_FEATURE_ADIADO)
        self.assertEqual(r.errors, [])

    def test_milestones_invalid_for_adiado(self) -> None:
        content = VALID_FEATURE_ADIADO.replace("milestones: []", "milestones: [M1]")
        r = self._run(content)
        self.assertTrue(r.errors, "non-empty milestones for ADIADO must fail")

    def test_duplicate_in_unique_items_array(self) -> None:
        content = VALID_FEATURE_INCLUDED.replace(
            "authorized_units: [MVP-05]\n",
            "authorized_units: [MVP-05, MVP-05]\n",
        )
        r = self._run(content)
        self.assertTrue(any("authorized_units" in e for e in r.errors))

    def test_authorization_absent_for_incluido(self) -> None:
        content = (
            "---\n"
            "feature_id: FT-PRESENCAS\n"
            'title: "Feature: Controle de presenças"\n'
            "type: feature_spec\n"
            "mvp_status: INCLUIDO\n"
            "milestones: [M3]\n"
            "---\n# body\n"
        )
        r = self._run(content)
        self.assertTrue(
            r.errors,
            "INCLUIDO without authorized_units/requirements/authorized_by/derived_from must fail",
        )

    def test_derived_from_absent_for_incluido(self) -> None:
        content = (
            "---\n"
            "feature_id: FT-PRESENCAS\n"
            'title: "Feature: Controle de presenças"\n'
            "type: feature_spec\n"
            "mvp_status: INCLUIDO\n"
            "milestones: [M3]\n"
            "authorized_units: [MVP-05]\n"
            "authorized_requirements: [RF-018]\n"
            "authorized_by: DOC-CEPRAEA-DEC-MAPA-FEATURES\n"
            "---\n# body\n"
        )
        r = self._run(content)
        self.assertTrue(any("derived_from" in e for e in r.errors))

    def test_front_matter_absent(self) -> None:
        r = self._run("# No front matter\n")
        self.assertTrue(any("front matter absent" in e for e in r.errors))


if __name__ == "__main__":
    unittest.main()
