import assert from 'node:assert/strict';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {
  buildMigrationArtifacts,
  classifyOccurrence,
  outputFiles,
  scanRepository,
} from '../src/migrate-history.mjs';

const policy = {
  policy_id: 'MIG-EPISTEMIC-001',
  version: '1.1.0',
  baseline_commit: 'baseline',
  legacy_term: 'APROVADO',
  scan_extensions: ['.json', '.jsonl', '.yaml', '.yml', '.md', '.mjs'],
  excluded_directories: ['.git', 'node_modules', 'dist'],
  excluded_output_prefixes: ['governance/artifacts/migrations/act-f00-008/'],
  human_approval_prefixes: ['docs/evidence/approvals/', 'governance/artifacts/approvals/'],
  historical_prefixes: ['docs/archive/', '.inicio/historico/'],
  technical_validation_prefixes: ['docs/validation/reports/', '.inicio/evidencias/validate-documentation/', '.inicio/evidencias/VALIDACAO-VSCODE.md', 'RELATORIO-VSCODE.md'],
  negative_test_fragments: ['/tests/', 'test/', 'fixture', 'fixtures'],
  normative_paths: ['governance/schemas/approval-record.schema.json', 'docs/contracts/schemas/workflow.schema.json'],
  explicit_active_fields: ['validation_result', 'validator_result', 'checker_result', 'maker_result', 'legacy_declared_status'],
  technical_result_fields: ['result', 'resultado', 'status', 'validation_result', 'validator_result', 'checker_result', 'maker_result'],
  normalization_rules: [],
  invariants: {
    preserve_original: true,
    human_approval_inferred: false,
    migration_idempotent: true,
    active_prohibited_occurrences_after_migration: 0,
    unclassified_occurrences: 0,
    historical_records_authorize_gate: false,
  },
};

assert.equal(classifyOccurrence({
  filePath: 'docs/evidence/approvals/aprovacao.yaml',
  line: 'decision: APROVADO',
  field: 'decision',
}, policy), 'LEGITIMATE_HUMAN_APPROVAL');

assert.equal(classifyOccurrence({
  filePath: 'docs/validation/reports/resultado.yaml',
  line: 'result: APROVADO',
  field: 'result',
}, policy), 'LEGACY_ACTIVE_STATUS');

assert.equal(classifyOccurrence({
  filePath: 'docs/canonical/context/contexto.md',
  line: '- **Status:** APROVADO',
  field: 'status',
}, policy), 'DOCUMENTATION_REFERENCE');

assert.equal(classifyOccurrence({
  filePath: 'docs/contracts/schemas/workflow.schema.json',
  line: '"status": {"enum": ["RASCUNHO", "APROVADO"]}',
  field: 'status',
}, policy), 'NORMATIVE_RULE');

assert.equal(classifyOccurrence({
  filePath: 'docs/archive/resultado.md',
  line: 'Resultado histórico: APROVADO',
  field: 'resultado_histórico',
}, policy), 'HISTORICAL_CITATION');

assert.equal(classifyOccurrence({
  filePath: 'governance/tests/negative-fixture.json',
  line: '"checker_result": "APROVADO"',
  field: 'checker_result',
}, policy), 'NEGATIVE_TEST_FIXTURE');

const root = await mkdtemp(path.join(os.tmpdir(), 'act-f00-008-'));
try {
  await mkdir(path.join(root, 'docs/validation/reports'), { recursive: true });
  await mkdir(path.join(root, 'docs/evidence/approvals'), { recursive: true });
  await mkdir(path.join(root, 'docs/archive'), { recursive: true });
  await mkdir(path.join(root, 'docs/canonical/context'), { recursive: true });
  await mkdir(path.join(root, 'governance/tests'), { recursive: true });

  await writeFile(path.join(root, 'docs/validation/reports/report.json'), '{\n  "result": "APROVADO"\n}\n');
  await writeFile(path.join(root, 'docs/evidence/approvals/approval.yaml'), 'decision: APROVADO\napprover_id: HUM-DAVI-SERMENHO\n');
  await writeFile(path.join(root, 'docs/archive/history.md'), 'Resultado histórico: APROVADO\n');
  await writeFile(path.join(root, 'docs/canonical/context/context.md'), '- **Status:** APROVADO\n');
  await writeFile(path.join(root, 'governance/tests/negative-fixture.json'), '{"checker_result":"APROVADO"}\n');

  const occurrences = await scanRepository(root, policy);
  assert.equal(occurrences.length, 5);
  assert.equal(occurrences.filter((item) => item.classification === 'LEGACY_ACTIVE_STATUS').length, 1);
  assert.equal(occurrences.filter((item) => item.classification === 'LEGITIMATE_HUMAN_APPROVAL').length, 1);
  assert.equal(occurrences.filter((item) => item.classification === 'HISTORICAL_CITATION').length, 1);
  assert.equal(occurrences.filter((item) => item.classification === 'DOCUMENTATION_REFERENCE').length, 1);
  assert.equal(occurrences.filter((item) => item.classification === 'NEGATIVE_TEST_FIXTURE').length, 1);

  const artifactsA = buildMigrationArtifacts(occurrences, policy);
  const artifactsB = buildMigrationArtifacts(occurrences, policy);
  assert.deepEqual(artifactsA, artifactsB, 'A migração deve ser determinística e idempotente');
  assert.equal(artifactsA.migratedRecords.length, 1);
  assert.equal(artifactsA.migratedRecords[0].legacy_result, 'APROVADO');
  assert.equal(artifactsA.migratedRecords[0].normalized_result, 'VALIDACAO_ESTRUTURAL_CONFORME');
  assert.equal(artifactsA.migratedRecords[0].historical_record, true);
  assert.equal(artifactsA.migratedRecords[0].human_approval_inferred, false);
  assert.equal(artifactsA.summary.active_prohibited_occurrences_after_migration, 0);
  assert.equal(artifactsA.summary.human_approvals_fabricated, 0);
  assert.equal(artifactsA.summary.original_records_deleted_or_rewritten, 0);
  assert.equal(artifactsA.summary.result, 'MIGRACAO_HISTORICA_CONFORME');
  assert.deepEqual(outputFiles(artifactsA), outputFiles(artifactsB));
} finally {
  await rm(root, { recursive: true, force: true });
}

console.log(JSON.stringify({
  result: 'AUTOTESTE_CONFORME',
  suite: 'ACT-F00-008',
  assertions: 23
}, null, 2));
