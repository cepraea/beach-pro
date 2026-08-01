import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const GOVERNANCE_ROOT = path.resolve(__dirname, '..');

export const LANE_RANK = Object.freeze({
  VIA_RAPIDA: 1,
  VIA_CONTROLADA: 2,
  VIA_CRITICA: 3,
});

export async function readJson(filePath) {
  const raw = await readFile(filePath, 'utf8');
  try {
    return JSON.parse(raw);
  } catch (error) {
    throw new Error(`JSON_INVALIDO: ${filePath}: ${error.message}`);
  }
}

export async function loadSchema(schemaName) {
  const normalized = schemaName.endsWith('.json') ? schemaName : `${schemaName}.json`;
  return readJson(path.join(GOVERNANCE_ROOT, 'schemas', normalized));
}

export async function loadPolicy(policyName) {
  const normalized = policyName.endsWith('.json') ? policyName : `${policyName}.json`;
  return readJson(path.join(GOVERNANCE_ROOT, 'policies', normalized));
}

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function typeMatches(expected, value) {
  switch (expected) {
    case 'object': return isPlainObject(value);
    case 'array': return Array.isArray(value);
    case 'string': return typeof value === 'string';
    case 'integer': return Number.isInteger(value);
    case 'number': return typeof value === 'number' && Number.isFinite(value);
    case 'boolean': return typeof value === 'boolean';
    case 'null': return value === null;
    default: return false;
  }
}

function validateString(schema, value, pointer, errors) {
  if (schema.minLength !== undefined && value.length < schema.minLength) {
    errors.push(`${pointer}: minLength=${schema.minLength}`);
  }
  if (schema.maxLength !== undefined && value.length > schema.maxLength) {
    errors.push(`${pointer}: maxLength=${schema.maxLength}`);
  }
  if (schema.pattern !== undefined && !(new RegExp(schema.pattern).test(value))) {
    errors.push(`${pointer}: não corresponde ao pattern ${schema.pattern}`);
  }
  if (schema.format === 'date-time' && Number.isNaN(Date.parse(value))) {
    errors.push(`${pointer}: date-time inválido`);
  }
}

function validateArray(schema, value, pointer, errors) {
  if (schema.minItems !== undefined && value.length < schema.minItems) {
    errors.push(`${pointer}: minItems=${schema.minItems}`);
  }
  if (schema.maxItems !== undefined && value.length > schema.maxItems) {
    errors.push(`${pointer}: maxItems=${schema.maxItems}`);
  }
  if (schema.uniqueItems === true) {
    const serialized = value.map((item) => JSON.stringify(item));
    if (new Set(serialized).size !== serialized.length) {
      errors.push(`${pointer}: itens duplicados não permitidos`);
    }
  }
  if (schema.items) {
    value.forEach((item, index) => validateAgainstSchema(schema.items, item, `${pointer}/${index}`, errors));
  }
}

function validateObject(schema, value, pointer, errors) {
  const properties = schema.properties ?? {};
  const required = schema.required ?? [];
  for (const key of required) {
    if (!Object.prototype.hasOwnProperty.call(value, key)) {
      errors.push(`${pointer}/${key}: campo obrigatório ausente`);
    }
  }
  for (const [key, childValue] of Object.entries(value)) {
    if (Object.prototype.hasOwnProperty.call(properties, key)) {
      validateAgainstSchema(properties[key], childValue, `${pointer}/${key}`, errors);
    } else if (schema.additionalProperties === false) {
      errors.push(`${pointer}/${key}: propriedade adicional não permitida`);
    } else if (isPlainObject(schema.additionalProperties)) {
      validateAgainstSchema(schema.additionalProperties, childValue, `${pointer}/${key}`, errors);
    }
  }
}

export function validateAgainstSchema(schema, value, pointer = '$', errors = []) {
  if (schema.const !== undefined && value !== schema.const) {
    errors.push(`${pointer}: deve ser ${JSON.stringify(schema.const)}`);
    return errors;
  }
  if (schema.enum && !schema.enum.includes(value)) {
    errors.push(`${pointer}: valor não permitido ${JSON.stringify(value)}`);
    return errors;
  }
  if (schema.type) {
    const expected = Array.isArray(schema.type) ? schema.type : [schema.type];
    if (!expected.some((type) => typeMatches(type, value))) {
      errors.push(`${pointer}: tipo inválido; esperado ${expected.join('|')}`);
      return errors;
    }
  }
  if (typeof value === 'string') validateString(schema, value, pointer, errors);
  if (Array.isArray(value)) validateArray(schema, value, pointer, errors);
  if (isPlainObject(value)) validateObject(schema, value, pointer, errors);
  return errors;
}

