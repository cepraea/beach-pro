#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import {
  mkdtemp,
  mkdir,
  readFile,
  rm,
  writeFile,
} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { gzipSync, gunzipSync } from 'node:zlib';
import { executeMigration } from './migrate-history.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPOSITORY_ROOT = path.resolve(__dirname, '../..');
const POLICY_PATH = 'governance/policies/epistemic-migration-policy.json';
const OUTPUT_PATH = 'governance/artifacts/migrations/act-f00-008';
const PERSISTED_FILES = [
  { generated: 'legacy-approved-inventory.json', persisted: 'legacy-approved-inventory.json.gz', compressed: true },
  { generated: 'epistemic-migration-map.json', persisted: 'epistemic-migration-map.json', compressed: false },
  { generated: 'migrated-records.jsonl', persisted: 'migrated-records.jsonl.gz', compressed: true },
  { generated: 'unresolved-occurrences.json', persisted: 'unresolved-occurrences.json', compressed: false },
  { generated: 'migration-summary.json', persisted: 'migration-summary.json', compressed: false },
  { generated: 'regression-report.json', persisted: 'regression-report.json', compressed: false },
];

function git(args) {
  return execFileSync('git', args, {
    cwd: REPOSITORY_ROOT,
    encoding: 'utf8',
    maxBuffer: 32 * 1024 * 1024,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
}

async function annotateBaseline(outputRoot, baselineCommit) {
  for (const name of ['legacy-approved-inventory.json', 'migration-summary.json']) {
    const target = path.join(outputRoot, name);
    const document = JSON.parse(await readFile(target, 'utf8'));
    document.scan_source = 'baseline_commit';
    document.baseline_commit_verified = baselineCommit;
    await writeFile(target, `${JSON.stringify(document, null, 2)}\n`, 'utf8');
  }
}

async function persistOutputs(generatedRoot, committedRoot) {
  await mkdir(committedRoot, { recursive: true });
  for (const entry of PERSISTED_FILES) {
    const generated = await readFile(path.join(generatedRoot, entry.generated));
    const persisted = entry.compressed
      ? gzipSync(generated, { level: 9, mtime: 0 })
      : generated;
    await writeFile(path.join(committedRoot, entry.persisted), persisted);
  }
}

async function compareOutputs(generatedRoot, committedRoot) {
  const errors = [];
  for (const entry of PERSISTED_FILES) {
    const generated = await readFile(path.join(generatedRoot, entry.generated));
    const committed = await readFile(path.join(committedRoot, entry.persisted)).catch(() => null);
    if (committed === null) {
      errors.push(`${entry.persisted}: artefato ausente`);
      continue;
    }
    const restored = entry.compressed ? gunzipSync(committed) : committed;
    if (!generated.equals(restored)) errors.push(`${entry.persisted}: artefato desatualizado`);
  }
  if (errors.length > 0) throw new Error(`ARTEFATOS_DE_MIGRACAO_INVALIDOS: ${errors.join('; ')}`);
}

async function main() {
  const mode = process.argv.includes('--check') ? 'check' : 'write';
  const policy = JSON.parse(await readFile(path.join(REPOSITORY_ROOT, POLICY_PATH), 'utf8'));
  const baselineCommit = policy.baseline_commit;

  git(['cat-file', '-e', `${baselineCommit}^{commit}`]);
  const baselineRoot = await mkdtemp(path.join(os.tmpdir(), 'act-f00-008-baseline-'));

  try {
    git(['worktree', 'add', '--detach', baselineRoot, baselineCommit]);
    const policyTarget = path.join(baselineRoot, POLICY_PATH);
    await mkdir(path.dirname(policyTarget), { recursive: true });
    await writeFile(policyTarget, `${JSON.stringify(policy, null, 2)}\n`, 'utf8');

    const artifacts = await executeMigration({
      mode: 'write',
      root: baselineRoot,
      output: OUTPUT_PATH,
      policy: POLICY_PATH,
    });

    const generatedRoot = path.join(baselineRoot, OUTPUT_PATH);
    await annotateBaseline(generatedRoot, baselineCommit);
    const committedRoot = path.join(REPOSITORY_ROOT, OUTPUT_PATH);

    if (mode === 'write') await persistOutputs(generatedRoot, committedRoot);
    else await compareOutputs(generatedRoot, committedRoot);

    console.log(JSON.stringify({
      result: artifacts.summary.result,
      action_id: 'ACT-F00-008',
      mode,
      scan_source: 'baseline_commit',
      baseline_commit: baselineCommit,
      persistence: 'GZIP_DETERMINISTICO_PARA_ARTEFATOS_VOLUMOSOS',
      total_occurrences: artifacts.summary.total_occurrences,
      total_migrated: artifacts.summary.total_migrated,
      total_unresolved: artifacts.summary.total_unresolved,
    }, null, 2));
  } finally {
    try {
      git(['worktree', 'remove', '--force', baselineRoot]);
    } catch {
      await rm(baselineRoot, { recursive: true, force: true });
    }
  }
}

main().catch((error) => {
  console.error(JSON.stringify({
    result: 'ERRO_DE_MIGRACAO_HISTORICA',
    action_id: 'ACT-F00-008',
    error: error.message,
  }, null, 2));
  process.exitCode = 1;
});
