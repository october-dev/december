# ADR-002 — Canonical history is event-sourced

- **Status:** Accepted for audit
- **Date:** 2026-08-01

## Context

The product promise depends on returning later, understanding what happened, replaying it, surviving crashes, and creating counterfactual branches. Mutable save-state alone cannot supply adequate provenance.

## Decision

Accepted commands append immutable versioned events with causal parents, RNG references, code/config version, and state hashes. Current state and UI views are projections. Periodic snapshots accelerate recovery but are not the source of truth. Model prompts/responses are content-addressed so replay does not call a live model.

## Consequences

- Event schema/versioning discipline and storage cost.
- Easier audit, recovery, shadow worlds, migrations, and causal UI.
- Bugs in historical events require projection fixes/upcasters or explicit corrective events, not silent rewriting.

## Amendments from the 2026-08-01 audit

Three implementation constraints matter. Their Phase 1 form is deliberately simple; all are specified in [`14`](../14-determinism-replay-and-state-integrity.md):

- **The log must expose only committed event batches in canonical order.** Phase 1 enforces one serialized writer. A multi-writer design requires a separately tested commit-order protocol; `xid8` values alone are not commit order.
- **Integrity checks are proportional.** Phase 1 hash-chains events, versions/hashes affected aggregates, and hashes full snapshots. Incremental world digests are added only if profiling justifies them.
- **The prompt/response cache is canonical**, not a performance optimization, and **replay hard-fails on a cache miss**. No provider offers reproducible sampling, so a miss would fabricate a divergent history while claiming to reproduce one. See [ADR-006](006-pinned-environment-determinism.md).

## Rejected alternatives

- Periodic JSON save files only.
- Database rows mutated without event lineage.
- Replay that resamples weather or calls current LLMs.
