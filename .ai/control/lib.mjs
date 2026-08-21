import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";

export function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}
export function sha256File(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}
export function unique(values) {
  return new Set(values).size === values.length;
}
export function isObject(v) {
  return v !== null && typeof v === "object" && !Array.isArray(v);
}
export function reqObject(v, errors, label) {
  if (!isObject(v)) { errors.push(`${label}: expected object`); return false; }
  return true;
}
export function reqArray(v, errors, label, min=0) {
  if (!Array.isArray(v)) { errors.push(`${label}: expected array`); return false; }
  if (v.length < min) errors.push(`${label}: expected at least ${min} item(s)`);
  return true;
}
export function reqString(v, errors, label) {
  if (typeof v !== "string" || v.trim() === "") { errors.push(`${label}: expected non-empty string`); return false; }
  return true;
}
export function reqBool(v, errors, label) {
  if (typeof v !== "boolean") { errors.push(`${label}: expected boolean`); return false; }
  return true;
}
export function reqEnum(v, allowed, errors, label) {
  if (!allowed.includes(v)) { errors.push(`${label}: expected one of ${allowed.join(", ")}`); return false; }
  return true;
}
export function reqPattern(v, re, errors, label) {
  if (!reqString(v, errors, label)) return false;
  if (!re.test(v)) { errors.push(`${label}: invalid format (${v})`); return false; }
  return true;
}
export function parseDate(v, errors, label) {
  if (!reqString(v, errors, label)) return null;
  const n = Date.parse(v);
  if (Number.isNaN(n)) { errors.push(`${label}: invalid date-time`); return null; }
  return n;
}
export function relativePath(v, errors, label) {
  if (!reqString(v, errors, label)) return false;
  if (path.isAbsolute(v) || v.split(/[\\/]/).includes("..")) {
    errors.push(`${label}: path must be repository-relative and cannot contain ..`);
    return false;
  }
  return true;
}
export function pathAllowed(target, changed) {
  if (target === changed) return true;
  if (target.endsWith("/")) return changed.startsWith(target);
  return false;
}
export function run(cmd, args, cwd=process.cwd()) {
  return spawnSync(cmd, args, { cwd, encoding: "utf8" });
}
export function topoAcyclic(ids, edges, errors, label="actions") {
  const state = new Map();
  const visit = (id, stack=[]) => {
    const s = state.get(id);
    if (s === 2) return;
    if (s === 1) {
      errors.push(`${label}: dependency cycle: ${[...stack, id].join(" -> ")}`);
      return;
    }
    state.set(id, 1);
    for (const dep of edges.get(id) ?? []) visit(dep, [...stack, id]);
    state.set(id, 2);
  };
  for (const id of ids) visit(id);
}
export function printVerdict(name, errors, extra={}) {
  if (errors.length) {
    console.error(JSON.stringify({ validator:name, verdict:"FAIL", errors, ...extra }, null, 2));
    return 1;
  }
  console.log(JSON.stringify({ validator:name, verdict:"PASS", ...extra }, null, 2));
  return 0;
}
