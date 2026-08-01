import { execFileSync } from 'node:child_process';

try {
  execFileSync('git', ['rev-parse', '--is-inside-work-tree'], { stdio: 'ignore' });
  execFileSync('git', ['config', 'core.hooksPath', '.githooks'], { stdio: 'inherit' });
  console.log('core.hooksPath=.githooks');
} catch {
  console.error('HOOK_INSTALLATION_FAILED');
  process.exitCode = 1;
}
