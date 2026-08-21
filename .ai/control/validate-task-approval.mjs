#!/usr/bin/env node
import {
  readJson, sha256File, reqObject, reqString, reqEnum, reqPattern,
  parseDate, printVerdict
} from "./lib.mjs";
import { validateTaskProposalObject } from "./validate-task-proposal.mjs";

export function validateTaskApprovalObjects(proposal, approval, proposalFile, repoRoot=process.cwd()) {
  const e = validateTaskProposalObject(proposal,repoRoot);
  if (!reqObject(approval,e,"approval")) return e;
  reqEnum(approval.object_type,["task_approval"],e,"approval.object_type");
  reqEnum(approval.schema_version,["1.0"],e,"approval.schema_version");
  reqPattern(approval.approval_id,/^APR-[A-Z0-9._-]{3,127}$/,e,"approval.approval_id");
  reqString(approval.task_id,e,"approval.task_id");
  if (approval.task_id !== proposal.task_id) e.push("approval.task_id does not match proposal.task_id");

  if (reqObject(approval.proposal_binding,e,"approval.proposal_binding")) {
    const b=approval.proposal_binding;
    if (b.proposal_id !== proposal.proposal_id) e.push("approval proposal_id mismatch");
    if (b.revision !== proposal.revision) e.push("approval revision mismatch");
    reqPattern(b.proposal_sha256,/^[a-f0-9]{64}$/,e,"approval.proposal_sha256");
    if (proposalFile) {
      const actual=sha256File(proposalFile);
      if (b.proposal_sha256 !== actual) e.push(`approval proposal_sha256 mismatch: expected ${actual}`);
    }
  }
  if (reqObject(approval.plan_review,e,"approval.plan_review")) {
    reqEnum(approval.plan_review.reviewer,["codex"],e,"approval.plan_review.reviewer");
    reqEnum(approval.plan_review.review_stage,["PLAN"],e,"approval.plan_review.review_stage");
    reqEnum(approval.plan_review.verdict,["PASS"],e,"approval.plan_review.verdict");
    parseDate(approval.plan_review.reviewed_at,e,"approval.plan_review.reviewed_at");
  }
  reqEnum(approval.decision,["approved"],e,"approval.decision");
  if (reqObject(approval.issued_by,e,"approval.issued_by")) {
    reqEnum(approval.issued_by.actor_type,["human"],e,"approval.issued_by.actor_type");
    reqString(approval.issued_by.actor_id,e,"approval.issued_by.actor_id");
  }
  parseDate(approval.issued_at,e,"approval.issued_at");
  if (reqObject(approval.runtime_anchor,e,"approval.runtime_anchor")) {
    reqEnum(approval.runtime_anchor.repository,["cepraea/beach-pro"],e,"approval.runtime_anchor.repository");
    reqString(approval.runtime_anchor.branch,e,"approval.runtime_anchor.branch");
    if (["main","master"].includes(approval.runtime_anchor.branch)) e.push("approval.runtime_anchor.branch cannot be main/master");
    reqPattern(approval.runtime_anchor.base_commit,/^[a-fA-F0-9]{7,64}$/,e,"approval.runtime_anchor.base_commit");
    reqEnum(approval.runtime_anchor.working_tree_policy,["clean_required","contract_allowed_changes_only"],e,"approval.runtime_anchor.working_tree_policy");
  }
  return e;
}

export function validateTaskApprovalFiles(proposalFile,approvalFile,repoRoot=process.cwd()) {
  let p,a;
  try { p=readJson(proposalFile); } catch(err) { return [`proposal JSON parse failed: ${err.message}`]; }
  try { a=readJson(approvalFile); } catch(err) { return [`approval JSON parse failed: ${err.message}`]; }
  return validateTaskApprovalObjects(p,a,proposalFile,repoRoot);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const [proposalFile,approvalFile]=process.argv.slice(2);
  if (!proposalFile || !approvalFile) { console.error("usage: node .ai/control/validate-task-approval.mjs <proposal.json> <approval.json>"); process.exit(2); }
  const errors=validateTaskApprovalFiles(proposalFile,approvalFile,process.cwd());
  process.exitCode=printVerdict("validate-task-approval",errors,{proposalFile,approvalFile});
}
