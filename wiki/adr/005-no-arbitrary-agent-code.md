# ADR-005 — Residents never receive arbitrary code or shell execution

- **Status:** Accepted
- **Date:** 2026-08-01

## Context

Some embodied-agent projects offer generated code execution to extend behavior. An always-running multi-agent world processes untrusted resident text and external model output. Shell, filesystem, package installation, and open network access create unnecessary integrity, exfiltration, and persistence risks.

## Decision

Residents use a versioned allowlisted command API. Novel projects compile through bounded physical/institutional grammars. No resident gets shell, filesystem, database, browser/network, secret, eval, or arbitrary-code tools. Developer coding agents remain outside the simulation trust boundary.

## Consequences

- Less open-ended software invention inside the initial world.
- Much stronger security, replayability, and invariant enforcement.
- Future “digital technology” eras would require a separately sandboxed architecture and a new ADR.

## Rejected alternatives

- Generated JavaScript/Python execution in the simulation process.
- Per-agent containers with unrestricted egress.
- Prompt-only warnings without technical isolation.

