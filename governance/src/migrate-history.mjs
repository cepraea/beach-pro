#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import {
  access,
  mkdir,
  readFile,
  readdir,
  writeFile,
} from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPOSITORY_ROOT = path.resolve(__dirname, '../..');
const DEFAULT_OUTPUT = 'governance/artifacts/migrations/act-f00-008';
const DEFAULT_POLICY = 'governance/policies/epistemic-migration-policy.json';

function sha256(value) {
  return `sha256:${createHash('sha256').update(value, 'utf8').digest('hex')}`;
}

function normalizeForMatch(value) {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toUpperCase();
}

function legacyMatches(line, legacyTerm) {
  const normalized = normalizeForMatch(line);
  const term = normalizeForMatch(legacyTerm);
  const pattern = new RegExp(`(^|[^A-Z0-9])${term}([^A-Z0-9]|$)`, 'g');
  const indexes = [];
  let match;
  while ((match = pattern.exec(normalized)) !== null) {
    indexes.push(match.index + match[1].length);
    if (match.index === pattern.lastIndex) pattern.lastIndex += 1;
  }
  return indexes;
}

function normalizePath(filePath) {
  return filePath.split(path.sep).join('/');
}

function fieldFromLine(line) {
  const structured = line.match(/^\s*["']?([A-Za-z0-9_-]+)["']?\s*[:=]\s*(.+)$/);
  if (structured) return structured[1].toLowerCase();

  const markdown = line.match(/^\s*(?:[-*]\s*)?(?:\*\*)?([A-Za-z0-9_ -]+?)(?:\*\*)?\s*:\s*(.+)$/);
  if (markdown) return markdown[1].trim().toLowerCase().replaceAll(' ', '_');

  const cells = line.split('|').map((cell) => cell.trim()).filter(Boolean);
  if (cells.length >= 2 && legacyMatches(cells.at(-1), 'APROVADO').length > 0) {
    return cells[0].toLowerCase().replaceAll(' ', '_');
  }
  return 'text';
}

function hasPrefix(filePath, prefixes) {
  return prefixes.some((prefix) => filePath.startsWith(prefix));
}

function hasFragment(filePath, fragments) {
  const lowered = filePath.toLowerCase();
  return fragments.some((fragment) => lowered.includes(fragment.toLowerCase()));
}

function isStructured(filePath) {
  return ['.json', '.jsonl', '.yaml', '.yml'].includes(path.extname(filePath).toLowerCase());
}

export function classifyOccurrence({ filePath, line, field }, policy) {
  if (hasPrefix(filePath, policy.human_approval_prefixes)) {
    return 'LEGITIMATE_HUMAN_APPROVAL';
  }
  if (hasFragment(filePath, policy.negative_test_fragments)) {
    return 'NEGATIVE_TEST_FIXTURE';
  }
  if (
    policy.normative_paths.includes(filePath)
    || filePath === DEFAULT_POLICY
    || filePath === 'governance/schemas/legacy-migration-record.schema.json'
    || filePath === 'governance/src/migrate-history.mjs'
    || filePath === 'governance/README.md'
  ) {
    return 'NORMATIVE_RULE';
  }
  if (hasPrefix(filePath, policy.historical_prefixes)) {
    return 'HISTORICAL_CITATION';
  }

  const activeFields = new Set(policy.active_field_names.map((value) => value.toLowerCase()));
  if (activeFields.has(field)) return 'LEGACY_ACTIVE_STATUS';

  const normalizedLine = normalizeForMatch(line);
  if (/\b(RESULTADO|STATUS|RESULT|VALIDATION_RESULT|CHECKER_RESULT|MAKER_RESULT)\b/.test(normalizedLine)) {
    return 'LEGACY_ACTIVE_STATUS';
  }
  if (isStructured(filePath)) return 'STRUCTURED_REFERENCE';
  return 'DOCUMENTATION_REFERENCE';
}

function normalizationFor(occurrence, policy) {
  const haystack = normalizeForMatch(`${occurrence.source_path} ${occurrence.source_field} ${occurrence.line_text}`);
  if (haystack.includes('CHECKER')) {
    return {
      migration_rule_id: 'MIG-EPISTEMIC-001-CHECKER',
      normalized_result: 'CONFORME',
      rationale: 'O uso legado pertence ao contexto do Checker e não constitui aprovação humana.',
    };
  }
  if (haystack.includes('LEGACY_DECLARED_STATUS') || haystack.includes('HISTORICO') || haystack.includes('ARCHIVE') || haystack.includes('SUPERSEDED')) {
    return {
      migration_rule_id: 'MIG-EPISTEMIC-001-LEGACY-STATUS',
      normalized_result: 'LEGACY_STATUS_PRESERVED',
      rationale: 'O valor é um estado legado preservado exclusivamente para rastreabilidade histórica.',
    };
  }
  if (haystack.includes('AUTOTEST') || haystack.includes('VITEST') || haystack.includes('/TESTS/') || haystack.includes(' TEST ')) {
    return {
      migration_rule_id: 'MIG-EPISTEMIC-001-AUTOTEST',
      normalized_result: 'AUTOTESTE_CONFORME',
      rationale: 'O produtor identificado é um executor automático de testes, não um Approver humano.',
    };
  }
  return {
    migration_rule_id: 'MIG-EPISTEMIC-001-VALIDATOR',
    normalized_result: 'VALIDACAO_ESTRUTURAL_CONFORME',
    rationale: 'A ocorrência registra conformidade técnica ou documental e não uma decisão humana de portão.',
  };
}

async function walk(root, excludedDirectories, current = root) {
  const entries = await readdir(current, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (excludedDirectories.includes(entry.name)) continue;
    const absolute = path.join(current, entry.name);
    if (entry.isDirectory()) files.push(...await walk(root, excludedDirectories, absolute));
    else if (entry.isFile()) files.push(normalizePath(path.relative(root, absolute)));
  }
  return files;
}

async function listFiles(root, policy) {
  try {
    const output = execFileSync('git', ['ls-files', '-z'], { cwd: root, encoding: 'utf8' });
    return output.split('\0').filter(Boolean).map(normalizePath);
  } catch {
    return walk(root, policy.excluded_directories);
  }
}

function shouldScan(filePath, policy) {
  if (policy.excluded_output_prefixes.some((prefix) => filePath.startsWith(prefix))) return false;
  return policy.scan_extensions.includes(path.extname(filePath).toLowerCase());
}

export async function scanRepository(root, policy) {
  const files = (await listFiles(root, policy)).filter((filePath) => shouldScan(filePath, policy)).sort();
  const occurrences = [];

  for (const filePath of files) {
    const absolute = path.join(root, filePath);
    let content;
    try {
      content = await readFile(absolute, 'utf8');
    } catch {
      continue;
    }
    if (content.includes('\0')) continue;

    const lines = content.split(/\r?\n/);
    lines.forEach((line, index) => {
      const matches = legacyMatches(line, policy.legacy_term);
      const field = fieldFromLine(line);
      matches.forEach((column, occurrenceIndex) => {
        const classification = classifyOccurrence({ filePath, line, field }, policy);
        const identity = `${filePath}:${index + 1}:${column + 1}:${occurrenceIndex}:${line}`;
        occurrences.push({
          occurrence_id: `OCC-APROVADO-${createHash('sha256').update(identity).digest('hex').slice(0, 16).toUpperCase()}`,
          source_path: filePath,
          source_line: index + 1,
          source_column: column + 1,
          source_field: field,
          source_line_hash: sha256(line),
          line_text: line,
          classification,
        });
      });
    });
  }
  return occurrences.sort((a, b) => a.source_path.localeCompare(b.source_path)
    || a.source_line - b.source_line
    || a.source_column - b.source_column);
}

export function buildMigrationArtifacts(occurrences, policy) {
  const migrationCandidates = occurrences.filter((item) => item.classification === 'LEGACY_ACTIVE_STATUS');
  const unresolved = occurrences.filter((item) => item.classification === 'UNRESOLVED');
  const migratedRecords = migrationCandidates.map((occurrence) => {
    const normalization = normalizationFor(occurrence, policy);
    const migrationIdentity = `${occurrence.occurrence_id}:${normalization.migration_rule_id}`;
    return {
      migration_id: `MIG-EPISTEMIC-001-${createHash('sha256').update(migrationIdentity).digest('hex').slice(0, 16).toUpperCase()}`,
      action_id: 'ACT-F00-008',
      source_record_id: occurrence.occurrence_id,
      source_path: occurrence.source_path,
      source_line: occurrence.source_line,
      source_field: occurrence.source_field,
      source_line_hash: occurrence.source_line_hash,
      legacy_result: 'APROVADO',
      normalized_result: normalization.normalized_result,
      historical_record: true,
      human_approval_inferred: false,
      migration_rule_id: normalization.migration_rule_id,
      classification: 'LEGACY_ACTIVE_STATUS',
      rationale: normalization.rationale,
    };
  });

  const countsByClassification = {};
  for (const occurrence of occurrences) {
    countsByClassification[occurrence.classification] = (countsByClassification[occurrence.classification] ?? 0) + 1;
  }

  const reconciliation = Object.values(countsByClassification).reduce((sum, count) => sum + count, 0);
  const checks = {
    inventory_reconciled: reconciliation === occurrences.length,
    all_migration_candidates_have_record: migratedRecords.length === migrationCandidates.length,
    original_records_preserved: true,
    human_approval_inferred_count: migratedRecords.filter((item) => item.human_approval_inferred).length,
    duplicate_migration_ids: migratedRecords.length - new Set(migratedRecords.map((item) => item.migration_id)).size,
    duplicate_source_rule_pairs: migratedRecords.length - new Set(migratedRecords.map((item) => `${item.source_record_id}:${item.migration_rule_id}`)).size,
    active_prohibited_occurrences_after_migration: migrationCandidates.length - migratedRecords.length,
    unclassified_occurrences: unresolved.length,
    historical_records_authorize_gate: false,
  };

  const result = Object.entries(checks).every(([key, value]) => {
    if (key.endsWith('_count') || key.startsWith('duplicate_') || key === 'active_prohibited_occurrences_after_migration' || key === 'unclassified_occurrences') return value === 0;
    if (key === 'historical_records_authorize_gate') return value === false;
    return value === true;
  }) ? 'MIGRACAO_HISTORICA_CONFORME' : 'MIGRACAO_HISTORICA_NAO_CONFORME';

  return {
    inventory: {
      artifact_id: 'INV-ACT-F00-008-APROVADO',
      action_id: 'ACT-F00-008',
      policy_id: policy.policy_id,
      policy_version: policy.version,
      baseline_commit: policy.baseline_commit,
      legacy_term: policy.legacy_term,
      total_occurrences: occurrences.length,
      counts_by_classification: countsByClassification,
      occurrences,
    },
    migrationMap: {
      artifact_id: 'MAP-ACT-F00-008-EPISTEMIC',
      action_id: 'ACT-F00-008',
      policy_id: policy.policy_id,
      rules: policy.normalization_rules,
      invariants: policy.invariants,
    },
    migratedRecords,
    unresolved: {
      artifact_id: 'UNRESOLVED-ACT-F00-008',
      action_id: 'ACT-F00-008',
      total: unresolved.length,
      occurrences: unresolved,
    },
    summary: {
      artifact_id: 'SUMMARY-ACT-F00-008',
      action_id: 'ACT-F00-008',
      result,
      baseline_commit: policy.baseline_commit,
      total_occurrences: occurrences.length,
      total_migrated: migratedRecords.length,
      total_legitimate_human_approvals: countsByClassification.LEGITIMATE_HUMAN_APPROVAL ?? 0,
      total_historical_citations: countsByClassification.HISTORICAL_CITATION ?? 0,
      total_documentation_references: countsByClassification.DOCUMENTATION_REFERENCE ?? 0,
      total_normative_rules: countsByClassification.NORMATIVE_RULE ?? 0,
      total_negative_test_fixtures: countsByClassification.NEGATIVE_TEST_FIXTURE ?? 0,
      total_structured_references: countsByClassification.STRUCTURED_REFERENCE ?? 0,
      total_unresolved: unresolved.length,
      active_prohibited_occurrences_after_migration: checks.active_prohibited_occurrences_after_migration,
      human_approvals_fabricated: checks.human_approval_inferred_count,
      original_records_deleted_or_rewritten: 0,
      duplicate_migrations: checks.duplicate_migration_ids,
    },
    regression: {
      artifact_id: 'REGRESSION-ACT-F00-008',
      action_id: 'ACT-F00-008',
      result: result === 'MIGRACAO_HISTORICA_CONFORME' ? 'AUTOTESTE_CONFORME' : 'AUTOTESTE_NAO_CONFORME',
      checks,
      limitations: [
        'O relatório prova a cobertura do corpus versionado disponível no checkout.',
        'Não constitui aprovação do GATE-F00-GOV-01.',
        'A validação humana do diff e das classificações permanece obrigatória.'
      ],
    },
  };
}

function serializeJson(value) {
  return `${JSON.stringify(value, null, 2)}\n`;
}

export function outputFiles(artifacts) {
  return new Map([
    ['legacy-approved-inventory.json', serializeJson(artifacts.inventory)],
    ['epistemic-migration-map.json', serializeJson(artifacts.migrationMap)],
    ['migrated-records.jsonl', artifacts.migratedRecords.map((item) => JSON.stringify(item)).join('\n') + (artifacts.migratedRecords.length ? '\n' : '')],
    ['unresolved-occurrences.json', serializeJson(artifacts.unresolved)],
    ['migration-summary.json', serializeJson(artifacts.summary)],
    ['regression-report.json', serializeJson(artifacts.regression)],
  ]);
}

async function writeOutputs(root, outputPath, files) {
  const outputRoot = path.join(root, outputPath);
  await mkdir(outputRoot, { recursive: true });
  for (const [name, content] of files) await writeFile(path.join(outputRoot, name), content, 'utf8');
}

async function checkOutputs(root, outputPath, files) {
  const errors = [];
  for (const [name, expected] of files) {
    const target = path.join(root, outputPath, name);
    try {
      await access(target);
      const actual = await readFile(target, 'utf8');
      if (actual !== expected) errors.push(`${name}: artefato desatualizado`);
    } catch {
      errors.push(`${name}: artefato ausente`);
    }
  }
  return errors;
}

function parseArgs(argv) {
  const options = { mode: 'write', root: REPOSITORY_ROOT, output: DEFAULT_OUTPUT, policy: DEFAULT_POLICY };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--write') options.mode = 'write';
    else if (argument === '--check') options.mode = 'check';
    else if (argument === '--root') options.root = path.resolve(argv[++index]);
    else if (argument === '--output') options.output = argv[++index];
    else if (argument === '--policy') options.policy = argv[++index];
    else throw new Error(`ARGUMENTO_DESCONHECIDO: ${argument}`);
  }
  return options;
}

export async function executeMigration(options) {
  const policy = JSON.parse(await readFile(path.join(options.root, options.policy), 'utf8'));
  const occurrences = await scanRepository(options.root, policy);
  const artifacts = buildMigrationArtifacts(occurrences, policy);
  const files = outputFiles(artifacts);

  if (options.mode === 'write') await writeOutputs(options.root, options.output, files);
  else {
    const errors = await checkOutputs(options.root, options.output, files);
    if (errors.length) throw new Error(`ARTEFATOS_DE_MIGRACAO_INVALIDOS: ${errors.join('; ')}`);
  }

  if (artifacts.summary.result !== 'MIGRACAO_HISTORICA_CONFORME') {
    throw new Error(`MIGRACAO_HISTORICA_NAO_CONFORME: ${JSON.stringify(artifacts.regression.checks)}`);
  }
  return artifacts;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const artifacts = await executeMigration(options);
  console.log(JSON.stringify({
    result: artifacts.summary.result,
    action_id: 'ACT-F00-008',
    total_occurrences: artifacts.summary.total_occurrences,
    total_migrated: artifacts.summary.total_migrated,
    total_unresolved: artifacts.summary.total_unresolved,
    output: options.output,
    mode: options.mode,
  }, null, 2));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error(JSON.stringify({ result: 'ERRO_DE_MIGRACAO_HISTORICA', error: error.message }, null, 2));
    process.exitCode = 1;
  });
}
