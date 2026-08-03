#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { applyTranslations, contractProjection, freezeSegments, restoreProtected, segmentMarkdown, structuralProjection, validateResult, writeJson, VALIDATION_STATUS } from './engine.mjs';

const [command, ...args] = process.argv.slice(2);
const opts = Object.fromEntries(args.reduce((acc, value, index, all) => {
  if (value.startsWith('--')) acc.push([value.slice(2), all[index + 1]]);
  return acc;
}, []));

function required(name) { if (!opts[name]) throw new Error(`Missing --${name}`); return opts[name]; }
function loadJson(file) { return JSON.parse(fs.readFileSync(file, 'utf8')); }

if (command === 'prepare') {
  const source = required('source'); const profileFile = required('profile'); const out = required('out'); const runId = required('run-id');
  const sourceBuffer = fs.readFileSync(source); const profile = loadJson(profileFile);
  const result = segmentMarkdown({ sourceBuffer, runId, profile });
  const manifest = {
    schema_version: '1.0.0', translation_run_id: runId, source_artifact: source,
    source_artifact_sha256: result.sourceHash, source_encoding: 'UTF-8', working_copy: path.join(out, 'working-copy.md'),
    target_artifact: profile.target_artifact, source_language: profile.source_language, target_language: profile.target_language,
    parser: result.parser, state: result.errors.length ? 'BLOCKED' : 'FROZEN', validation_status: result.errors.length ? 'BLOCKED' : 'NOT_RUN', error_codes: result.errors,
  };
  fs.mkdirSync(out, { recursive: true });
  fs.writeFileSync(path.join(out, 'working-copy.md'), freezeSegments(result.segments, result.sourceText), 'utf8');
  writeJson(path.join(out, 'translation-manifest.json'), manifest);
  writeJson(path.join(out, 'protected-segments.json'), { schema_version: '1.0.0', segments: result.segments });
  writeJson(path.join(out, 'structural-projection.json'), { source: structuralProjection(result.sourceText), target: null });
  writeJson(path.join(out, 'contract-projection.json'), { source: contractProjection(result.sourceText), target: null });
  writeJson(path.join(out, 'semantic-traceability.json'), { schema_version: '1.0.0', propositions: [], coverage: 0, status: 'NOT_RUN' });
  writeJson(path.join(out, 'validation-report.json'), { translation_run_id: runId, validation_status: manifest.validation_status, error_codes: manifest.error_codes, limitations: ['Revisão bilíngue independente ainda não executada.'] });
  console.log(manifest.state);
} else if (command === 'apply') {
  const source = required('source'); const profileFile = required('profile'); const runDir = required('run-dir'); const translationsFile = required('translations');
  const profile = loadJson(profileFile); const manifest = loadJson(path.join(runDir, 'translation-manifest.json'));
  const protectedData = loadJson(path.join(runDir, 'protected-segments.json'));
  const translations = loadJson(translationsFile);
  const frozen = fs.readFileSync(path.join(runDir, 'working-copy.md'), 'utf8');
  const applied = applyTranslations({ frozenText: frozen, segments: protectedData.segments, translations });
  const restored = restoreProtected({ translatedText: applied.output, segments: protectedData.segments });
  const targetText = restored.output; fs.mkdirSync(path.dirname(profile.target_artifact), { recursive: true }); fs.writeFileSync(profile.target_artifact, targetText, 'utf8');
  const validation = validateResult({ sourceBuffer: fs.readFileSync(source), targetText, profile, manifest });
  const errors = [...applied.errors, ...restored.errors];
  const status = errors.length ? VALIDATION_STATUS.BLOCKED : validation.validation_status;
  writeJson(path.join(runDir, 'structural-projection.json'), { source: validation.source_structural_projection, target: validation.target_structural_projection });
  writeJson(path.join(runDir, 'contract-projection.json'), { source: validation.source_contract_projection, target: validation.target_contract_projection });
  writeJson(path.join(runDir, 'validation-report.json'), { translation_run_id: manifest.translation_run_id, validation_status: status, error_codes: [...new Set([...validation.error_codes, ...errors.map((e) => e.code)])], limitations: ['Equivalência proposicional depende de revisão bilíngue independente.'] });
  manifest.state = status === 'PASS' ? 'VALIDATED' : 'BLOCKED'; manifest.validation_status = status; manifest.error_codes = loadJson(path.join(runDir, 'validation-report.json')).error_codes;
  writeJson(path.join(runDir, 'translation-manifest.json'), manifest);
  console.log(status);
} else {
  console.error('Usage: cli.mjs prepare|apply ...'); process.exitCode = 2;
}
