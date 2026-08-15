#!/usr/bin/env node
// Resolve action_ref (AC-NNN/SEM-NNN/SYN-NNN) para commits reais e verifica a imutabilidade de
// `main` — seção 4.7, 4.9 e 13 (itens 4, 15) de PLANO_CEPRAEA_Modelo_Canonico_FINAL.md.
//
// Usa exclusivamente subcomandos Git de inspeção (status, diff, log, show, rev-parse, ls-files —
// AGENT_POLICY.md, RB-SHARED-001). Nunca invoca `git merge-base`: o hook do devcontainer bloqueia
// comandos Git fora dessa lista para o EXECUTOR ("Git privilegiado pertence a Davi"). Verificações
// de ancestralidade usam `git log --format=%H <ref>` e checam presença de SHA na lista, não
// `merge-base --is-ancestor`.
//
// Uso:
//   node verificar_repositorio.mjs                 varredura completa: todos os action_ref do
//                                                   corpus, branch atual, main inalterada
//   node verificar_repositorio.mjs AC-001           resolve um único action_ref

import { readFileSync, readdirSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const SCHEMAS_DIR = dirname(fileURLToPath(import.meta.url));
const MODELAGEM_DIR = dirname(SCHEMAS_DIR);

function git(args) {
  return execFileSync("git", args, { cwd: MODELAGEM_DIR, encoding: "utf8" }).trim();
}

function readReadmeVars() {
  const content = readFileSync(join(MODELAGEM_DIR, "README.md"), "utf8");
  const vars = {};
  const rowRe = /^\|\s*`([a-z_]+)`\s*\|\s*(.+?)\s*\|$/gm;
  let m;
  while ((m = rowRe.exec(content)) !== null) {
    const valMatch = m[2].match(/`([^`]+)`/);
    vars[m[1]] = valMatch ? valMatch[1] : m[2].trim();
  }
  return vars;
}

function extractJsonBlocks(content) {
  const blocks = [];
  const re = /```json\r?\n([\s\S]*?)\r?\n```/g;
  let m;
  while ((m = re.exec(content)) !== null) {
    try {
      blocks.push(JSON.parse(m[1]));
    } catch {
      // JSON malformado é responsabilidade de validar.mjs.
    }
  }
  return blocks;
}

function readFileIfExists(relPath) {
  const full = join(MODELAGEM_DIR, relPath);
  return existsSync(full) ? readFileSync(full, "utf8") : "";
}

function allCorpusFiles() {
  const fixed = [
    "evidencias/registro_evidencias.md",
    "conhecimento/glossario.md",
    "conhecimento/registro_regras.md",
    "decisoes/registro_decisoes.md",
    "candidatos/identidades.md",
    "candidatos/bounded_contexts.md",
    "candidatos/invariantes.md",
    "candidatos/ciclos_de_vida.md",
    "candidatos/agregados.md",
    "candidatos/fronteiras_transacionais.md",
    "dominio/identidades_definitivas.md",
    "dominio/bounded_contexts.md",
    "dominio/invariantes.md",
    "dominio/ciclos_de_vida.md",
    "dominio/agregados.md",
    "dominio/fronteiras_transacionais.md",
  ];
  const dossiesDir = join(MODELAGEM_DIR, "fontes/dossies");
  const dossies = existsSync(dossiesDir)
    ? readdirSync(dossiesDir)
        .filter((f) => f.endsWith(".md"))
        .map((f) => `fontes/dossies/${f}`)
    : [];
  return [...fixed, ...dossies];
}

// Coleta todo action_ref citado em evidencia.repository_evidence.action_ref (e variantes de
// nível superior, para schema_fonte.json) em todo o corpus.
function collectActionRefs() {
  const refs = new Set();
  for (const relPath of allCorpusFiles()) {
    const content = readFileIfExists(relPath);
    if (!content) continue;
    for (const instance of extractJsonBlocks(content)) {
      const ref = instance?.evidencia?.repository_evidence?.action_ref;
      if (ref) refs.add(ref);
    }
  }
  return [...refs].sort();
}

function resolveActionRef(actionRef, baseSha, branch) {
  let log;
  try {
    log = git(["log", "--format=%H%x1f%s", `${baseSha}..${branch}`]);
  } catch (e) {
    return { status: "ERRO", detail: `git log falhou: ${e.message}` };
  }
  const commits = log
    ? log.split("\n").map((line) => {
        const [sha, subject] = line.split("\x1f");
        return { sha, subject };
      })
    : [];
  const matches = commits.filter((c) => c.subject.startsWith(`${actionRef} `));
  if (matches.length === 0) return { status: "AUSENTE", detail: "nenhum commit com este subject na branch da fase" };
  if (matches.length > 1) return { status: "DUPLICADO", detail: matches.map((m) => m.sha.slice(0, 10)).join(", ") };
  return { status: "RESOLVIDO", detail: matches[0].sha };
}

function isAncestor(ancestorRef, descendantRef) {
  let ancestorSha;
  try {
    ancestorSha = git(["rev-parse", ancestorRef]);
  } catch {
    return false;
  }
  const list = git(["log", "--format=%H", descendantRef]).split("\n").filter(Boolean);
  return list.includes(ancestorSha);
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
function main() {
  const vars = readReadmeVars();
  const { base_sha: baseSha, branch_modelagem: branch, main_sha_before: mainShaBefore } = vars;

  if (!baseSha || !branch) {
    console.error("ERRO: base_sha ou branch_modelagem não encontrados em README.md.");
    process.exit(1);
  }

  const singleRef = process.argv[2];

  if (singleRef) {
    const result = resolveActionRef(singleRef, baseSha, branch);
    console.log(`${singleRef}: ${result.status} — ${result.detail}`);
    process.exit(result.status === "RESOLVIDO" ? 0 : 1);
  }

  let exitCode = 0;

  // Branch atual deve ser exatamente a branch da fase.
  const currentBranch = git(["rev-parse", "--abbrev-ref", "HEAD"]);
  if (currentBranch !== branch) {
    console.log(`[FALHA] branch atual '${currentBranch}' difere de branch_modelagem '${branch}'`);
    exitCode = 1;
  } else {
    console.log(`[OK] branch atual é '${branch}'`);
  }

  // BASE_SHA deve ser ancestral da branch da fase.
  if (isAncestor(baseSha, branch)) {
    console.log(`[OK] base_sha '${baseSha.slice(0, 10)}' é ancestral de '${branch}'`);
  } else {
    console.log(`[FALHA] base_sha '${baseSha.slice(0, 10)}' NÃO é ancestral de '${branch}'`);
    exitCode = 1;
  }

  // main não deve ter se movido.
  if (mainShaBefore) {
    const mainNow = git(["rev-parse", "main"]);
    if (mainNow === mainShaBefore) {
      console.log(`[OK] main permanece em '${mainShaBefore.slice(0, 10)}'`);
    } else {
      console.log(`[FALHA] main mudou: era '${mainShaBefore.slice(0, 10)}', agora é '${mainNow.slice(0, 10)}'`);
      exitCode = 1;
    }
  }

  // Resolve todo action_ref citado no corpus.
  const refs = collectActionRefs();
  let ausentes = 0;
  let duplicados = 0;
  for (const ref of refs) {
    const result = resolveActionRef(ref, baseSha, branch);
    const mark = result.status === "RESOLVIDO" ? "OK" : "FALHA";
    console.log(`[${mark}] ${ref}: ${result.status} — ${result.detail}`);
    if (result.status === "AUSENTE") ausentes += 1;
    if (result.status === "DUPLICADO") duplicados += 1;
  }
  if (ausentes > 0 || duplicados > 0) exitCode = 1;

  console.log(`action_refs=${refs.length} ausentes=${ausentes} duplicados=${duplicados}`);
  process.exit(exitCode);
}

main();