function collectForbiddenString(value, forbidden, pointer = '$', findings = []) {
  if (typeof value === 'string') {
    if (forbidden.some((term) => value.toUpperCase().includes(term.toUpperCase()))) {
      findings.push(pointer);
    }
  } else if (Array.isArray(value)) {
    value.forEach((item, index) => collectForbiddenString(item, forbidden, `${pointer}/${index}`, findings));
  } else if (isPlainObject(value)) {
    for (const [key, child] of Object.entries(value)) {
      collectForbiddenString(child, forbidden, `${pointer}/${key}`, findings);
    }
  }
  return findings;
}

export function validateSemanticContract(schemaId, value) {
  const errors = [];
  if (schemaId === 'checker-report.schema') {
    const forbidden = collectForbiddenString(value, ['APROVADO']);
    for (const pointer of forbidden) {
      errors.push(`${pointer}: termo epistemológico proibido no CHECKER_REPORT`);
    }
    if (value.result === 'DIVERGENCIA_ENCONTRADA' && (!Array.isArray(value.findings) || value.findings.length === 0)) {
      errors.push('$/findings: DIVERGENCIA_ENCONTRADA exige ao menos um finding');
    }
    if (value.result === 'CONFORME' && Array.isArray(value.findings) && value.findings.length > 0) {
      errors.push('$/findings: CONFORME não pode conter divergências');
    }
    if (value.result === 'INCONCLUSIVO' && (!Array.isArray(value.limitations) || value.limitations.length === 0)) {
      errors.push('$/limitations: INCONCLUSIVO exige limitação declarada');
    }
  }
  if (schemaId === 'approval-record.schema' && !value.approver_id?.startsWith('HUM-')) {
    errors.push('$/approver_id: aprovação exige identificador humano HUM-*');
  }
  return errors;
}

export async function validateDocument(schemaName, value) {
  const schema = await loadSchema(schemaName);
  const schemaId = path.basename(schemaName, '.json');
  return [
    ...validateAgainstSchema(schema, value),
    ...validateSemanticContract(schemaId, value),
  ];
}

function stripVolatile(value, volatileKeys) {
  if (Array.isArray(value)) return value.map((item) => stripVolatile(item, volatileKeys));
  if (!isPlainObject(value)) return value;
  const output = {};
  for (const [key, child] of Object.entries(value)) {
    if (!volatileKeys.has(key)) output[key] = stripVolatile(child, volatileKeys);
  }
  return output;
}

function stable(value) {
  if (Array.isArray(value)) return value.map(stable);
  if (!isPlainObject(value)) return value;
  const output = {};
  for (const key of Object.keys(value).sort()) output[key] = stable(value[key]);
  return output;
}

export function canonicalize(value, profile = { volatile_keys: [] }) {
  const volatileKeys = new Set(profile.volatile_keys ?? []);
  return JSON.stringify(stable(stripVolatile(value, volatileKeys)));
}

export function sha256(value) {
  return `sha256:${createHash('sha256').update(value, 'utf8').digest('hex')}`;
}

export function canonicalHash(value, profile) {
  return sha256(canonicalize(value, profile));
}

export function routeAction(action, routingPolicy) {
  const critical = new Set(routingPolicy.critical_triggers ?? []);
  const controlled = new Set(routingPolicy.controlled_triggers ?? []);
  const triggers = new Set(action.mandatory_triggers ?? []);

  let computed = 'VIA_RAPIDA';
  if ([...triggers].some((trigger) => critical.has(trigger))) computed = 'VIA_CRITICA';
  else if ([...triggers].some((trigger) => controlled.has(trigger))) computed = 'VIA_CONTROLADA';

  const declared = action.assigned_lane;
  if (declared && !LANE_RANK[declared]) throw new Error(`VIA_INVALIDA: ${declared}`);

  const assigned = declared && LANE_RANK[declared] > LANE_RANK[computed] ? declared : computed;
  return {
    action_id: action.action_id,
    previous_lane: declared ?? null,
    computed_lane: computed,
    assigned_lane: assigned,
    elevated: declared ? LANE_RANK[assigned] > LANE_RANK[declared] : false,
    downgrade_blocked: declared ? LANE_RANK[declared] > LANE_RANK[computed] : false,
    matched_critical_triggers: [...triggers].filter((trigger) => critical.has(trigger)),
    matched_controlled_triggers: [...triggers].filter((trigger) => controlled.has(trigger)),
    policy_version: routingPolicy.version,
  };
}
