#!/usr/bin/env node
import {
  readJson, sha256File, reqObject, reqArray, reqEnum, reqPattern,
  parseDate, unique, pathAllowed, printVerdict
} from "./lib.mjs";
import { validateTaskApprovalObjects } from "./validate-task-approval.mjs";

export function validateExecutionObjects(proposal, approval, result, proposalFile, approvalFile, repoRoot=process.cwd()) {
  const e = validateTaskApprovalObjects(proposal,approval,proposalFile,repoRoot);
  if (!reqObject(result,e,"execution_result")) return e;

  reqEnum(result.object_type,["execution_result"],e,"object_type");
  reqEnum(result.schema_version,["2.0"],e,"schema_version");
  reqPattern(result.execution_id,/^EXE-[A-Z0-9._-]{3,127}$/,e,"execution_id");
  if (result.task_id !== proposal.task_id) e.push("execution task_id mismatch");

  const proposalHash = proposalFile ? sha256File(proposalFile) : null;
  const approvalHash = approvalFile ? sha256File(approvalFile) : null;

  if (reqObject(result.proposal_binding,e,"proposal_binding")) {
    if (result.proposal_binding.proposal_id !== proposal.proposal_id) e.push("execution proposal_id mismatch");
    if (result.proposal_binding.revision !== proposal.revision) e.push("execution proposal revision mismatch");
    if (proposalHash && result.proposal_binding.proposal_sha256 !== proposalHash) e.push("execution proposal_sha256 mismatch");
  }

  if (reqObject(result.approval_binding,e,"approval_binding")) {
    if (result.approval_binding.approval_id !== approval.approval_id) e.push("execution approval_id mismatch");
    if (approvalHash && result.approval_binding.approval_sha256 !== approvalHash) e.push("execution approval_sha256 mismatch");
  }

  if (reqObject(result.runtime_anchor,e,"runtime_anchor")) {
    if (result.runtime_anchor.repository !== "cepraea/beach-pro") e.push("execution repository mismatch");
    if (result.runtime_anchor.branch !== approval.runtime_anchor?.branch) e.push("execution branch differs from approved branch");
    if (result.runtime_anchor.base_commit !== approval.runtime_anchor?.base_commit) e.push("execution base_commit differs from approval");
    if (result.runtime_anchor.head_commit !== result.runtime_anchor.base_commit) e.push("agents cannot mutate Git HEAD; head_commit must equal approved base_commit");
  }

  let preflightTime=null;
  if (reqObject(result.preflight,e,"preflight")) {
    reqEnum(result.preflight.status,["PASS","BLOCKED"],e,"preflight.status");
    preflightTime=parseDate(result.preflight.completed_at,e,"preflight.completed_at");
    reqArray(result.preflight.checks,e,"preflight.checks",1);
    if (result.handoff_status==="READY_FOR_REVIEW" && result.preflight.status!=="PASS") e.push("READY_FOR_REVIEW requires preflight PASS");
    for (const c of result.preflight.checks??[]) {
      if (result.handoff_status==="READY_FOR_REVIEW" && c.status!=="PASS") e.push(`preflight check failed: ${c.check_id}`);
    }
  }

  reqEnum(result.handoff_status,["READY_FOR_REVIEW","BLOCKED"],e,"handoff_status");
  reqEnum(result.termination_reason,[
    "NONE","FAILED_VALIDATION","PREFLIGHT_BLOCKED","STOPPED_CONTRACT_INVALID",
    "STOPPED_APPROVAL_MISMATCH","STOPPED_RUNTIME_DRIFT","STOPPED_PRECONDITION_FAILED",
    "STOPPED_DEPENDENCY_UNSATISFIED","STOPPED_SCOPE_VARIANCE","STOPPED_SEMANTIC_VARIANCE",
    "STOPPED_CONTRACT_AMBIGUITY","STOPPED_HUMAN_DECISION_REQUIRED",
    "STOPPED_FORBIDDEN_FILE_ACCESS","STOPPED_UNAUTHORIZED_DEPENDENCY_CHANGE",
    "STOPPED_UNAUTHORIZED_DATABASE_CHANGE","STOPPED_RUNBOOK_VIOLATION",
    "STOPPED_RISK_ESCALATION","STOPPED_EVIDENCE_IMPOSSIBLE","STOPPED_RULES_INTEGRITY_FAILURE"
  ],e,"termination_reason");
  if (result.handoff_status==="READY_FOR_REVIEW" && result.termination_reason!=="NONE") e.push("READY_FOR_REVIEW requires termination_reason NONE");
  if (result.handoff_status==="BLOCKED" && result.termination_reason==="NONE") e.push("BLOCKED requires a termination_reason");

  const started=parseDate(result.started_at,e,"started_at");
  const completed=parseDate(result.completed_at,e,"completed_at");
  if (started!==null && completed!==null && completed<started) e.push("completed_at precedes started_at");

  const proposalActions=new Map((proposal.actions??[]).map(a=>[a.action_id,a]));
  const acIds=new Set((proposal.acceptance_criteria??[]).map(a=>a.criterion_id));
  const targetPaths=(proposal.files??[]).filter(f=>f.role==="target").map(f=>f.path);

  const resultActions=Array.isArray(result.actions)?result.actions:[];
  reqArray(result.actions,e,"actions",1);
  const resultActionIds=resultActions.map(a=>a.action_id);
  if (!unique(resultActionIds)) e.push("execution actions duplicate action_id");
  for (const id of proposalActions.keys()) if (!resultActionIds.includes(id)) e.push(`execution missing proposal Action ${id}`);
  for (const id of resultActionIds) if (!proposalActions.has(id)) e.push(`execution contains unknown Action ${id}`);

  const evidences=Array.isArray(result.evidence)?result.evidence:[];
  reqArray(result.evidence,e,"evidence");
  const evMap=new Map();
  for (const ev of evidences) {
    reqPattern(ev.evidence_id,/^EVD-[A-Z0-9._-]{3,127}$/,e,"evidence_id");
    if (evMap.has(ev.evidence_id)) e.push(`duplicate evidence_id ${ev.evidence_id}`);
    evMap.set(ev.evidence_id,ev);

    if (ev.simulated !== false) e.push(`${ev.evidence_id}: simulated evidence is forbidden`);
    for (const aid of ev.action_refs??[]) if (!proposalActions.has(aid)) e.push(`${ev.evidence_id}: unknown action_ref ${aid}`);
    for (const ac of ev.acceptance_criteria_refs??[]) if (!acIds.has(ac)) e.push(`${ev.evidence_id}: unknown AC ${ac}`);

    const t=parseDate(ev.observed_at,e,`${ev.evidence_id}.observed_at`);
    if (preflightTime!==null && t!==null && t<preflightTime) e.push(`${ev.evidence_id}: observed before preflight completed`);

    const commandEvidence = typeof ev.command==="string" && Number.isInteger(ev.exit_code);
    const artifactEvidence = Array.isArray(ev.artifact_refs) && ev.artifact_refs.length>0;
    if (ev.status==="PASS" && !commandEvidence && !artifactEvidence) {
      e.push(`${ev.evidence_id}: PASS evidence needs command+exit_code or artifact_refs`);
    }
  }

  const changes=Array.isArray(result.changes)?result.changes:[];
  reqArray(result.changes,e,"changes");
  const changePaths=new Set();
  for (const ch of changes) {
    if (changePaths.has(ch.path)) e.push(`duplicate change path ${ch.path}`);
    changePaths.add(ch.path);

    for (const aid of ch.action_refs??[]) if (!proposalActions.has(aid)) e.push(`${ch.change_id}: unknown action_ref ${aid}`);
    const allowed=targetPaths.some(t=>pathAllowed(t,ch.path));
    if (!allowed || ch.authorized!==true) e.push(`${ch.change_id}: unauthorized target path ${ch.path}`);

    const t=parseDate(ch.observed_at,e,`${ch.change_id}.observed_at`);
    if (preflightTime!==null && t!==null && t<preflightTime) e.push(`${ch.change_id}: change observed before preflight completed`);
  }

  for (const ar of resultActions) {
    const pa=proposalActions.get(ar.action_id);
    if (!pa) continue;

    for (const ac of ar.acceptance_criteria_refs??[]) {
      if (!pa.acceptance_criteria_refs.includes(ac)) e.push(`${ar.action_id}: execution AC ${ac} not authorized by proposal Action`);
    }

    for (const file of ar.files_changed??[]) {
      if (!changePaths.has(file)) e.push(`${ar.action_id}: files_changed missing change entry for ${file}`);
      if (!targetPaths.some(t=>pathAllowed(t,file))) e.push(`${ar.action_id}: files_changed outside targets ${file}`);
    }

    for (const evId of ar.evidence_refs??[]) {
      if (!evMap.has(evId)) e.push(`${ar.action_id}: unresolved evidence_ref ${evId}`);
    }

    if (ar.status==="PASS") {
      if (!Array.isArray(ar.evidence_refs) || ar.evidence_refs.length===0) e.push(`${ar.action_id}: PASS requires evidence_refs`);
      for (const ac of pa.acceptance_criteria_refs) {
        const ok=[...evMap.values()].some(ev =>
          ev.status==="PASS" &&
          (ev.action_refs??[]).includes(ar.action_id) &&
          (ev.acceptance_criteria_refs??[]).includes(ac)
        );
        if (!ok) e.push(`${ar.action_id}: no PASS evidence for ${ac}`);
      }
    }

    if (result.handoff_status==="READY_FOR_REVIEW" && ar.status!=="PASS") {
      e.push(`READY_FOR_REVIEW requires Action PASS: ${ar.action_id}`);
    }
  }

  const finalChecks=Array.isArray(result.final_checks)?result.final_checks:[];
  reqArray(result.final_checks,e,"final_checks",1);
  const finalMap=new Map(finalChecks.map(c=>[c.check_id,c]));

  for (const chk of proposal.mandatory_checks??[]) {
    const got=finalMap.get(chk.check_id);
    if (!got) e.push(`missing mandatory final check ${chk.check_id}`);
    else if (result.handoff_status==="READY_FOR_REVIEW" && got.status!=="PASS") e.push(`mandatory final check failed ${chk.check_id}`);
  }

  for (const c of finalChecks) {
    for (const evId of c.evidence_refs??[]) if (!evMap.has(evId)) e.push(`${c.check_id}: unresolved evidence_ref ${evId}`);
  }

  reqArray(result.unauthorized_changes,e,"unauthorized_changes");
  if (result.handoff_status==="READY_FOR_REVIEW" && result.unauthorized_changes?.length) {
    e.push("READY_FOR_REVIEW requires unauthorized_changes=[]");
  }

  for (const ac of proposal.definition_of_done?.required_acceptance_criteria_refs??[]) {
    const ok=[...evMap.values()].some(ev => ev.status==="PASS" && (ev.acceptance_criteria_refs??[]).includes(ac));
    if (result.handoff_status==="READY_FOR_REVIEW" && !ok) e.push(`Definition of Done: missing PASS evidence for ${ac}`);
  }

  return e;
}

export function validateExecutionFiles(proposalFile,approvalFile,resultFile,repoRoot=process.cwd()) {
  let p,a,r;
  try { p=readJson(proposalFile); } catch(err) { return [`proposal JSON parse failed: ${err.message}`]; }
  try { a=readJson(approvalFile); } catch(err) { return [`approval JSON parse failed: ${err.message}`]; }
  try { r=readJson(resultFile); } catch(err) { return [`execution JSON parse failed: ${err.message}`]; }
  return validateExecutionObjects(p,a,r,proposalFile,approvalFile,repoRoot);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const [proposalFile,approvalFile,resultFile]=process.argv.slice(2);
  if (!proposalFile || !approvalFile || !resultFile) {
    console.error("usage: node .ai/control/validate-execution-result.mjs <proposal.json> <approval.json> <execution-result.json>");
    process.exit(2);
  }
  const errors=validateExecutionFiles(proposalFile,approvalFile,resultFile,process.cwd());
  process.exitCode=printVerdict("validate-execution-result",errors,{proposalFile,approvalFile,resultFile});
}
