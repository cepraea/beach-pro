#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import {
  readJson, reqObject, reqArray, reqString, reqBool, reqEnum, reqPattern,
  relativePath, unique, topoAcyclic, printVerdict
} from "./lib.mjs";

export function validateTaskProposalObject(p, repoRoot=process.cwd()) {
  const e = [];
  if (!reqObject(p,e,"proposal")) return e;
  reqEnum(p.object_type,["task_proposal"],e,"object_type");
  reqEnum(p.schema_version,["3.0"],e,"schema_version");
  reqPattern(p.proposal_id,/^[A-Z0-9][A-Z0-9._-]{2,127}$/,e,"proposal_id");
  if (!Number.isInteger(p.revision) || p.revision < 1) e.push("revision: expected integer >= 1");
  reqString(p.task_id,e,"task_id");
  for (const k of ["title","original_instruction","goal","problem","actor","current_behavior","expected_behavior"]) reqString(p[k],e,k);

  if (reqObject(p.context,e,"context")) {
    reqString(p.context.valid,e,"context.valid");
    reqString(p.context.invalid,e,"context.invalid");
  }

  const outputs = Array.isArray(p.outputs) ? p.outputs : [];
  reqArray(p.outputs,e,"outputs",1);
  const outputIds = [];
  outputs.forEach((o,i)=>{
    if (!reqObject(o,e,`outputs[${i}]`)) return;
    reqPattern(o.output_id,/^OUT-[0-9]{3,}$/,e,`outputs[${i}].output_id`);
    reqString(o.description,e,`outputs[${i}].description`);
    outputIds.push(o.output_id);
  });
  if (!unique(outputIds)) e.push("outputs: duplicate output_id");

  reqArray(p.preconditions,e,"preconditions");
  reqArray(p.dependencies,e,"dependencies");
  reqArray(p.relevant_states,e,"relevant_states",1);
  reqArray(p.included_edge_cases,e,"included_edge_cases");

  if (reqArray(p.normative_sources,e,"normative_sources",1)) {
    p.normative_sources.forEach((s,i)=>{
      if (!reqObject(s,e,`normative_sources[${i}]`)) return;
      reqEnum(s.kind,["file","decision","human_instruction"],e,`normative_sources[${i}].kind`);
      reqString(s.ref,e,`normative_sources[${i}].ref`);
      reqString(s.locator,e,`normative_sources[${i}].locator`);
      if (s.kind === "file") {
        relativePath(s.ref,e,`normative_sources[${i}].ref`);
        const full = path.join(repoRoot,s.ref);
        if (!fs.existsSync(full)) e.push(`normative_sources[${i}]: file not found: ${s.ref}`);
      }
    });
  }

  if (reqObject(p.boundaries,e,"boundaries")) {
    for (const k of ["in_scope","allowed_actions","prohibited_actions","stop_conditions"]) reqArray(p.boundaries[k],e,`boundaries.${k}`,1);
    for (const k of ["out_of_scope","allowed_technical_autonomy"]) reqArray(p.boundaries[k],e,`boundaries.${k}`);
  }

  if (reqObject(p.three_amigos,e,"three_amigos")) {
    for (const k of ["domain_business","development","quality"]) reqString(p.three_amigos[k],e,`three_amigos.${k}`);
  }
  reqArray(p.business_rules,e,"business_rules");
  reqArray(p.decisions,e,"decisions");
  reqArray(p.constraints,e,"constraints");

  const files = Array.isArray(p.files) ? p.files : [];
  reqArray(p.files,e,"files",1);
  const targets = [];
  files.forEach((f,i)=>{
    if (!reqObject(f,e,`files[${i}]`)) return;
    relativePath(f.path,e,`files[${i}].path`);
    reqEnum(f.role,["target","reference","read_only","forbidden"],e,`files[${i}].role`);
    reqEnum(f.operation,["read","change","none"],e,`files[${i}].operation`);
    const expected = f.role === "target" ? "change" : (f.role === "forbidden" ? "none" : "read");
    if (f.operation !== expected) e.push(`files[${i}]: role=${f.role} requires operation=${expected}`);
    if (f.role === "target") targets.push(f.path);
  });
  if (!targets.length) e.push("files: at least one target is required");

  reqArray(p.pending_human_decisions,e,"pending_human_decisions");
  if (Array.isArray(p.pending_human_decisions) && p.pending_human_decisions.length) {
    e.push("pending_human_decisions: unresolved human decisions block READY_FOR_REVIEW");
  }

  if (reqObject(p.risk,e,"risk")) {
    reqEnum(p.risk.level,["verde","amarelo","vermelho","vermelho_critico"],e,"risk.level");
    if (reqArray(p.risk.natures,e,"risk.natures")) {
      p.risk.natures.forEach((n,i)=>reqEnum(n,["ui","dependencia","rls","mfa","ci","dados"],e,`risk.natures[${i}]`));
      if (!unique(p.risk.natures)) e.push("risk.natures: duplicates");
    }
    reqEnum(p.risk.blast_radius,["baixo","medio","alto"],e,"risk.blast_radius");
    reqEnum(p.risk.reversibility,["reversivel","parcial","irreversivel"],e,"risk.reversibility");
    reqString(p.risk.justification,e,"risk.justification");
  }

  if (reqObject(p.runbook_binding,e,"runbook_binding")) {
    reqEnum(p.runbook_binding.catalog_version,["1.0"],e,"runbook_binding.catalog_version");
    reqBool(p.runbook_binding.repository_baseline_required,e,"runbook_binding.repository_baseline_required");
    reqBool(p.runbook_binding.evidence_review_required,e,"runbook_binding.evidence_review_required");
    if (reqArray(p.runbook_binding.operation_classes,e,"runbook_binding.operation_classes",1)) {
      p.runbook_binding.operation_classes.forEach((c,i)=>reqEnum(c,["code_change","database_change","documentation_change","dependency_change"],e,`operation_classes[${i}]`));
      if (!unique(p.runbook_binding.operation_classes)) e.push("operation_classes: duplicates");
      try {
        const cat = readJson(path.join(repoRoot,".ai/control/runbook-catalog.json"));
        if (cat.schema_version !== p.runbook_binding.catalog_version) e.push("runbook_binding.catalog_version does not match catalog");
        for (const c of p.runbook_binding.operation_classes) if (!cat.operation_classes?.[c]) e.push(`runbook catalog missing class: ${c}`);
      } catch (err) { e.push(`runbook catalog unavailable: ${err.message}`); }
    }
  }

  const acs = Array.isArray(p.acceptance_criteria) ? p.acceptance_criteria : [];
  reqArray(p.acceptance_criteria,e,"acceptance_criteria",1);
  const acIds = [];
  acs.forEach((ac,i)=>{
    if (!reqObject(ac,e,`acceptance_criteria[${i}]`)) return;
    reqPattern(ac.criterion_id,/^AC-[0-9]{3,}$/,e,`acceptance_criteria[${i}].criterion_id`);
    acIds.push(ac.criterion_id);
    if (reqArray(ac.output_refs,e,`acceptance_criteria[${i}].output_refs`,1)) {
      for (const out of ac.output_refs) if (!outputIds.includes(out)) e.push(`${ac.criterion_id}: unresolved output_ref ${out}`);
    }
    for (const k of ["condition","method","expected"]) reqString(ac[k],e,`${ac.criterion_id}.${k}`);
    reqEnum(ac.verification_owner,["deterministic","reviewer","human"],e,`${ac.criterion_id}.verification_owner`);
  });
  if (!unique(acIds)) e.push("acceptance_criteria: duplicate criterion_id");

  const actions = Array.isArray(p.actions) ? p.actions : [];
  reqArray(p.actions,e,"actions",1);
  const actionIds = [];
  const edges = new Map();
  const acCoverage = new Map(acIds.map(x=>[x,0]));
  actions.forEach((a,i)=>{
    if (!reqObject(a,e,`actions[${i}]`)) return;
    reqPattern(a.action_id,/^A-[0-9]{3,}$/,e,`actions[${i}].action_id`);
    actionIds.push(a.action_id);
    for (const k of ["action","purpose"]) reqString(a[k],e,`${a.action_id}.${k}`);
    reqArray(a.depends_on,e,`${a.action_id}.depends_on`);
    reqArray(a.acceptance_criteria_refs,e,`${a.action_id}.acceptance_criteria_refs`,1);
    reqArray(a.target_files,e,`${a.action_id}.target_files`,1);
    reqArray(a.expected_evidence,e,`${a.action_id}.expected_evidence`,1);
    edges.set(a.action_id,a.depends_on ?? []);
    for (const ac of a.acceptance_criteria_refs ?? []) {
      if (!acIds.includes(ac)) e.push(`${a.action_id}: unresolved acceptance criterion ${ac}`);
      else acCoverage.set(ac,(acCoverage.get(ac)??0)+1);
    }
    for (const f of a.target_files ?? []) {
      if (!targets.some(t => t===f || (t.endsWith("/") && f.startsWith(t)))) e.push(`${a.action_id}: target_file not covered by files.target: ${f}`);
    }
  });
  if (!unique(actionIds)) e.push("actions: duplicate action_id");
  for (const a of actions) for (const d of a.depends_on ?? []) {
    if (!actionIds.includes(d)) e.push(`${a.action_id}: unresolved dependency ${d}`);
    if (d === a.action_id) e.push(`${a.action_id}: self dependency`);
  }
  topoAcyclic(actionIds,edges,e);
  for (const [ac,count] of acCoverage) if (count===0) e.push(`${ac}: orphan acceptance criterion (no Action covers it)`);

  const checks = Array.isArray(p.mandatory_checks) ? p.mandatory_checks : [];
  reqArray(p.mandatory_checks,e,"mandatory_checks",1);
  const checkIds=[];
  checks.forEach((c,i)=>{
    if (!reqObject(c,e,`mandatory_checks[${i}]`)) return;
    reqPattern(c.check_id,/^CHK-[0-9]{3,}$/,e,`mandatory_checks[${i}].check_id`);
    checkIds.push(c.check_id);
    reqEnum(c.kind,["schema","lint","typecheck","test","build","git","security","custom"],e,`${c.check_id}.kind`);
    reqString(c.command,e,`${c.check_id}.command`);
    if (!Number.isInteger(c.expected_exit_code) || c.expected_exit_code<0 || c.expected_exit_code>255) e.push(`${c.check_id}.expected_exit_code invalid`);
  });
  if (!unique(checkIds)) e.push("mandatory_checks: duplicate check_id");

  if (reqObject(p.definition_of_done,e,"definition_of_done")) {
    const d=p.definition_of_done;
    if (reqArray(d.required_acceptance_criteria_refs,e,"definition_of_done.required_acceptance_criteria_refs",1))
      for (const id of d.required_acceptance_criteria_refs) if (!acIds.includes(id)) e.push(`definition_of_done: unknown AC ${id}`);
    if (reqArray(d.required_check_refs,e,"definition_of_done.required_check_refs",1))
      for (const id of d.required_check_refs) if (!checkIds.includes(id)) e.push(`definition_of_done: unknown check ${id}`);
    if (d.no_unauthorized_changes !== true) e.push("definition_of_done.no_unauthorized_changes must be true");
    if (d.no_pending_human_decisions !== true) e.push("definition_of_done.no_pending_human_decisions must be true");
  }

  return e;
}

export function validateTaskProposalFile(file, repoRoot=process.cwd()) {
  let p;
  try { p=readJson(file); } catch(err) { return [`JSON parse failed: ${err.message}`]; }
  return validateTaskProposalObject(p,repoRoot);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const file=process.argv[2];
  if (!file) { console.error("usage: node .ai/control/validate-task-proposal.mjs <proposal.json>"); process.exit(2); }
  const errors=validateTaskProposalFile(file,process.cwd());
  process.exitCode=printVerdict("validate-task-proposal",errors,{file});
}
