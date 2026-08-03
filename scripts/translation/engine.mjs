import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import MarkdownIt from 'markdown-it';

const require = createRequire(import.meta.url);
const parserVersion = require('markdown-it/package.json').version;
if (parserVersion !== '14.3.0') {
  throw new Error(`E_PARSER_VERSION_MISMATCH: expected 14.3.0, got ${parserVersion}`);
}

export const PARSER_CONFIG = Object.freeze({
  package: 'markdown-it',
  version: '14.3.0',
  preset: 'default',
  options: Object.freeze({ html: true, breaks: false, linkify: false, typographer: false }),
});

export const CLASSIFICATION = Object.freeze({
  PROTECTED_EXACT: 'PROTECTED_EXACT',
  TRANSLATABLE_CONTROLLED: 'TRANSLATABLE_CONTROLLED',
  MARKDOWN_SYNTAX: 'MARKDOWN_SYNTAX',
  AMBIGUOUS: 'AMBIGUOUS',
});

export const VALIDATION_STATUS = Object.freeze({
  NOT_RUN: 'NOT_RUN', PASS: 'PASS', FAIL: 'FAIL', BLOCKED: 'BLOCKED',
});

export const ERROR_CODE = Object.freeze({
  SOURCE_NOT_FIXED: 'E_SOURCE_NOT_FIXED',
  PARSE_FAILED: 'E_PARSE_FAILED',
  UNCOVERED_SOURCE_BYTES: 'E_UNCOVERED_SOURCE_BYTES',
  UNCLASSIFIED_SEGMENT: 'E_UNCLASSIFIED_SEGMENT',
  UNKNOWN_FIELD: 'E_UNKNOWN_FIELD',
  UNKNOWN_CLASS: 'E_UNKNOWN_CLASS',
  CLASSIFICATION_CONFLICT: 'E_CLASSIFICATION_CONFLICT',
  PLACEHOLDER_MISSING: 'E_PLACEHOLDER_MISSING',
  PLACEHOLDER_DUPLICATED: 'E_PLACEHOLDER_DUPLICATED',
  PLACEHOLDER_COLLISION: 'E_PLACEHOLDER_COLLISION',
  PROTECTED_VALUE_CHANGED: 'E_PROTECTED_VALUE_CHANGED',
  LOGICAL_POSITION_CHANGED: 'E_LOGICAL_POSITION_CHANGED',
  CARDINALITY_CHANGED: 'E_CARDINALITY_CHANGED',
  ASSOCIATION_CHANGED: 'E_ASSOCIATION_CHANGED',
  CONTRACT_RELATION_CHANGED: 'E_CONTRACT_RELATION_CHANGED',
  SEMANTIC_SIGNATURE_CHANGED: 'E_SEMANTIC_SIGNATURE_CHANGED',
  UNMATCHED_SOURCE_PROPOSITION: 'E_UNMATCHED_SOURCE_PROPOSITION',
  TARGET_ADDITION_WITHOUT_SOURCE: 'E_TARGET_ADDITION_WITHOUT_SOURCE',
  TRANSLATION_VALUE_MISSING: 'E_TRANSLATION_VALUE_MISSING',
  JAPANESE_RESIDUAL: 'E_JAPANESE_RESIDUAL',
  SOURCE_HASH_CHANGED: 'E_SOURCE_HASH_CHANGED',
});

