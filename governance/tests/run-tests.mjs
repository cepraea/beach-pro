import assert from 'node:assert/strict';
import {
  canonicalHash,
  canonicalize,
  routeAction,
  validateDocument,
} from '../src/runtime.mjs';
import routingPolicy from '../policies/routing-rules.json' with { type: 'json' };
import canonicalProfile from '../policies/canonicalization-profile.json' with { type: 'json' };

const HASH_A = `sha256:${'a'.repeat(64)}`;

async function expectValid(schema, value) {
  const errors = await validateDocument(schema, value);
  assert.deepEqual(errors, [], `Esperado válido, erros: ${errors.join('; ')}`);
}

async function expectInvalid(schema, value, pattern) {
  const errors = await validateDocument(schema, value);
  assert.ok(errors.length > 0, 'Esperado inválido');
  if (pattern) {
    assert.ok(errors.some((error) => pattern.test(error)), `Erro esperado não encontrado: ${errors.join('; ')}`);
  }
}

const validChecker = {
  checker_run_id: 'CHK-PILOTO-001',
  checker_id: 'AGENT-CHECKER-01',
  checker_role: 'CHECKER',
  review_policy_version: '1.0.0',
  candidate_artifact_id: 'ART-UC-001',
  candidate_artifact_version: '1.0.0',
  candidate_content_hash: HASH_A,
  source_hashes: [HASH_A],
  uc_id: 'UC-F04-000001',
  source_id: 'SRC-F03-001',
  segment_ids: ['SEG-F03-001-001'],
  result: 'DIVERGENCIA_ENCONTRADA',
  checked_fields: ['normalized_statement'],
  findings: [{
    finding_id: 'DIV-PILOTO-001',
    field: 'normalized_statement',
    claim_checked: 'A regra não possui exceção.',
    source_evidence: 'A fonte contém uma exceção explícita.',
    source_locator: {
      source_id: 'SRC-F03-001',
      segment_id: 'SEG-F03-001-001',
      additional_locator: 'parágrafo 3'
    },
    divergence_type: 'EXCECAO_OMITIDA',
    impact: 'MATERIAL',
    rationale: 'A omissão altera a aplicabilidade da regra.',
    recommended_action: 'HUMAN_EXCEPTION_REVIEW'
  }],
  limitations: []
};

await expectValid('checker-report.schema.json', validChecker);
await expectInvalid('checker-report.schema.json', { ...validChecker, result: 'APROVADO' }, /valor não permitido|termo epistemológico proibido/);
await expectInvalid('checker-report.schema.json', { ...validChecker, findings: [] }, /exige ao menos um finding/);
await expectInvalid(
  'checker-report.schema.json',
  { ...validChecker, limitations: ['Resultado APROVADO pelo revisor.'] },
  /termo epistemológico proibido/
);

const risk = {
  classification_id: 'RISK-ACT-F00-004',
  action_id: 'ACT-F00-004',
  classification_policy_version: '1.0.0',
  dimensions: {
    impact: 'CRITICO',
    propagation: 'SISTEMICA',
    reversibility: 'CUSTOSA',
    ambiguity: 'MATERIAL',
    sensitivity: 'INTERNA'
  },
  mandatory_triggers: ['REGRA_NORMATIVA'],
  assigned_lane: 'VIA_CRITICA',
  rationale: ['Regra normativa exige elevação crítica.'],
  input_hashes: [HASH_A],
  classified_by: 'AGENT-ROUTER-01'
};
await expectValid('risk-classification.schema.json', risk);
await expectInvalid(
  'risk-classification.schema.json',
  { ...risk, dimensions: { ...risk.dimensions, sensitivity: undefined } },
  /sensitivity/
);

const criticalRoute = routeAction({
  action_id: 'ACT-F00-004',
  assigned_lane: 'VIA_RAPIDA',
  mandatory_triggers: ['REGRA_NORMATIVA']
}, routingPolicy);
assert.equal(criticalRoute.assigned_lane, 'VIA_CRITICA');
assert.equal(criticalRoute.elevated, true);

const controlledRoute = routeAction({
  action_id: 'ACT-F04-001',
  mandatory_triggers: ['INTERPRETACAO_SEMANTICA']
}, routingPolicy);
assert.equal(controlledRoute.assigned_lane, 'VIA_CONTROLADA');

const fastRoute = routeAction({
  action_id: 'ACT-F04-002',
  mandatory_triggers: []
}, routingPolicy);
assert.equal(fastRoute.assigned_lane, 'VIA_RAPIDA');

const noSilentDowngrade = routeAction({
  action_id: 'ACT-F00-005',
  assigned_lane: 'VIA_CRITICA',
  mandatory_triggers: []
}, routingPolicy);
assert.equal(noSilentDowngrade.assigned_lane, 'VIA_CRITICA');
assert.equal(noSilentDowngrade.downgrade_blocked, true);

const objectA = { b: 2, a: 1, execution_metadata: { model: 'x' } };
const objectB = { a: 1, b: 2, execution_metadata: { model: 'y' } };
assert.equal(canonicalize(objectA, canonicalProfile), canonicalize(objectB, canonicalProfile));
assert.equal(canonicalHash(objectA, canonicalProfile), canonicalHash(objectB, canonicalProfile));
assert.notEqual(canonicalHash(objectA, canonicalProfile), canonicalHash({ a: 1, b: 3 }, canonicalProfile));
assert.notEqual(
  canonicalHash({ list: ['a', 'b'] }, canonicalProfile),
  canonicalHash({ list: ['b', 'a'] }, canonicalProfile)
);

const validApproval = {
  approval_id: 'APR-GOV-001',
  action_id: 'ACT-F00-009',
  artifact_id: 'PKG-PILOTO-001',
  artifact_version: '1.0.0',
  content_hash: HASH_A,
  package_hash: HASH_A,
  approval_scope: ['GATE-F00-GOV-01'],
  decision: 'APROVADO',
  approver_id: 'HUM-DAVI-SERMENHO',
  conditions: []
};
await expectValid('approval-record.schema.json', validApproval);
await expectInvalid(
  'approval-record.schema.json',
  { ...validApproval, approver_id: 'AGENT-CHECKER-01' },
  /HUM-|pattern/
);

console.log(JSON.stringify({
  result: 'AUTOTESTE_CONFORME',
  suite: 'ACT-F00-007',
  assertions: 18
}, null, 2));
