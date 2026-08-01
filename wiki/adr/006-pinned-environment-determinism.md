# ADR-006 — Separate event reconstruction, kernel re-execution, and fresh branches

- **Status:** Accepted. **Numeric representation decided 2026-08-01: Option A, fixed-unit integers.**
- **Date:** 2026-08-01 (added by audit pass)

## Context

The plan claimed replays are "bit-for-bit identical in the non-LLM kernel." That claim is false as stated for a Python simulation using floating-point arithmetic, and it sits underneath event sourcing, shadow worlds, the causal UI, and the entire audit protocol.

IEEE 754 guarantees correctly rounded basic operations, so a fixed sequence of `+ - * / sqrt` is reproducible across conforming hardware. What is not reproducible is *which* sequence executes: FMA contraction differs between x86 and ARM64 toolchains, SIMD reduction order varies with lane width and runtime CPU dispatch, and — decisively — glibc explicitly disclaims correctly rounded transcendentals, so `exp`, `log`, `pow`, and `sin` differ across libc versions and operating systems. NumPy makes no cross-platform or cross-version guarantee and says so in its own compatibility policy.

Separately, no LLM provider offers reproducible sampling. OpenAI's and Gemini's `seed` parameters are documented as best-effort; Anthropic has no seed at all and its newest models reject `temperature` outright.

## Decision

December makes three claims:

1. Recorded events reconstruct canonical state exactly on every supported platform.
2. Re-executing commands and stochastic transitions reproduces checkpoint hashes within a pinned numeric environment; fixed-unit canonical state is the preferred route to broader portability.
3. Calling a live model again is a fresh branch, never a replay.

The content-addressed model-response cache is **canonical**: backed up and versioned with the event log, and replay hard-fails on a cache miss rather than calling a live model.

**Gate 1 decides the sub-question:** which state variables use fixed units and where float calculations are permitted before deterministic quantization. Full integer-only ecology is not required merely to rebuild recorded history.

## Consequences

- Every public reproducibility statement carries the qualifier. The success criteria in [`00`](../00-vision-and-north-star.md) were amended.
- The kernel accepts real constraints: single-threaded, default GIL build, pinned `PYTHONHASHSEED`, no unordered-collection iteration, no wall-clock reads, no platform `libm` in state-writing code, no finalizers.
- A cross-platform reconstruction suite is mandatory. Kernel re-execution divergence is a Blocker only when it violates the project’s declared supported environment/guarantee.
- Under Option A, the kernel gains portable determinism at the cost of arithmetic discipline — scaled integers with declared precision per quantity.

## Owner decisions, 2026-08-01

**Numeric representation: Option A — fixed-unit integers.** Conserved and discrete canonical quantities use scaled integers with declared precision (grams, millilitres, kilojoules, seconds, millimetres). Floating-point arithmetic is permitted *inside* a transition, but only its explicitly quantized output enters canonical state, using a declared rounding rule. Portable kernel re-execution therefore becomes a Phase 1 goal rather than an aspiration.

**Deployment target: single local machine.**

Note that these two answers are deliberately mismatched in the safe direction. A single pinned machine would make Option B defensible on its own; choosing Option A anyway costs some arithmetic discipline and buys three things: history recorded today remains replayable if the world ever moves to a server, the determinism tests in §D9 test something real rather than tautologically passing on one box, and an auditor can reproduce a history on their own hardware — which the audit protocol in [`12`](../12-audit-guide.md) assumes but could not otherwise deliver.

**Declared units for canonical state** (extend deliberately; each addition is a schema change):

| Quantity | Unit | Type |
|---|---|---|
| Mass (grain, materials) | gram | `int` |
| Volume (water) | millilitre | `int` |
| Energy | kilojoule | `int` |
| Time | second | `int` |
| Distance | millimetre | `int` |
| Area | square metre | `int` |
| Count | item | `int` |
| Proportions and rates | parts-per-million | `int` |

Rounding is **half-to-even at every quantization boundary**, applied by a single shared helper so the rule cannot drift between subsystems. No canonical field is a float. A property test asserts that no canonical state field is float-typed at any point in the event log.

## Rejected alternatives

- **Claiming portable bit-identity anyway.** It would be false, and it would be discovered at the worst possible moment — when an auditor tries to reproduce a history on their own machine.
- **Abandoning determinism as too hard.** It is the foundation of every integrity promise the project makes.
- **Treating the response cache as a performance optimization.** A cache miss during replay would silently fabricate a divergent history under the banner of reproduction.
