#!/usr/bin/env node
import { writeFile } from 'node:fs/promises';
import {
  canonicalHash,
  canonicalize,
  loadPolicy,
  readJson,
  routeAction,
  validateDocument,
} from './runtime.mjs';

function usage() {
  console.error(`Uso:
  governance validate <schema> <arquivo.json>
  governance route <acao.json>
  governance canonicalize <arquivo.json> [saida.json]
  governance hash <arquivo.json>`);
}

async function main() {
  const [command, ...args] = process.argv.slice(2);
  if (!command) {
    usage();
    process.exitCode = 2;
    return;
  }

  if (command === 'validate') {
    const [schemaName, filePath] = args;
    if (!schemaName || !filePath) throw new Error('ARGUMENTOS_INSUFICIENTES');
    const value = await readJson(filePath);
    const errors = await validateDocument(schemaName, value);
    if (errors.length > 0) {
      console.error(JSON.stringify({ result: 'VALIDACAO_ESTRUTURAL_NAO_CONFORME', errors }, null, 2));
      process.exitCode = 1;
      return;
    }
    console.log(JSON.stringify({ result: 'VALIDACAO_ESTRUTURAL_CONFORME', schema: schemaName, file: filePath }, null, 2));
    return;
  }

  if (command === 'route') {
    const [filePath] = args;
    if (!filePath) throw new Error('ARGUMENTOS_INSUFICIENTES');
    const action = await readJson(filePath);
    const policy = await loadPolicy('routing-rules.json');
    console.log(JSON.stringify(routeAction(action, policy), null, 2));
    return;
  }

  if (command === 'canonicalize') {
    const [filePath, outputPath] = args;
    if (!filePath) throw new Error('ARGUMENTOS_INSUFICIENTES');
    const value = await readJson(filePath);
    const profile = await loadPolicy('canonicalization-profile.json');
    const result = `${canonicalize(value, profile)}\n`;
    if (outputPath) await writeFile(outputPath, result, 'utf8');
    else process.stdout.write(result);
    return;
  }

  if (command === 'hash') {
    const [filePath] = args;
    if (!filePath) throw new Error('ARGUMENTOS_INSUFICIENTES');
    const value = await readJson(filePath);
    const profile = await loadPolicy('canonicalization-profile.json');
    console.log(JSON.stringify({ content_hash: canonicalHash(value, profile), file: filePath }, null, 2));
    return;
  }

  usage();
  process.exitCode = 2;
}

main().catch((error) => {
  console.error(JSON.stringify({ result: 'ERRO_DE_EXECUCAO', error: error.message }, null, 2));
  process.exitCode = 1;
});
