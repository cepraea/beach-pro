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
import policy from '../policies/epistemic-migration-policy.json' with { type: 'json' };

assert.equal(classifyOccurrence({
  filePath: 'docs/evidence/approvals/aprovacao.yaml',
  line: 'decision: APROVADO',
  field: 'decision',
}, policy), 'LEGITIMATE_HUMAN_APPROVAL');
assert.equal(classifyOccurrence({
  filePath: '.inicio/evidencias/VALIDACAO-VSCODE.md',
  line: '| npm run test | 1 teste | Aprovado |',
  field: 'npm_run_test',
}, policy), 'LEGACY_ACTIVE_STATUS');
assert.equal(classifyOccurrence({
  filePath: 'docs/validation/reports/relatorio.md',
  line: '| PA-001 | Critério | **Aprovado** | Evidência | — |',
  field: 'pa-001',
}, policy), 'LEGACY_ACTIVE_STATUS');
assert.equal(classifyOccurrence({
  filePath: 'docs/validation/reports/relatorio.md',
  line: '| PA-002 | Critério | **Aprovado com ressalvas** | Evidência | Ajustar |',
  field: 'pa-002',
}, policy), 'LEGACY_ACTIVE_STATUS');
assert.equal(classifyOccurrence({
  filePath: 'docs/validation/reports/relatorio.md',
  line: '| **Aprovado** | Todos os critérios atendidos. |',
  field: 'aprovado',
}, policy), 'DOCUMENTATION_REFERENCE');
assert.equal(classifyOccurrence({
  filePath: 'docs/validation/reports/relatorio.md',
  line: 'O escopo anteriormente aprovado foi preservado.',
  field: 'text',
}, policy), 'DOCUMENTATION_REFERENCE');
assert.equal(classifyOccurrence({
  filePath: '.inicio/evidencias/validate-documentation/run/validation.md',
  line: 'Vitest: 1 teste aprovado',
  field: 'vitest',
}, policy), 'LEGACY_ACTIVE_STATUS');
assert.equal(classifyOccurrence({
  filePath: '.inicio/evidencias/validate-documentation/run/environment.md',
  line: 'O processo foi aprovado fora do sandbox.',
  field: 'text',
}, policy), 'DOCUMENTATION_REFERENCE');
assert.equal(classifyOccurrence({
  filePath: 'docs/registry/registro-documentos.yaml',
  line: 'legacy_declared_status: DERIVADO_NAO_APROVADO',
  field: 'legacy_declared_status',
}, policy), 'NEGATED_REFERENCE');
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
  await mkdir(path.join(root, 'docs/registry'), { recursive: true });
  await mkdir(path.join(root, '.inicio/evidencias/validate-documentation/run'), { recursive: true });
  await mkdir(path.join(root, 'governance/tests'), { recursive: true });

  await writeFile(path.join(root, 'docs/validation/reports/report.md'), [
    '| PA-001 | Critério | **Aprovado** | Evidência | — |',
    '| PA-002 | Critério | **Aprovado com ressalvas** | Evidência | Ajustar |',
    '| **Aprovado** | Definição do vocabulário. |',
    'O escopo aprovado permanece como referência.',
    '',
  ].join('\n'));
  await writeFile(path.join(root, 'docs/evidence/approvals/approval.yaml'), 'decision: APROVADO\napprover_id: HUM-DAVI-SERMENHO\n');
  await writeFile(path.join(root, 'docs/archive/history.md'), 'Resultado histórico: APROVADO\n');
  await writeFile(path.join(root, 'docs/registry/registry.yaml'), [
    'legacy_declared_status: RASCUNHO_CONTROLADO_V0_APROVADO',
    'legacy_declared_status: DERIVADO_NAO_APROVADO',
    '',
  ].join('\n'));
  await writeFile(path.join(root, '.inicio/evidencias/validate-documentation/run/validation.md'), 'Vitest: 1 teste aprovado\n');
  await writeFile(path.join(root, 'governance/tests/negative-fixture.json'), '{"checker_result":"APROVADO"}\n');

  const occurrences = await scanRepository(root, policy);
  assert.equal(occurrences.length, 10);
  assert.equal(occurrences.filter((item) => item.classification === 'LEGACY_ACTIVE_STATUS').length, 4);
  assert.equal(occurrences.filter((item) => item.classification === 'LEGITIMATE_HUMAN_APPROVAL').length, 1);
  assert.equal(occurrences.filter((item) => item.classification === 'HISTORICAL_CITATION').length, 1);
  assert.equal(occurrences.filter((item) => item.classification === 'DOCUMENTATION_REFERENCE').length, 2);
  assert.equal(occurrences.filter((item) => item.classification === 'NEGATED_REFERENCE').length, 1);
  assert.equal(occurrences.filter((item) => item.classification === 'NEGATIVE_TEST_FIXTURE').length, 1);

  const artifactsA = buildMigrationArtifacts(occurrences, policy);
  const artifactsB = buildMigrationArtifacts(occurrences, policy);
  assert.deepEqual(artifactsA, artifactsB, 'A migração deve ser determinística e idempotente');
  assert.equal(artifactsA.migratedRecords.length, 4);
  const results = artifactsA.migratedRecords.map((record) => record.normalized_result).sort();
  assert.deepEqual(results, [
    'AUTOTESTE_CONFORME',
    'LEGACY_STATUS_PRESERVED',
    'VALIDACAO_ESTRUTURAL_CONFORME',
    'VALIDACAO_ESTRUTURAL_CONFORME_COM_RESSALVAS',
  ].sort());
  const reservation = artifactsA.migratedRecords.find((record) => record.legacy_qualifier === 'COM_RESSALVAS');
  assert.ok(reservation);
  assert.equal(reservation.normalized_result, 'VALIDACAO_ESTRUTURAL_CONFORME_COM_RESSALVAS');
  assert.equal(artifactsA.migratedRecords.every((record) => record.historical_record === true), true);
  assert.equal(artifactsA.migratedRecords.every((record) => record.human_approval_inferred === false), true);
  assert.equal(artifactsA.summary.active_prohibited_occurrences_after_migration, 0);
  assert.equal(artifactsA.summary.human_approvals_fabricated, 0);
  assert.equal(artifactsA.summary.original_records_deleted_or_rewritten, 0);
  assert.equal(artifactsA.summary.total_negated_references, 1);
  assert.equal(artifactsA.summary.result, 'MIGRACAO_HISTORICA_CONFORME');
  assert.deepEqual(outputFiles(artifactsA), outputFiles(artifactsB));
} finally {
  await rm(root, { recursive: true, force: true });
}

console.log(JSON.stringify({
  result: 'AUTOTESTE_CONFORME',
  suite: 'ACT-F00-008',
  assertions: 32
}, null, 2));
