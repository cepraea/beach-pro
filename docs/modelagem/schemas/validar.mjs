#!/usr/bin/env node
// Valida registros do Modelo Canônico CEPRAEA-BEACH-PRO contra o subconjunto de JSON Schema
// declarado na seção 5.3 de PLANO_CEPRAEA_Modelo_Canonico_FINAL.md. Sem dependência externa.
//
// Uso:
//   node validar.mjs                              valida o corpus real em docs/modelagem/**
//   node validar.mjs schemas/fixtures/manifest.json  valida as fixtures declaradas no manifesto
//
// Regra de segurança (seção 5.3): se qualquer schema usar uma keyword fora do subconjunto
// suportado, este script falha explicitamente — nunca ignora silenciosamente uma keyword
// desconhecida.

import { readFileSync, readdirSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, basename } from "node:path";

const SCHEMAS_DIR = dirname(fileURLToPath(import.meta.url));
const MODELAGEM_DIR = dirname(SCHEMAS_DIR);

const ANNOTATION_KEYS = new Set(["$schema", "$id", "title", "description"]);
const VALIDATION_KEYS = new Set([
  "type", "required", "properties", "items", "enum", "const",
  "pattern", "minLength", "minItems", "allOf", "if", "then", "format",
]);
const ALLOWED_KEYS = new Set([...ANNOTATION_KEYS, ...VALIDATION_KEYS]);

// ---------------------------------------------------------------------------
// Guarda de keywords conhecidas — roda sobre o SCHEMA, não sobre a instância.
// ---------------------------------------------------------------------------
function checkKnownKeywords(schema, path = "$") {
  if (schema === null || typeof schema !== "object" || Array.isArray(schema)) return;
  for (const key of Object.keys(schema)) {
    if (!ALLOWED_KEYS.has(key)) {
      throw new Error(
        `Keyword desconhecida '${key}' em ${path} — fora do subconjunto suportado por ` +
          `validar.mjs (seção 5.3 do plano). Falha explícita, keyword não ignorada.`
      );
    }
    if (key === "format" && schema.format !== "date") {
      throw new Error(`format='${schema.format}' em ${path}.format não suportado — só 'date' está implementado.`);
    }
    if (key === "properties") {
      for (const [propKey, propSchema] of Object.entries(schema.properties)) {
        checkKnownKeywords(propSchema, `${path}.properties.${propKey}`);
      }
    } else if (key === "items") {
      checkKnownKeywords(schema.items, `${path}.items`);
    } else if (key === "allOf") {
      schema.allOf.forEach((s, i) => checkKnownKeywords(s, `${path}.allOf[${i}]`));
    } else if (key === "if" || key === "then") {
      checkKnownKeywords(schema[key], `${path}.${key}`);
    }
  }
}

// ---------------------------------------------------------------------------
// Validador de instância contra schema (subconjunto fixo de keywords).
// ---------------------------------------------------------------------------
function deepEqual(a, b) {
  if (a === b) return true;
  if (typeof a !== typeof b) return false;
  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
    return a.every((v, i) => deepEqual(v, b[i]));
  }
  if (a && b && typeof a === "object") {
    const ka = Object.keys(a).sort();
    const kb = Object.keys(b).sort();
    if (!deepEqual(ka, kb)) return false;
    return ka.every((k) => deepEqual(a[k], b[k]));
  }
  return false;
}

function typeOf(instance) {
  if (instance === null) return "null";
  if (Array.isArray(instance)) return "array";
  return typeof instance;
}

function matchesType(instance, type) {
  switch (type) {
    case "string":
      return typeof instance === "string";
    case "boolean":
      return typeof instance === "boolean";
    case "number":
      return typeof instance === "number";
    case "integer":
      return typeof instance === "number" && Number.isInteger(instance);
    case "object":
      return typeof instance === "object" && instance !== null && !Array.isArray(instance);
    case "array":
      return Array.isArray(instance);
    case "null":
      return instance === null;
    default:
      return false;
  }
}