export function sha256(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

export function strictUtf8(buffer) {
  return new TextDecoder('utf-8', { fatal: true }).decode(buffer);
}

function byteOffsetsByLine(buffer) {
  const starts = [0];
  for (let i = 0; i < buffer.length; i += 1) if (buffer[i] === 0x0a) starts.push(i + 1);
  starts.push(buffer.length);
  return starts;
}

function classifyLine(line, state, profile) {
  const trimmed = line.trim();
  if (state.frontMatter) {
    if (trimmed === '---') return { classification: CLASSIFICATION.MARKDOWN_SYNTAX, rule: 'CR-002A' };
    const yaml = /^([A-Za-z_][A-Za-z0-9_-]*):(.*)$/.exec(line.replace(/\r?\n$/u, ''));
    if (yaml) {
      if (yaml[1] === 'description') return { classification: CLASSIFICATION.TRANSLATABLE_CONTROLLED, rule: 'CR-002B' };
      return { classification: CLASSIFICATION.PROTECTED_EXACT, rule: 'CR-002C' };
    }
    return { classification: CLASSIFICATION.PROTECTED_EXACT, rule: 'CR-002D' };
  }
  if (state.fence) {
    const info = state.fenceInfo;
    if (/^(mermaid|yaml|yml|json|gherkin|markdown|md)$/i.test(info)) {
      return { classification: CLASSIFICATION.TRANSLATABLE_CONTROLLED, rule: 'CR-004M' };
    }
    return { classification: CLASSIFICATION.PROTECTED_EXACT, rule: 'CR-004' };
  }
  if (/^\s*```/.test(line) || /^\s*~~~~/.test(line)) return { classification: CLASSIFICATION.MARKDOWN_SYNTAX, rule: 'CR-003' };
  if (/^\s*(#{1,6}|>|[-*+] |\d+[.)] |\|)/.test(line)) return { classification: CLASSIFICATION.TRANSLATABLE_CONTROLLED, rule: 'CR-010' };
  if (trimmed === '' || /^\s*([-*_])(?:\s*\1){2,}\s*$/.test(line)) return { classification: CLASSIFICATION.MARKDOWN_SYNTAX, rule: 'CR-011' };
  if (profile.protected_literals.some((literal) => line.includes(literal)) && !/[ぁ-んァ-ン一-龯]/u.test(line)) {
    return { classification: CLASSIFICATION.PROTECTED_EXACT, rule: 'CR-001' };
  }
  return { classification: CLASSIFICATION.TRANSLATABLE_CONTROLLED, rule: 'CR-012' };
}

export function segmentMarkdown({ sourceBuffer, runId, profile }) {
  const sourceText = strictUtf8(sourceBuffer);
  const sourceHash = sha256(sourceBuffer);
  const md = new MarkdownIt(PARSER_CONFIG.preset, PARSER_CONFIG.options);
  let tokens;
  try { tokens = md.parse(sourceText, {}); } catch (error) {
    return { sourceHash, sourceText, tokens: [], segments: [], errors: [ERROR_CODE.PARSE_FAILED], parserError: String(error) };
  }
  const lineStarts = byteOffsetsByLine(sourceBuffer);
  const lines = sourceText.split(/(?<=\n)/u);
  const segments = [];
  let byteCursor = 0;
  const state = { frontMatter: lines[0]?.trim() === '---', fence: false, fenceInfo: '' };
  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    const trimmed = line.trim();
    const openingFence = /^\s*(```+|~~~+)\s*([^\s]*)/.exec(line);
    const closingFence = state.fence && new RegExp(`^\\s*${state.fenceMarker[0]}{${state.fenceMarker.length},}\\s*$`).test(trimmed);
    const classification = (closingFence || (!state.fence && openingFence))
      ? { classification: CLASSIFICATION.MARKDOWN_SYNTAX, rule: 'CR-003' }
      : classifyLine(line, state, profile);
    const bytes = Buffer.from(line, 'utf8');
    const id = `SEG-${String(i + 1).padStart(6, '0')}`;
    const valueHash = sha256(bytes);
    const placeholderId = classification.classification === CLASSIFICATION.PROTECTED_EXACT
      ? `@@TR:${runId}:${id}:${valueHash.slice(0, 16)}@@`
      : null;
    segments.push({
      segment_id: id,
      source_ast_path: `document/block[${String(i + 1).padStart(4, '0')}]/line/span[0001]`,
      source_byte_start: byteCursor,
      source_byte_end: byteCursor + bytes.length,
      source_value_base64: bytes.toString('base64'),
      source_value_sha256: valueHash,
      node_type: state.fence ? 'code_fence' : (trimmed.startsWith('#') ? 'heading' : 'text'),
      classification: classification.classification,
      classification_rule_id: classification.rule,
      placeholder_id: placeholderId,
      occurrence: 1,
      relation_ids: [],
      translation_value: null,
      proposition_ids: [],
      validation_status: VALIDATION_STATUS.NOT_RUN,
      error_codes: [],
    });
    byteCursor += bytes.length;
    if (state.frontMatter && i > 0 && trimmed === '---') state.frontMatter = false;
    if (!state.fence && openingFence) {
      state.fence = true; state.fenceMarker = openingFence[1]; state.fenceInfo = openingFence[2] ?? '';
    } else if (closingFence) {
      state.fence = false; state.fenceInfo = ''; state.fenceMarker = '';
    }
  }
  const errors = [];
  if (state.fence) errors.push(ERROR_CODE.PARSE_FAILED);
  if (byteCursor !== sourceBuffer.length) errors.push(ERROR_CODE.UNCOVERED_SOURCE_BYTES);
  for (let i = 1; i < segments.length; i += 1) {
    if (segments[i - 1].source_byte_end !== segments[i].source_byte_start) errors.push(ERROR_CODE.UNCOVERED_SOURCE_BYTES);
  }
  return { sourceHash, sourceText, tokens, segments, errors, parser: PARSER_CONFIG, lineStarts };
}

export function freezeSegments(segments, sourceText) {
  let output = sourceText;
  for (const segment of [...segments].reverse()) {
    if (segment.classification !== CLASSIFICATION.PROTECTED_EXACT) continue;
    const before = Buffer.from(output, 'utf8').subarray(0, segment.source_byte_start).toString('utf8');
    const after = Buffer.from(output, 'utf8').subarray(segment.source_byte_end).toString('utf8');
    if (output.includes(segment.placeholder_id)) throw new Error(ERROR_CODE.PLACEHOLDER_COLLISION);
    output = `${before}${segment.placeholder_id}${after}`;
  }
  return output;
}

