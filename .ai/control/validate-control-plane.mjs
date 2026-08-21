#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { readJson, printVerdict } from "./lib.mjs";
import { validateTaskProposalFile } from "./validate-task-proposal.mjs";
import { validateTaskApprovalFiles } from "./validate-task-approval.mjs";
import { validateExecutionFiles } from "./validate-execution-result.mjs";

const root=process.cwd();
const e=[];
const exists=(p)=>fs.existsSync(path.join(root,p));
const config=readJson(path.join(root,".ai/control/control-plane.json"));

for (const p of config.required_control_files) {
  if (!exists(p)) e.push(`required control file missing: ${p}`);
}
for (const p of config.required_decision_files ?? []) {
  if (!exists(p)) e.push(`required decision file missing: ${p}`);
}
for (const p of Object.values(config.namespaces)) {
  if (!exists(p)) e.push(`canonical namespace missing: ${p}`);
}
for (const p of config.forbidden_operational_namespaces) {
  if (exists(p)) e.push(`forbidden operational namespace exists: ${p}`);
}

if (exists(".ai")) {
  const allowed = new Set(["control","decisions","tasks"]);
  for (const name of fs.readdirSync(path.join(root,".ai"))) {
    if (!allowed.has(name)) e.push(`unexpected top-level .ai entry: .ai/${name}`);
  }
}

for (const p of config.operational_sources) {
  if (!exists(p)) {
    e.push(`operational source missing: ${p}`);
    continue;
  }
  const text=fs.readFileSync(path.join(root,p),"utf8");
  for (const stale of config.stale_operational_references) {
    if (text.includes(stale)) e.push(`stale operational reference in ${p}: ${stale}`);
  }
}

for (const p of [
  ".ai/control/control-plane.json",
  ".ai/control/runbook-catalog.json",
  ".ai/control/task-proposal.schema.json",
  ".ai/control/task-approval.schema.json",
  ".ai/control/execution-result.schema.json",
  ".ai/control/verification-plan.schema.json",
  "manifest.json"
]) {
  if (!exists(p)) continue;
  try {
    JSON.parse(fs.readFileSync(path.join(root,p),"utf8"));
  } catch(err) {
    e.push(`invalid JSON ${p}: ${err.message}`);
  }
}

if (exists(".ai/control/runbook-catalog.json")) {
  const cat=readJson(path.join(root,".ai/control/runbook-catalog.json"));
  const refs=[];
  for (const cls of Object.values(cat.operation_classes??{})) {
    refs.push(...(cls.executor??[]),...(cls.reviewer??[]));
  }
  refs.push(...Object.values(cat.shared??{}));
  for (const p of [...new Set(refs)]) {
    if (!exists(p)) {
      e.push(`runbook catalog path missing: ${p}`);
      continue;
    }
    const text=fs.readFileSync(path.join(root,p),"utf8");
    for (const stale of config.stale_operational_references) {
      if (text.includes(stale)) e.push(`stale operational reference in ${p}: ${stale}`);
    }
  }
}

if (exists("manifest.json")) {
  const manifest=readJson(path.join(root,"manifest.json"));
  for (const a of manifest.assets??[]) {
    if (!exists(a.path)) e.push(`manifest asset path missing: ${a.path}`);
  }
}

const goodProposal=".ai/control/fixtures/known-good/task-proposal.example.json";
const goodApproval=".ai/control/fixtures/known-good/task-approval.example.json";
const goodExecution=".ai/control/fixtures/known-good/execution-result.example.json";

if (exists(goodProposal)) {
  e.push(...validateTaskProposalFile(path.join(root,goodProposal),root).map(x=>`known-good proposal: ${x}`));
}
if (exists(goodProposal)&&exists(goodApproval)) {
  e.push(...validateTaskApprovalFiles(
    path.join(root,goodProposal),
    path.join(root,goodApproval),
    root
  ).map(x=>`known-good approval: ${x}`));
}
if (exists(goodProposal)&&exists(goodApproval)&&exists(goodExecution)) {
  e.push(...validateExecutionFiles(
    path.join(root,goodProposal),
    path.join(root,goodApproval),
    path.join(root,goodExecution),
    root
  ).map(x=>`known-good execution: ${x}`));
}

const badProposal=".ai/control/fixtures/known-bad/task-proposal-action-orphan.json";
if (exists(badProposal) && validateTaskProposalFile(path.join(root,badProposal),root).length===0) {
  e.push("known-bad proposal unexpectedly passed");
}

const badApproval=".ai/control/fixtures/known-bad/task-approval-hash-mismatch.json";
if (exists(badApproval) && validateTaskApprovalFiles(
  path.join(root,goodProposal),
  path.join(root,badApproval),
  root
).length===0) {
  e.push("known-bad approval unexpectedly passed");
}

for (const bad of [
  ".ai/control/fixtures/known-bad/execution-result-unauthorized-change.json",
  ".ai/control/fixtures/known-bad/execution-result-simulated-evidence.json"
]) {
  if (
    exists(bad) &&
    validateExecutionFiles(
      path.join(root,goodProposal),
      path.join(root,goodApproval),
      path.join(root,bad),
      root
    ).length===0
  ) {
    e.push(`known-bad execution unexpectedly passed: ${bad}`);
  }
}

process.exitCode=printVerdict("validate-control-plane",e,{
  bootstrap_mode:config.bootstrap_mode,
  fvr_mode:config.fvr_mode
});