function isValidCalendarDate(s) {
  const m = /^([0-9]{4})-([0-9]{2})-([0-9]{2})$/.exec(s);
  if (!m) return false;
  const [, y, mo, d] = m.map(Number);
  const dt = new Date(Date.UTC(y, mo - 1, d));
  return dt.getUTCFullYear() === y && dt.getUTCMonth() === mo - 1 && dt.getUTCDate() === d;
}

// Valida `instance` contra `schema`, empilhando mensagens de erro em `errors`.
function validateInstance(schema, instance, path, errors) {
  if (schema.const !== undefined) {
    if (!deepEqual(instance, schema.const)) {
      errors.push(`${path}: esperado const ${JSON.stringify(schema.const)}, recebido ${JSON.stringify(instance)}`);
    }
  }

  if (schema.enum !== undefined) {
    if (!schema.enum.some((v) => deepEqual(v, instance))) {
      errors.push(`${path}: valor ${JSON.stringify(instance)} não pertence ao enum ${JSON.stringify(schema.enum)}`);
    }
  }

  if (schema.type !== undefined) {
    const types = Array.isArray(schema.type) ? schema.type : [schema.type];
    if (!types.some((t) => matchesType(instance, t))) {
      errors.push(`${path}: esperado tipo ${JSON.stringify(schema.type)}, recebido ${typeOf(instance)}`);
    }
  }

  if (schema.pattern !== undefined && typeof instance === "string") {
    if (!new RegExp(schema.pattern).test(instance)) {
      errors.push(`${path}: valor '${instance}' não corresponde ao padrão ${schema.pattern}`);
    }
  }

  if (schema.minLength !== undefined && typeof instance === "string") {
    if (instance.length < schema.minLength) {
      errors.push(`${path}: comprimento ${instance.length} menor que minLength ${schema.minLength}`);
    }
  }

  if (schema.minItems !== undefined && Array.isArray(instance)) {
    if (instance.length < schema.minItems) {
      errors.push(`${path}: ${instance.length} itens, menor que minItems ${schema.minItems}`);
    }
  }

  if (schema.format === "date" && typeof instance === "string") {
    if (!isValidCalendarDate(instance)) {
      errors.push(`${path}: '${instance}' não é uma data válida no formato YYYY-MM-DD`);
    }
  }

  if (schema.required !== undefined && typeof instance === "object" && instance !== null && !Array.isArray(instance)) {
    for (const key of schema.required) {
      if (!(key in instance)) {
        errors.push(`${path}: propriedade obrigatória '${key}' ausente`);
      }
    }
  }

  if (schema.properties !== undefined && typeof instance === "object" && instance !== null && !Array.isArray(instance)) {
    for (const [key, subschema] of Object.entries(schema.properties)) {
      if (key in instance) {
        validateInstance(subschema, instance[key], `${path}.${key}`, errors);
      }
    }
  }

  if (schema.items !== undefined && Array.isArray(instance)) {
    instance.forEach((item, i) => validateInstance(schema.items, item, `${path}[${i}]`, errors));
  }

  if (schema.allOf !== undefined) {
    for (const sub of schema.allOf) validateInstance(sub, instance, path, errors);
  }

  if (schema.if !== undefined) {
    const ifErrors = [];
    validateInstance(schema.if, instance, path, ifErrors);
    if (ifErrors.length === 0 && schema.then !== undefined) {
      validateInstance(schema.then, instance, path, errors);
    }
  }

  return errors;
}

// ---------------------------------------------------------------------------
// Regra complementar (nota após schema_fonte.json, seção 5.1 do plano): comparar dois campos
// irmãos por igualdade exige $data-reference, fora do subconjunto de JSON Schema desta fase —
// por isso é aplicada aqui como código, não como keyword de schema.
// ---------------------------------------------------------------------------
function applyComplementaryRules(schemaFile, instance, errors) {
  if (schemaFile === "schema_fonte.json" && instance.estado_processamento === "CONCLUIDO") {
    const actionRef = instance.evidencia?.repository_evidence?.action_ref;
    if (actionRef !== instance.id_acao) {
      errors.push(
        `$: regra complementar (seção 5.1) — evidencia.repository_evidence.action_ref ` +
          `('${actionRef}') deve ser igual a id_acao ('${instance.id_acao}') quando estado_processamento=CONCLUIDO`
      );
    }
  }
}

