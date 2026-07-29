"""Regression tests for the athlete-function and tactical-role taxonomy."""

from pathlib import Path
import unittest


WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
DOCS_ROOT = WORKSPACE_ROOT / "docs"

NORMATIVE_DOCUMENTS = (
    DOCS_ROOT / "README.md",
    DOCS_ROOT / "canonical/context/contexto-cepraea-beach-pro.md",
    DOCS_ROOT / "canonical/decisions/decisao-019-mvp-sintetico.md",
    DOCS_ROOT / "canonical/decisions/decisao-mapa-features.md",
    DOCS_ROOT
    / "controlled/candidates/contexto-produto-cepraea-beach-pro.md",
    DOCS_ROOT
    / "controlled/candidates/proposta-mvp-sintetico-cepraea.md",
    DOCS_ROOT / "validation/reports/relatorio-auditoria-requisitos-mvp.md",
)


class DomainTaxonomyTests(unittest.TestCase):
    """Keep permanent athlete data separate from contextual match roles."""

    def test_dec_019_declares_all_domain_invariants(self) -> None:
        decision = (
            DOCS_ROOT / "canonical/decisions/decisao-019-mvp-sintetico.md"
        ).read_text(encoding="utf-8")

        for invariant_number in range(1, 6):
            with self.subTest(invariant_number=invariant_number):
                self.assertIn(
                    f"INV-DOM-{invariant_number:03d}",
                    decision,
                )

    def test_normative_documents_do_not_restore_the_invalid_taxonomy(
        self,
    ) -> None:
        forbidden_statements = (
            "especialista substitui coringa",
            "não é nome alternativo para especialista",
            "goleira, defesa, ataque, especialista e indefinida",
            "goleira, defesa, ataque, especialista ou indefinida",
        )

        for path in NORMATIVE_DOCUMENTS:
            content = path.read_text(encoding="utf-8").casefold()
            for statement in forbidden_statements:
                with self.subTest(path=path, statement=statement):
                    self.assertNotIn(statement, content)

    def test_canonical_decision_limits_broad_functions(self) -> None:
        decision = (
            DOCS_ROOT / "canonical/decisions/decisao-019-mvp-sintetico.md"
        ).read_text(encoding="utf-8")
        coverage = decision.split(
            "Fica aprovada somente a cobertura quantitativa pelas funções "
            "amplas:",
            maxsplit=1,
        )[1].split("Posições específicas", maxsplit=1)[0]

        self.assertIn("- goleira;", coverage)
        self.assertIn("- defesa;", coverage)
        self.assertIn("- ataque;", coverage)
        self.assertIn("- indefinida.", coverage)
        self.assertNotIn("- especialista", coverage.casefold())
        self.assertNotIn("- coringa", coverage.casefold())

    def test_legacy_source_preserves_value_with_supersession_note(self) -> None:
        source = (
            DOCS_ROOT / "sources/primary/contexto-operacional-cepraea.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "`GOLEIRA`, `DEFESA`, `ATAQUE`, `CORINGA` e\n`INDEFINIDA`",
            source,
        )
        self.assertIn("Nota de superação do modelo legado", source)
        self.assertIn(
            "`CORINGA` e `ESPECIALISTA` denominam o mesmo papel",
            source,
        )


if __name__ == "__main__":
    unittest.main()
