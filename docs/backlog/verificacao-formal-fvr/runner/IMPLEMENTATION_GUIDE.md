# FVR-1.0 Runner Implementation — Mechanical Use

This package contains an implementation candidate of the frozen FVR-1.0 specification.

## Authority

The source of normative behavior is `normative/`. The implementation is subordinate to those files.

`verify.sh` is not conformant merely because it runs. Conformance is granted only by the conformance harness when every mandatory FVR vector and every AC-FVR-01..20 mapping returns PASS.

## Files

- `.ai-control/runner/verify.sh` — Fixed Verification Runner candidate.
- `conformance/conformance_harness.py` — external conformance engine.
- `conformance/requirements.txt` — Python-only harness dependencies.
- `SYSTEM_REQUIREMENTS.json` — host/dependency boundary.
- `implementation-validation.json` — checks actually executed in the build environment.
- `normative/` — frozen schema and conformance inputs copied into this package.

## Trust Anchor

Calculate hashes over exact stored bytes:

```bash
sha256sum   .ai-control/runner/verify.sh   .ai-control/verification-plan.json   .ai-control/contract.json
```

The verification-plan hash is external-only. Do not add a self-hash field to the plan.

## Runner invocation

```bash
.ai-control/runner/verify.sh   --plan .ai-control/verification-plan.json   --contract .ai-control/contract.json   --schema-dir ./normative/schemas   --expected-plan-sha256 '<PLAN_SHA256>'   --expected-contract-sha256 '<CONTRACT_SHA256>'   --expected-runner-sha256 '<RUNNER_SHA256>'   --run-id 'RUN-EXAMPLE-001'
```

Runner process result mapping:

- `0`: evidence collection completed (`RUN_COMPLETED` or `RUN_COMPLETED_WITH_FAILED_ASSERTIONS`);
- `10`: `PLAN_INVALID`;
- `11`: `CONTROL_INTEGRITY_FAILURE`;
- `12`: `POLICY_VIOLATION`;
- `13`: `PACKAGE_INCOMPLETE`;
- `14`: `RUNNER_INTERNAL_ERROR`.

A child exit code is evidence and is never reused as the runner process exit code.

## Full conformance execution

Install the host preconditions listed in `SYSTEM_REQUIREMENTS.json`, then:

```bash
python3 conformance/conformance_harness.py   --runner .ai-control/runner/verify.sh   --schema-dir normative/schemas   --spec-dir normative/runner-conformance   --report conformance-report.json
```

Interpretation:

- `CONFORMANT`: all mandatory vectors and AC-FVR-01..20 passed.
- `NON_CONFORMANT`: at least one mandatory check failed.
- `HARNESS_INVALID`: the environment cannot execute the normative harness. This is not PASS.

## Sandbox semantics

`process.run` never falls back to host execution. It requires `bwrap`.

The intended mount model is:

- `/fvr/source`: source workspace, read-only;
- `/fvr/work`: disposable writable copy;
- `/tmp`: ephemeral writable area;
- system paths: read-only;
- default network namespace: isolated;
- stdin: closed;
- TTY: absent;
- effective capabilities: zero;
- non-root UID;
- `NoNewPrivs=1`.

These properties are not accepted from configuration text. The harness probes them behaviorally.

## Atomic publication

The runner writes a package under:

`.ai-control/verification-package/.tmp/<run_id>`

and publishes it only with a same-filesystem rename to:

`.ai-control/verification-package/<run_id>`

The crash-consistency suite verifies that the final directory is not visible before publication.

## Assurance boundary

The SHA-256 trust anchor identifies the bytes of `verify.sh`, including its embedded Python engine. It does not attest the host Python interpreter, installed validation libraries, kernel or sandbox executable. Those are host security constraints at RI-2/E1. This package does not claim RI-3.
