#!/usr/bin/env node
// Percorre 100% das referências cruzadas do corpus de modelagem CEPRAEA-BEACH-PRO e reporta
// órfãos — seção 4.3/4.7 e seção 13 (itens 3, 5-11) de PLANO_CEPRAEA_Modelo_Canonico_FINAL.md.
//
// Cadeia verificada: SRC → EVD → TERMO/REGRA/elemento(candidatos→dominio) → logico.
//
// Uso: node verificar_referencias.mjs
// Saída: lista de órfãos (se houver) e uma linha final "orfaos=N"; exit 0 se N=0, senão 1.

import { readFileSync, readdirSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const SCHEMAS_DIR = dirname(fileURLToPath(import.meta.url));
const MODELAGEM_DIR = dirname(SCHEMAS_DIR);

function extractJsonBlocks(content) {
  const blocks = [];
  const re = /```json\r?\n([\s\S]*?)\r?\n```/g;
  let m;
  while ((m = re.exec(content)) !== null) {
    const line = content.slice(0, m.index).split("\n").length;
    try {
      blocks.push({ instance: JSON.parse(m[1]), line });
    } catch {
      // JSON malformado é responsabilidade de validar.mjs, não deste script.
    }
  }
  return blocks;
}

function readFileIfExists(relPath) {
  const full = join(MODELAGEM_DIR, relPath);
  return existsSync(full) ? readFileSync(full, "utf8") : "";
}

function blocksOf(relPath) {
  const content = readFileIfExists(relPath);
  return content ? extractJsonBlocks(content).map((b) => ({ ...b, file: relPath })) : [];
}

function dossieBlocks() {
  const dir = join(MODELAGEM_DIR, "fontes/dossies");
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((f) => f.endsWith(".md"))
    .flatMap((f) => blocksOf(`fontes/dossies/${f}`));
}

const ELEMENTO_FILES = {
  candidatos: [
    "candidatos/identidades.md",
    "candidatos/bounded_contexts.md",
    "candidatos/invariantes.md",
    "candidatos/ciclos_de_vida.md",
    "candidatos/agregados.md",
    "candidatos/fronteiras_transacionais.md",
  ],
  dominio: [
    "dominio/identidades_definitivas.md",
    "dominio/bounded_contexts.md",
    "dominio/invariantes.md",
    "dominio/ciclos_de_vida.md",
    "dominio/agregados.md",
    "dominio/fronteiras_transacionais.md",
  ],
};

// ---------------------------------------------------------------------------
// Coleta
// ---------------------------------------------------------------------------
const orfaos = [];

function reportar(tipo, ref, arquivo, linha, motivo) {
  orfaos.push({ tipo, ref, arquivo, linha, motivo });
}

const fontes = new Map(); // id_fonte -> { id_acao, file, line }
for (const b of dossieBlocks()) {
  if (b.instance.id_fonte) fontes.set(b.instance.id_fonte, { id_acao: b.instance.id_acao, file: b.file, line: b.line });
}

const evidencias = new Map(); // id_evidencia -> { id_fonte, id_acao, file, line }
for (const b of blocksOf("evidencias/registro_evidencias.md")) {
  if (b.instance.id_evidencia) {
    evidencias.set(b.instance.id_evidencia, {
      id_fonte: b.instance.id_fonte,
      id_acao: b.instance.id_acao,
      file: b.file,
      line: b.line,
    });
  }
}

const termos = blocksOf("conhecimento/glossario.md");
const regras = blocksOf("conhecimento/registro_regras.md");

const elementos = [
  ...ELEMENTO_FILES.candidatos.flatMap((f) => blocksOf(f)),
  ...ELEMENTO_FILES.dominio.flatMap((f) => blocksOf(f)),
];

const decisoes = new Map();
for (const b of blocksOf("decisoes/registro_decisoes.md")) {
  if (b.instance.id_decisao) decisoes.set(b.instance.id_decisao, { file: b.file, line: b.line });
}

// ---------------------------------------------------------------------------
// EVD → SRC / AC
// ---------------------------------------------------------------------------
for (const [id, evd] of evidencias) {
  if (!evd.id_fonte || !fontes.has(evd.id_fonte)) {
    reportar("EVD->SRC", id, evd.file, evd.line, `id_fonte '${evd.id_fonte}' não encontrado em fontes/dossies/`);
  } else {
    const fonte = fontes.get(evd.id_fonte);
    if (fonte.id_acao && evd.id_acao && fonte.id_acao !== evd.id_acao) {
      reportar(
        "EVD->AC",
        id,
        evd.file,
        evd.line,
        `id_acao '${evd.id_acao}' diverge do id_acao '${fonte.id_acao}' registrado para ${evd.id_fonte}`
      );
    }
  }
}

// ---------------------------------------------------------------------------
// TERMO.fonte / REGRA.fonte → EVD (sempre EVD-NNNN, sem exceção REF:)
// ---------------------------------------------------------------------------
function verificarFonteEvd(blocks, tipo) {
  for (const b of blocks) {
    const id = b.instance[tipo === "TERMO" ? "id_termo" : "id_regra"];
    for (const ref of b.instance.fonte ?? []) {
      if (!evidencias.has(ref)) {
        reportar(`${tipo}.fonte->EVD`, id, b.file, b.line, `fonte '${ref}' não encontrada em evidencias/registro_evidencias.md`);
      }
    }
  }
}
verificarFonteEvd(termos, "TERMO");
verificarFonteEvd(regras, "REGRA");

// ---------------------------------------------------------------------------
// elemento.fonte → EVD (ou REF: — permitido sem checagem de existência)
// ---------------------------------------------------------------------------
for (const b of elementos) {
  const id = b.instance.id_elemento;
  for (const ref of b.instance.fonte ?? []) {
    if (ref.startsWith("REF:")) continue;
    if (!evidencias.has(ref)) {
      reportar("elemento.fonte->EVD", id, b.file, b.line, `fonte '${ref}' não encontrada em evidencias/registro_evidencias.md`);
    }
  }
}

// ---------------------------------------------------------------------------
// elemento.bounded_context_id → CTX existente (elemento tipo=BOUNDED_CONTEXT é o próprio)
// ---------------------------------------------------------------------------
const ctxIds = new Set(elementos.filter((b) => b.instance.tipo === "BOUNDED_CONTEXT").map((b) => b.instance.id_elemento));
for (const b of elementos) {
  const bcId = b.instance.bounded_context_id;
  if (bcId && !ctxIds.has(bcId)) {
    reportar("elemento->CTX", b.instance.id_elemento, b.file, b.line, `bounded_context_id '${bcId}' não encontrado entre os BOUNDED_CONTEXT registrados`);
  }
}

// ---------------------------------------------------------------------------
// Rotas de promoção — candidatos/ <-> dominio/ (seção 4.7, INV-PROC-003/004)
// ---------------------------------------------------------------------------
const porIdEstagio = new Map(); // id_elemento -> [{estagio, file, line, instance}]
for (const b of elementos) {
  const id = b.instance.id_elemento;
  if (!id) continue;
  if (!porIdEstagio.has(id)) porIdEstagio.set(id, []);
  porIdEstagio.get(id).push({ estagio: b.instance.estagio, file: b.file, line: b.line, instance: b.instance });
}

for (const [id, entradas] of porIdEstagio) {
  const dominioEntradas = entradas.filter((e) => e.estagio === "DOMINIO");
  const promovidoEntradas = entradas.filter((e) => e.estagio === "PROMOVIDO");
  const candidatoEntradas = entradas.filter((e) => e.estagio === "CANDIDATO");

  for (const d of dominioEntradas) {
    const { promoted_by, promoted_from } = d.instance;
    if (promoted_by === "PRE-SEED") {
      if (!promoted_from || !promoted_from.startsWith("REF:")) {
        reportar("DOMINIO(PRE-SEED)", id, d.file, d.line, "promoted_from deveria começar com 'REF:' na rota PRE-SEED");
      }
      continue; // ROTA B: não exige candidato correspondente.
    }
    // ROTA A: precisa existir candidato PROMOVIDO cujo promoted_to aponte exatamente para este DOMINIO.
    const match = promovidoEntradas.find((p) => p.instance.promoted_to === `${d.file}#${id}`);
    if (!match) {
      reportar("DOMINIO(ROTA A)", id, d.file, d.line, `nenhum candidato PROMOVIDO correspondente encontrado (promoted_by='${promoted_by}')`);
    }
  }

  for (const p of promovidoEntradas) {
    const promotedTo = p.instance.promoted_to;
    const alvo = dominioEntradas.some((d) => promotedTo === `${d.file}#${id}`);
    if (!alvo) {
      reportar("PROMOVIDO->DOMINIO", id, p.file, p.line, `promoted_to '${promotedTo}' não resolve para nenhum elemento DOMINIO com este id_elemento`);
    }
  }

  if (dominioEntradas.length > 0 && candidatoEntradas.length > 0) {
    reportar(
      "CANDIDATO_NAO_PROMOVIDO",
      id,
      candidatoEntradas[0].file,
      candidatoEntradas[0].line,
      `existe entrada DOMINIO para '${id}' mas o candidato original continua estagio=CANDIDATO (deveria ser PROMOVIDO)`
    );
  }
}

// ---------------------------------------------------------------------------
// dominio/modelo_canonico_dominio.md — referencia só IDs existentes em dominio/
// ---------------------------------------------------------------------------
const dominioIds = new Set(elementos.filter((b) => b.instance.estagio === "DOMINIO").map((b) => b.instance.id_elemento));
const canonicoContent = readFileIfExists("dominio/modelo_canonico_dominio.md");
if (canonicoContent) {
  const idPattern = /\b(CTX|IDN|AGG|INV|LFC|TRX)-[0-9]{3}\b/g;
  const encontrados = new Set(canonicoContent.match(idPattern) ?? []);
  for (const ref of encontrados) {
    if (!dominioIds.has(ref)) {
      reportar("modelo_canonico->dominio", ref, "dominio/modelo_canonico_dominio.md", null, `ID '${ref}' citado mas não existe em dominio/ com estagio=DOMINIO`);
    }
  }
}

// ---------------------------------------------------------------------------
// logico/modelo_logico_relacional.md — só CTX MADURA_PARA_MODELO_LOGICO, com derived_from[]
// Contrato ad-hoc (seção 6, "Contratos adicionais" — sem schema_x.json próprio):
//   { "id_elemento_logico": "...", "bounded_context_id": "CTX-NNN", "derived_from": ["..."] }
// ---------------------------------------------------------------------------
const maturidadePorCtx = new Map();
for (const b of elementos) {
  if (b.instance.tipo === "BOUNDED_CONTEXT" && b.instance.estagio === "DOMINIO") {
    maturidadePorCtx.set(b.instance.id_elemento, b.instance.maturidade);
  }
}
const todosOsIds = new Set([
  ...fontes.keys(),
  ...evidencias.keys(),
  ...termos.map((b) => b.instance.id_termo),
  ...regras.map((b) => b.instance.id_regra),
  ...elementos.map((b) => b.instance.id_elemento),
]);

for (const b of blocksOf("logico/modelo_logico_relacional.md")) {
  const id = b.instance.id_elemento_logico ?? "(sem id)";
  const bcId = b.instance.bounded_context_id;
  if (!bcId || maturidadePorCtx.get(bcId) !== "MADURA_PARA_MODELO_LOGICO") {
    reportar("logico->CTX_maduro", id, b.file, b.line, `bounded_context_id '${bcId}' não é um CTX-NNN em DOMINIO com maturidade=MADURA_PARA_MODELO_LOGICO`);
  }
  const derivedFrom = b.instance.derived_from ?? [];
  if (derivedFrom.length === 0) {
    reportar("logico.derived_from", id, b.file, b.line, "derived_from[] vazio ou ausente (INV-PROC-009)");
  }
  for (const ref of derivedFrom) {
    if (!todosOsIds.has(ref)) {
      reportar("logico.derived_from->id", id, b.file, b.line, `derived_from referencia '${ref}', que não existe no corpus`);
    }
  }
}

// ---------------------------------------------------------------------------
// logico/areas_pendentes.md — contrato ad-hoc:
//   { "bounded_context_id": "CTX-NNN", "maturidade": "...", "blocking_ids": [...],
//     "blocking_reason": "...", "required_resolution": "..." }
// ---------------------------------------------------------------------------
for (const b of blocksOf("logico/areas_pendentes.md")) {
  const bcId = b.instance.bounded_context_id ?? "(sem bounded_context_id)";
  if (!bcId || !ctxIds.has(bcId)) {
    reportar("areas_pendentes->CTX", bcId, b.file, b.line, `bounded_context_id '${bcId}' não existe entre os BOUNDED_CONTEXT registrados`);
  }
  if (!b.instance.blocking_reason) reportar("areas_pendentes.blocking_reason", bcId, b.file, b.line, "blocking_reason ausente");
  if (!b.instance.required_resolution) reportar("areas_pendentes.required_resolution", bcId, b.file, b.line, "required_resolution ausente");
  for (const ref of b.instance.blocking_ids ?? []) {
    if (!todosOsIds.has(ref)) {
      reportar("areas_pendentes.blocking_ids->id", bcId, b.file, b.line, `blocking_ids referencia '${ref}', que não existe no corpus`);
    }
  }
}

// ---------------------------------------------------------------------------
// Saída
// ---------------------------------------------------------------------------
for (const o of orfaos) {
  const loc = o.linha ? `${o.arquivo}:${o.linha}` : o.arquivo;
  console.log(`[ORFAO] ${o.tipo} '${o.ref}' em ${loc} — ${o.motivo}`);
}
console.log(`orfaos=${orfaos.length}`);
process.exit(orfaos.length === 0 ? 0 : 1);