export function applyTranslations({ frozenText: _frozenText, segments, translations }) {
  const errors = [];
  const chunks = [];
  for (const segment of segments) {
    const source = Buffer.from(segment.source_value_base64, 'base64').toString('utf8');
    if (segment.classification === CLASSIFICATION.PROTECTED_EXACT) {
      chunks.push(segment.placeholder_id);
      continue;
    }
    if (segment.classification === CLASSIFICATION.TRANSLATABLE_CONTROLLED) {
      const translated = translations[segment.segment_id];
      if (typeof translated !== 'string') {
        errors.push({ segment_id: segment.segment_id, code: ERROR_CODE.TRANSLATION_VALUE_MISSING });
        chunks.push(source);
        continue;
      }
      segment.translation_value = translated;
      chunks.push(translated);
      continue;
    }
    chunks.push(source);
  }
  return { output: chunks.join(''), errors };
}

export function restoreProtected({ translatedText, segments }) {
  let output = translatedText;
  const errors = [];
  for (const segment of segments) {
    if (segment.classification !== CLASSIFICATION.PROTECTED_EXACT) continue;
    const matches = output.split(segment.placeholder_id).length - 1;
    if (matches === 0) errors.push({ segment_id: segment.segment_id, code: ERROR_CODE.PLACEHOLDER_MISSING });
    if (matches > 1) errors.push({ segment_id: segment.segment_id, code: ERROR_CODE.PLACEHOLDER_DUPLICATED });
    output = output.replace(segment.placeholder_id, Buffer.from(segment.source_value_base64, 'base64').toString('utf8'));
  }
  return { output, errors };
}

export function structuralProjection(text) {
  const lines = text.split('\n');
  const headings = lines.filter((line) => /^#{1,6}\s/.test(line)).map((line) => ({ level: line.match(/^#+/)[0].length, text: line.replace(/^#+\s*/, '') }));
  const fences = lines.filter((line) => /^\s*(```+|~~~+)/.test(line)).map((line) => line.trim());
  const tableRows = lines.filter((line) => /^\s*\|.*\|\s*$/.test(line)).length;
  const listItems = lines.filter((line) => /^\s*(?:[-*+] |\d+[.)] )/.test(line)).length;
  return { headings, fences, table_rows: tableRows, list_items: listItems };
}

export function contractProjection(text) {
  const frontmatter = /^---\n([\s\S]*?)\n---/u.exec(text)?.[1] ?? '';
  const name = /^name:\s*(.+)$/mu.exec(frontmatter)?.[1]?.trim() ?? null;
  const model = /^model:\s*(.+)$/mu.exec(frontmatter)?.[1]?.trim() ?? null;
  const tools = [...frontmatter.matchAll(/^\s*-\s*(Read|Write|Edit|Glob|Grep|Bash)\s*$/gmu)].map((m) => m[1]);
  const fileTypes = [...new Set([...text.matchAll(/`?([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`?/gu)].map((m) => m[1]))].sort();
  const mermaidNodes = [...new Set([...text.matchAll(/^\s*([A-Za-z][A-Za-z0-9_]*)\s*\[/gmu)].map((m) => m[1]))].sort();
  const mermaidEdges = [...text.matchAll(/^\s*([A-Za-z][A-Za-z0-9_]*)\s*--[^\n]*?-->[^\n]*?([A-Za-z][A-Za-z0-9_]*)/gmu)].map((m) => `${m[1]}->${m[2]}`).sort();
  return { name, model, tools, file_types: fileTypes, mermaid_nodes: mermaidNodes, mermaid_edges: mermaidEdges };
}

export function hasJapanese(text) { return /[ぁ-んァ-ン一-龯々〆ヵヶ]/u.test(text); }

export function validateResult({ sourceBuffer, targetText, profile, manifest }) {
  const errors = [];
  if (sha256(sourceBuffer) !== manifest.source_artifact_sha256) errors.push(ERROR_CODE.SOURCE_HASH_CHANGED);
  const sourceText = strictUtf8(sourceBuffer);
  const sourceStructure = structuralProjection(sourceText);
  const targetStructure = structuralProjection(targetText);
  if (JSON.stringify(sourceStructure.headings.map((h) => h.level)) !== JSON.stringify(targetStructure.headings.map((h) => h.level))) errors.push(ERROR_CODE.CARDINALITY_CHANGED);
  const sourceContract = contractProjection(sourceText);
  const targetContract = contractProjection(targetText);
  for (const key of ['name', 'model', 'tools', 'mermaid_nodes', 'mermaid_edges']) {
    if (JSON.stringify(sourceContract[key]) !== JSON.stringify(targetContract[key])) errors.push(ERROR_CODE.CONTRACT_RELATION_CHANGED);
  }
  if (!profile.allowed_japanese_residual && hasJapanese(targetText)) errors.push(ERROR_CODE.JAPANESE_RESIDUAL);
  return {
    validation_status: errors.length ? VALIDATION_STATUS.BLOCKED : VALIDATION_STATUS.PASS,
    error_codes: [...new Set(errors)],
    source_structural_projection: sourceStructure,
    target_structural_projection: targetStructure,
    source_contract_projection: sourceContract,
    target_contract_projection: targetContract,
  };
}

export function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}
