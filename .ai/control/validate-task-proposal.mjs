// Validador leve de task-proposal.schema.json — subconjunto de JSON Schema 2020-12
// (type, const, enum, required, additionalProperties, items, minItems, maxItems, uniqueItems,
// minLength, maxLength, pattern, minimum, contains, not, if/then/else, allOf, $ref/$defs).
// Sem dependência externa (mesmo princípio de docs/modelagem/schemas/validar.mjs).
// Cobre exatamente as keywords usadas em task-proposal.schema.json — não é um validador
// genérico de JSON Schema 2020-12 e não substitui uma ferramenta certificada (ex.: Ajv) quando
// uma estiver disponível no ambiente.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_SCHEMA = join(HERE, "task-proposal.schema.json");
const DEFAULT_INSTANCE = join(HERE, "..", "task-proposal.example.json");

function resolveRef(ref, root) {
  const path = ref.replace(/^#\//, "").split("/");
  let node = root;
  for (const p of path) node = node[p];
  return node;
}

function validate(instance, schema, root, path, errors) {
  if (schema.$ref) {
    validate(instance, resolveRef(schema.$ref, root), root, path, errors);
  }
  if (schema.const !== undefined) {
    if (instance !== schema.const) errors.push(`${path}: expected const ${JSON.stringify(schema.const)}, got ${JSON.stringify(instance)}`);
  }
  if (schema.enum) {
    if (!schema.enum.includes(instance)) errors.push(`${path}: ${JSON.stringify(instance)} not in enum ${JSON.stringify(schema.enum)}`);
  }
  if (schema.type) {
    const t = schema.type;
    const actual = Array.isArray(instance) ? "array" : instance === null ? "null" : typeof instance;
    if (t === "integer") {
      if (!Number.isInteger(instance)) errors.push(`${path}: expected integer, got ${actual}`);
    } else if (actual !== t) {
      errors.push(`${path}: expected ${t}, got ${actual}`);
    }
  }
  if (schema.minLength !== undefined && typeof instance === "string" && instance.length < schema.minLength) {
    errors.push(`${path}: string shorter than minLength ${schema.minLength}`);
  }
  if (schema.maxLength !== undefined && typeof instance === "string" && instance.length > schema.maxLength) {
    errors.push(`${path}: string longer than maxLength ${schema.maxLength}`);
  }
  if (schema.pattern && typeof instance === "string" && !new RegExp(schema.pattern).test(instance)) {
    errors.push(`${path}: does not match pattern ${schema.pattern}`);
  }
  if (schema.minimum !== undefined && typeof instance === "number" && instance < schema.minimum) {
    errors.push(`${path}: below minimum ${schema.minimum}`);
  }
  if (Array.isArray(instance)) {
    if (schema.minItems !== undefined && instance.length < schema.minItems) errors.push(`${path}: fewer than minItems ${schema.minItems}`);
    if (schema.maxItems !== undefined && instance.length > schema.maxItems) errors.push(`${path}: more than maxItems ${schema.maxItems}`);
    if (schema.uniqueItems) {
      const seen = new Set();
      for (const item of instance) {
        const key = JSON.stringify(item);
        if (seen.has(key)) errors.push(`${path}: duplicate item ${key}`);
        seen.add(key);
      }
    }
    if (schema.items) {
      instance.forEach((item, i) => validate(item, schema.items, root, `${path}[${i}]`, errors));
    }
    if (schema.contains) {
      const ok = instance.some((item) => {
        const sub = [];
        validate(item, schema.contains, root, `${path}[contains]`, sub);
        return sub.length === 0;
      });
      if (!ok) errors.push(`${path}: does not contain a match for required item`);
    }
  }
  if (schema.type === "object" || (instance && typeof instance === "object" && !Array.isArray(instance) && schema.properties)) {
    if (schema.required) {
      for (const key of schema.required) {
        if (!(key in instance)) errors.push(`${path}: missing required property "${key}"`);
      }
    }
    if (schema.additionalProperties === false && schema.properties) {
      for (const key of Object.keys(instance)) {
        if (!(key in schema.properties)) errors.push(`${path}: unexpected property "${key}"`);
      }
    }
    if (schema.properties) {
      for (const [key, subschema] of Object.entries(schema.properties)) {
        if (key in instance) validate(instance[key], subschema, root, `${path}.${key}`, errors);
      }
    }
  }
  if (schema.not) {
    const sub = [];
    validate(instance, schema.not, root, path, sub);
    if (sub.length === 0) errors.push(`${path}: matched "not" schema (should not)`);
  }
  if (schema.if) {
    const condErrors = [];
    validate(instance, schema.if, root, path, condErrors);
    const branch = condErrors.length === 0 ? schema.then : schema.else;
    if (branch) validate(instance, branch, root, path, errors);
  }
  if (schema.allOf) {
    for (const sub of schema.allOf) validate(instance, sub, root, path, errors);
  }
}

const schemaPath = process.argv[2] ?? DEFAULT_SCHEMA;
const instancePath = process.argv[3] ?? DEFAULT_INSTANCE;
const schema = JSON.parse(readFileSync(schemaPath, "utf8"));
const instance = JSON.parse(readFileSync(instancePath, "utf8"));
const errors = [];
validate(instance, schema, schema, "$", errors);
if (errors.length === 0) {
  console.log(`VALID: ${instancePath} conforms to ${schemaPath}`);
} else {
  console.log(`INVALID (${errors.length} errors): ${instancePath} against ${schemaPath}`);
  for (const e of errors) console.log(" -", e);
  process.exitCode = 1;
}
