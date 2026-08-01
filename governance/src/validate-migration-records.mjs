#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { validateDocument } from './runtime.mjs';

const [filePath = 'governance/artifacts/migrations/act-f00-008/migrated-records.jsonl'] = process.argv.slice(2);

async function main() {
  const raw = await readFile(filePath, 'utf8');
  const lines = raw.split(/\r?\n/).filter((line) => line.trim().length > 0);
  if (lines.length === 0) throw new Error('MIGRACAO_SEM_REGISTROS');

  const errors = [];
  const migrationIds = new Set();
  const sourceRulePairs = new Set();

  for (const [index, line] of lines.entries()) {
    let record;
    try {
      record = JSON.parse(line);
    } catch (error) {
      errors.push(`linha ${index + 1}: JSON_INVALIDO: ${error.message}`);
      continue;
    }

    const structuralErrors = await validateDocument('legacy-migration-record.schema.json', record);
    errors.push(...structuralErrors.map((error) => `linha ${index + 1}: ${error}`));

    if (migrationIds.has(record.migration_id)) errors.push(`linha ${index + 1}: migration_id duplicado`);
    migrationIds.add(record.migration_id);

    const pair = `${record.source_record_id}:${record.migration_rule_id}`;
    if (sourceRulePairs.has(pair)) errors.push(`linha ${index + 1}: source_record_id + migration_rule_id duplicado`);
    sourceRulePairs.add(pair);
  }

  if (errors.length > 0) {
    console.error(JSON.stringify({
      result: 'VALIDACAO_ESTRUTURAL_NAO_CONFORME',
      action_id: 'ACT-F00-008',
      file: filePath,
      records: lines.length,
      errors,
    }, null, 2));
    process.exitCode = 1;
    return;
  }

  console.log(JSON.stringify({
    result: 'VALIDACAO_ESTRUTURAL_CONFORME',
    action_id: 'ACT-F00-008',
    schema: 'legacy-migration-record.schema.json',
    file: filePath,
    records: lines.length,
    duplicate_migration_ids: 0,
    duplicate_source_rule_pairs: 0,
  }, null, 2));
}

main().catch((error) => {
  console.error(JSON.stringify({ result: 'ERRO_DE_VALIDACAO_DA_MIGRACAO', error: error.message }, null, 2));
  process.exitCode = 1;
});
