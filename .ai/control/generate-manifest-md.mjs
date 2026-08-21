#!/usr/bin/env node
import fs from "node:fs";

const manifest = JSON.parse(fs.readFileSync("manifest.json","utf8"));
const lines = [
  "# Inventário do repositório (manifest)",
  "",
  "> **Fonte estruturada autoritativa:** [`manifest.json`](./manifest.json).",
  "> Este arquivo é uma visão humana derivada; não deve ser editado independentemente.",
  "",
  `Projeto: **${manifest.project}**`,
  `Versão do inventário: **${manifest.version}**`,
  `Atualizado em: **${manifest.updated_at}**`,
  "",
  "| Path | Tipo | Status | Consumidores | Propósito |",
  "| --- | --- | --- | --- | --- |",
];

for (const a of manifest.assets) {
  lines.push(`| \`${a.path}\` | ${a.type} | ${a.status} | ${(a.consumers??[]).join(", ")} | ${String(a.purpose).replace(/\|/g,"\\|")} |`);
}

lines.push("");
lines.push("## Regra de manutenção");
lines.push("");
lines.push("1. Atualize `manifest.json`.");
lines.push("2. Execute `node .ai/control/generate-manifest-md.mjs`.");
lines.push("3. Execute `node .ai/control/validate-control-plane.mjs`.");
lines.push("");

fs.writeFileSync("manifest.md", lines.join("\n"));
console.log("manifest.md generated");