// ---------------------------------------------------------------------------
// Carregamento de schemas
// ---------------------------------------------------------------------------
const SCHEMA_FILES = [
  "schema_fonte.json",
  "schema_decisao.json",
  "schema_evidencia.json",
  "schema_elemento_modelo.json",
  "schema_termo.json",
  "schema_regra.json",
];

function loadSchemas() {
  const schemas = {};
  for (const file of SCHEMA_FILES) {
    const full = join(SCHEMAS_DIR, file);
    const schema = JSON.parse(readFileSync(full, "utf8"));
    checkKnownKeywords(schema, file);
    schemas[file] = schema;
  }
  return schemas;
}

// ---------------------------------------------------------------------------
// Extração de blocos ```json ... ``` de um arquivo Markdown
// ---------------------------------------------------------------------------
function extractJsonBlocks(content) {
  const blocks = [];
  const re = /```json\r?\n([\s\S]*?)\r?\n```/g;
  let m;
  while ((m = re.exec(content)) !== null) {
    const line = content.slice(0, m.index).split("\n").length;
    blocks.push({ raw: m[1], line });
  }
  return blocks;
}

// ---------------------------------------------------------------------------
// Modo corpus — valida todos os registros reais em docs/modelagem/**
// ---------------------------------------------------------------------------
const CORPUS_ENTRIES = [
  { dir: "fontes/dossies", listDir: true, schema: "schema_fonte.json" },
  { file: "evidencias/registro_evidencias.md", schema: "schema_evidencia.json" },
  { file: "conhecimento/glossario.md", schema: "schema_termo.json" },
  { file: "conhecimento/registro_regras.md", schema: "schema_regra.json" },
  { file: "candidatos/identidades.md", schema: "schema_elemento_modelo.json" },
  { file: "candidatos/bounded_contexts.md", schema: "schema_elemento_modelo.json" },
  { file: "candidatos/invariantes.md", schema: "schema_elemento_modelo.json" },
  { file: "candidatos/ciclos_de_vida.md", schema: "schema_elemento_modelo.json" },
  { file: "candidatos/agregados.md", schema: "schema_elemento_modelo.json" },
  { file: "candidatos/fronteiras_transacionais.md", schema: "schema_elemento_modelo.json" },
  { file: "dominio/identidades_definitivas.md", schema: "schema_elemento_modelo.json" },
  { file: "dominio/bounded_contexts.md", schema: "schema_elemento_modelo.json" },
  { file: "dominio/invariantes.md", schema: "schema_elemento_modelo.json" },
  { file: "dominio/ciclos_de_vida.md", schema: "schema_elemento_modelo.json" },
  { file: "dominio/agregados.md", schema: "schema_elemento_modelo.json" },
  { file: "dominio/fronteiras_transacionais.md", schema: "schema_elemento_modelo.json" },
  { file: "decisoes/registro_decisoes.md", schema: "schema_decisao.json" },
];

function resolveFiles(entry) {
  if (entry.listDir) {
    const full = join(MODELAGEM_DIR, entry.dir);
    if (!existsSync(full)) return [];
    return readdirSync(full)
      .filter((f) => f.endsWith(".md"))
      .map((f) => join(entry.dir, f));
  }
  return [entry.file];
}

function runCorpus(schemas) {
  let total = 0;
  const problems = [];
  for (const entry of CORPUS_ENTRIES) {
    for (const relPath of resolveFiles(entry)) {
      const full = join(MODELAGEM_DIR, relPath);
      if (!existsSync(full)) continue;
      const content = readFileSync(full, "utf8");
      for (const block of extractJsonBlocks(content)) {
        total += 1;
        let instance;
        try {
          instance = JSON.parse(block.raw);
        } catch (e) {
          problems.push({ file: relPath, line: block.line, error: `JSON inválido: ${e.message}` });
          continue;
        }
        const errs = [];
        validateInstance(schemas[entry.schema], instance, "$", errs);
        applyComplementaryRules(entry.schema, instance, errs);
        if (errs.length > 0) {
          problems.push({ file: relPath, line: block.line, error: errs.join("; ") });
        }
      }
    }
  }
  return { total, problems };
}

