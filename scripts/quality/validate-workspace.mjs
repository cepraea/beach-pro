import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = process.cwd();
const errors = [];

function read(path) {
  return readFileSync(resolve(root, path), 'utf8');
}

function readJson(path) {
  try {
    return JSON.parse(read(path));
  } catch (error) {
    errors.push(`${path}: JSON inválido (${error.message})`);
    return {};
  }
}

function check(condition, message) {
  if (!condition) {
    errors.push(message);
  }
}

const packageJson = readJson('package.json');
const workspace = readJson('cepraea-beach-pro.code-workspace');
const settings = readJson('.vscode/settings.json');
const extensions = readJson('.vscode/extensions.json');
const tasks = readJson('.vscode/tasks.json');
const launch = readJson('.vscode/launch.json');
const envExample = read('.env.example');
const nvmVersion = read('.nvmrc').trim();
const viteConfig = read('vite.config.ts');

check(
  workspace.folders?.length === 1 && workspace.folders[0]?.path === '.',
  'O Workspace deve apontar exclusivamente para a raiz do projeto.',
);
check(
  Object.keys(workspace).every((key) => key === 'folders'),
  'Configurações e extensões devem ficar em .vscode, não duplicadas no Workspace.',
);
check(
  settings['typescript.tsdk'] === 'node_modules/typescript/lib',
  'O VS Code deve usar o TypeScript instalado no projeto.',
);
check(settings['editor.formatOnSave'] === true, 'A formatação ao salvar deve estar ativa.');
check(
  extensions.recommendations?.includes('davidanson.vscode-markdownlint'),
  'Markdownlint deve constar nas extensões recomendadas.',
);

const scripts = packageJson.scripts ?? {};
const requiredScripts = [
  'assets:pwa',
  'dev',
  'build',
  'preview',
  'lint',
  'lint:md',
  'lint:md:vscode',
  'quality:workspace',
  'format',
  'format:check',
  'typecheck',
  'test',
  'test:watch',
  'validate',
];
for (const script of requiredScripts) {
  check(Boolean(scripts[script]), `O script obrigatório "${script}" não existe.`);
}

for (const task of tasks.tasks ?? []) {
  if (task.type === 'npm') {
    check(Boolean(scripts[task.script]), `A tarefa "${task.label}" referencia o script inexistente.`);
  }
}

const taskLabels = new Set((tasks.tasks ?? []).map((task) => task.label));
for (const configuration of launch.configurations ?? []) {
  if (configuration.preLaunchTask) {
    check(
      taskLabels.has(configuration.preLaunchTask),
      `A depuração referencia a tarefa inexistente "${configuration.preLaunchTask}".`,
    );
  }
  check(
    configuration.url === 'http://localhost:5173',
    `A depuração "${configuration.name}" deve usar http://localhost:5173.`,
  );
}

check(/port:\s*5173/.test(viteConfig), 'O Vite deve usar a porta 5173.');
check(/host:\s*true/.test(viteConfig), 'O Vite deve aceitar conexões de rede com host: true.');
check(packageJson.engines?.node === nvmVersion, '.nvmrc e package.json#engines.node divergem.');
check(
  packageJson.engines?.npm === '11.11.0',
  'package.json#engines.npm deve fixar a versão 11.11.0.',
);
check(
  packageJson.packageManager === 'npm@11.11.0',
  'package.json#packageManager deve fixar npm@11.11.0.',
);
check(
  !scripts.test?.includes('passWithNoTests'),
  'A porta de testes não pode aprovar um projeto sem arquivos de teste.',
);

const expectedEnvironmentVariables = [
  'VITE_APP_NAME',
  'VITE_SUPABASE_URL',
  'VITE_SUPABASE_ANON_KEY',
  'VITE_ENABLE_OFFLINE',
];
const declaredEnvironmentVariables = envExample
  .split(/\r?\n/)
  .filter((line) => line && !line.startsWith('#'))
  .map((line) => line.split('=', 1)[0]);

check(
  JSON.stringify(declaredEnvironmentVariables) === JSON.stringify(expectedEnvironmentVariables),
  '.env.example não corresponde ao contrato canônico de variáveis públicas.',
);
check(
  !envExample.toLowerCase().includes('service_role'),
  '.env.example não pode conter chave service_role.',
);

for (const size of [192, 512]) {
  const path = `public/icons/icon-${size}x${size}.png`;
  try {
    const icon = readFileSync(resolve(root, path));
    check(icon.subarray(1, 4).toString('ascii') === 'PNG', `${path} não é um arquivo PNG.`);
    check(
      icon.readUInt32BE(16) === size && icon.readUInt32BE(20) === size,
      `${path} não possui dimensões ${size} x ${size}.`,
    );
  } catch (error) {
    errors.push(`${path}: ícone obrigatório indisponível (${error.message})`);
  }
}

if (errors.length > 0) {
  console.error('Validação do Workspace reprovada:');
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exitCode = 1;
} else {
  console.log('Validação do Workspace aprovada.');
}