// ---------------------------------------------------------------------------
// Modo fixtures — executa schemas/fixtures/manifest.json
// ---------------------------------------------------------------------------
function runFixtures(manifestPath, schemas) {
  const manifestFull = join(process.cwd(), manifestPath);
  const manifest = JSON.parse(readFileSync(manifestFull, "utf8"));
  const fixturesDir = dirname(manifestFull);

  let passed = 0;
  let failed = 0;
  const acceptExpected = manifest.filter((f) => f.expected === "ACCEPT").length;
  const rejectExpected = manifest.filter((f) => f.expected === "REJECT").length;
  const details = [];

  for (const entry of manifest) {
    const fixturePath = join(fixturesDir, entry.file);
    const instance = JSON.parse(readFileSync(fixturePath, "utf8"));
    const errs = [];
    validateInstance(schemas[entry.schema], instance, "$", errs);
    applyComplementaryRules(entry.schema, instance, errs);
    const actual = errs.length === 0 ? "ACCEPT" : "REJECT";
    const outcomeOk = actual === entry.expected;

    // Não basta ACCEPT/REJECT bater — para REJECT, a causa declarada em
    // expected_error_contains precisa aparecer literalmente em algum erro produzido.
    // Sem isso, uma fixture podia ser rejeitada pelo motivo errado e ainda "passar"
    // (achado do REVIEWER, seção 5.4 do plano: "produzir exatamente o resultado E o motivo").
    let reasonOk = true;
    if (entry.expected === "REJECT") {
      if (!entry.expected_error_contains) {
        reasonOk = false; // manifest incompleto é falha, não passe silenciosamente.
      } else {
        reasonOk = errs.some((e) => e.includes(entry.expected_error_contains));
      }
    }

    const ok = outcomeOk && reasonOk;
    if (ok) passed += 1;
    else failed += 1;
    details.push({
      file: entry.file,
      expected: entry.expected,
      actual,
      ok,
      outcomeOk,
      reasonOk,
      errors: errs,
      expected_reason: entry.expected_reason ?? null,
      expected_error_contains: entry.expected_error_contains ?? null,
    });
  }

  return { total: manifest.length, accept_expected: acceptExpected, reject_expected: rejectExpected, passed, failed, details };
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
function main() {
  let schemas;
  try {
    schemas = loadSchemas();
  } catch (e) {
    console.error(`ERRO: ${e.message}`);
    process.exit(1);
  }

  const manifestArg = process.argv[2];

  if (manifestArg) {
    const result = runFixtures(manifestArg, schemas);
    for (const d of result.details) {
      const mark = d.ok ? "OK" : !d.outcomeOk ? "FALHA(resultado)" : "FALHA(motivo)";
      console.log(`[${mark}] ${d.file} — esperado=${d.expected} obtido=${d.actual}`);
      if (!d.ok) {
        console.log(`        motivo esperado: ${d.expected_reason ?? "(não declarado no manifest)"}`);
        if (!d.outcomeOk) {
          console.log(`        erros produzidos: ${d.errors.join("; ") || "(nenhum)"}`);
        } else {
          console.log(
            `        substring exigida ('${d.expected_error_contains}') não apareceu em nenhum erro — ` +
              `rejeitado, mas não pela causa declarada. erros produzidos: ${d.errors.join("; ")}`
          );
        }
      }
    }
    console.log(
      `total=${result.total} accept_expected=${result.accept_expected} ` +
        `reject_expected=${result.reject_expected} passed=${result.passed} failed=${result.failed}`
    );
    process.exit(result.failed === 0 ? 0 : 1);
  } else {
    const result = runCorpus(schemas);
    for (const p of result.problems) {
      console.log(`[FALHA] ${p.file}:${p.line} — ${p.error}`);
    }
    console.log(`total=${result.total} errors=${result.problems.length}`);
    process.exit(result.problems.length === 0 ? 0 : 1);
  }
}

main();
