# 14 — Determinism, Replay, and State Integrity

**Status:** added by the 2026-08-01 audit pass. This document replaces the informal determinism language in [`00`](00-vision-and-north-star.md), [`06`](06-architecture-and-data.md), and [`ADR-002`](adr/002-event-sourced-history.md) with a specification that survives contact with real hardware.

## Why this document exists

Earlier drafts claimed replays are "bit-for-bit identical in the non-LLM kernel." That claim, unqualified, is false for any Python simulation that uses floating-point arithmetic, and it is the load-bearing claim under event sourcing, shadow worlds, the causal UI, and the audit protocol. If replay is not actually reproducible, every downstream integrity promise is decoration.

This document states what is achievable, at what cost, and what the project commits to.

## D1. Three reproducibility guarantees

Earlier versions used “replay” for three different operations. They are now separate:

1. **Recorded-history reconstruction.** Apply the already-recorded canonical events to an empty projection or compatible snapshot. This must be portable across supported machines because events contain the authoritative outcomes and use canonical encodings. No weather, RNG, physics, or model decision is recomputed.
2. **Kernel re-execution.** Starting from the same initial state, commands, RNG keys, code, and config, recompute the events. Exact checkpoint equality is required inside the pinned numeric environment. Portable equality is a Phase 1 goal if canonical state uses fixed units and deterministic transition implementations.
3. **Fresh counterfactual simulation.** Re-run one or more cognition decisions against a live model or change an intervention. This is a new branch, never a replay, and is expected to diverge.

> **Claim.** Recorded history reconstructs exactly from its event artifacts. Kernel re-execution reproduces checkpoint hashes within the declared environment. Fresh model sampling produces a separately identified branch.

This distinction prevents floating-point caveats from weakening ordinary event-store recovery while keeping re-simulation claims honest.

### Why portable bit-identity is not available

IEEE 754 requires correctly rounded results for `+ - * / sqrt fma`, so a *fixed sequence* of basic operations is reproducible across conforming hardware. Everything that breaks reproducibility is about which sequence actually executes:

| Divergence source | Effect | Applies to us? |
|---|---|---|
| FMA contraction (`a*b+c` as one rounding vs two) | Different low bits; x86 and ARM64 toolchains default differently | Yes, if the kernel does float arithmetic in compiled extensions |
| SIMD reduction order (SSE/AVX2/AVX-512/NEON lane counts) | Reassociated sums differ | Yes, via NumPy's runtime CPU dispatch |
| `libm` transcendentals (`exp`, `log`, `pow`, `sin`) | glibc explicitly disclaims correct rounding; results differ by version, OS, and architecture | Yes — this alone falsifies portable bit-identity |
| BLAS backend (OpenBLAS vs MKL vs Accelerate) and its thread count | Different results for any linear algebra | Only if the kernel uses `@` or `np.linalg` |
| `-ffast-math` / FTZ / DAZ flags, including flags set by *other* loaded libraries | Reassociation and denormal flushing | Possible, via third-party wheels |
| x87 80-bit intermediates | Extra precision on 32-bit x86 | No — we require SSE2/NEON code paths |

NumPy makes no cross-platform or cross-version guarantee. `np.sum` uses pairwise summation "when the summation is along the fast axis in memory," so its result depends on array layout, axis, and strides, and on the SIMD width selected at runtime. The [NumPy random compatibility policy](https://numpy.org/doc/stable/reference/random/compatibility.html) is explicit that identical streams are promised only for "the same build of numpy, in the same environment, on the same machine."

Correctly-rounded math libraries are maturing — the [CORE-MATH project](https://core-math.gitlabpages.inria.fr/) has been partially upstreamed into glibc 2.42/2.43, and [LLVM libc](https://libc.llvm.org/math/) implements C23 math correctly rounded — but relying on whatever `libm` the host ships remains unsound. Portable determinism would require bundling a correctly-rounded math layer or making the kernel integer-only.

### Numeric policy for kernel re-execution

**Phase 1 must answer one question: can the canonical kernel state be integer-valued?**

Conserved and discrete canonical quantities—mass, volume, energy reserve, time, inventory counts, cell coordinates, and currency if it ever exists—should use scaled integers with explicit rounding. Scientific calculations may use floats inside a transition, but only their quantized declared output enters canonical state. Phase 1 tests boundary cases across supported environments before claiming portable kernel re-execution.

This is the recommended target. It costs discipline, not performance. Gate 1 records the decision explicitly:

- **Option A (preferred):** fixed-unit canonical state, with deterministic quantization at transition boundaries.
- **Option B (fallback):** float canonical state and pinned-environment re-execution only.

Do not defer this decision past Gate 1. Retrofitting fixed-point arithmetic into an existing ecology and crop model is a rewrite.

## D2. Kernel execution constraints

Whichever option is chosen, the kernel obeys these rules. They are testable and belong in CI.

1. **The kernel is a synchronous, single-threaded pure function** of (prior state, ordered input events). Concurrency lives strictly outside it. No `asyncio` inside a transition rule, no thread pools, no executor callbacks.
2. **Run on the default GIL build.** Free-threaded CPython is officially supported as of 3.14, but true parallelism reintroduces allocation-order and interleaving nondeterminism. If free-threading is ever adopted, the kernel stays confined to one thread with no shared mutable state.
3. **`PYTHONHASHSEED` is pinned** in the world manifest and asserted at startup. `str`/`bytes` hashing is salted per process by default.
4. **Never iterate an unordered collection.** `dict` preserves insertion order (guaranteed since 3.7) and is permitted when insertion order is itself deterministic. `set` and `frozenset` iteration is forbidden in any code path that writes state; use `sorted(collection, key=<stable canonical key>)`. A lint rule enforces this.
5. **No `id()`-derived ordering and no default `object.__hash__`** for any entity that participates in state. Entities sort by their stable string ID.
6. **No finalizers.** `__del__`, weakref callbacks, and resurrection are banned in kernel modules; GC timing is not reproducible.
7. **No wall-clock reads inside the kernel.** Simulated time is a state variable. `time.time()`, `datetime.now()`, and `loop.time()` are banned in kernel modules and blocked by lint.
8. **No platform `libm` in state-writing code** under Option B. If a transition rule needs `exp` or `pow` (crop growth curves, decay, hazard rates), it uses a project-owned implementation: a table-plus-polynomial approximation with declared precision, versioned as a parameter. This is a small amount of code and it removes the single largest portability hazard.
9. **Pin SIMD dispatch and BLAS** under Option B: set `NPY_DISABLE_CPU_FEATURES` to a documented baseline, pin the NumPy wheel in the lockfile, and keep linear algebra out of the kernel entirely.
10. **Canonical serialization** for hashing: fixed field order, integers where possible, and for any float a fixed-width byte encoding — never `repr()`.

## D3. Random number generation

Use **counter-based, stateless, key-derived streams**. A counter-based generator is a pure function `output = f(key, counter)`, so it needs no sequential state in snapshots, can be evaluated from any point, and gives independent streams by construction.

```text
stream_key = SHA256(root_seed ‖ branch_id ‖ subsystem ‖ entity_id ‖ purpose)[:16]
draw       = Philox(key=stream_key, counter=logical_draw_index)
```

Rules:

- **Never `seed = hash(entity_id)`.** Python's `hash()` is salted, so it is not even stable across processes; truncated seed spaces invite birthday collisions between entities; and related seeds produce correlated streams in some generators.
- **Use the raw BitGenerator bit stream as the stable layer.** NumPy's [NEP 19 policy](https://numpy.org/neps/nep-0019-rng-policy.html) permits breaking *distribution* streams (`normal`, `poisson`, `multivariate_normal`) in minor releases for performance or correctness. Integer bit output from PCG64/Philox is stable in practice; the float distribution layer is where version risk concentrates. December implements its own inverse-CDF transforms over raw bits for any distribution whose stream must survive a dependency bump, and records the distribution implementation version on every stochastic event.
- **One stream per (subsystem, entity, purpose).** This delivers the property [`06`](06-architecture-and-data.md) already demands: adding a cosmetic draw cannot perturb crop yields, because cosmetic draws live in a different stream with a different key.
- **Record `distribution_version`, parameters, counter, and sampled result** on every stochastic event, so a draw can be re-derived and audited without re-running the subsystem.
- Pin the NumPy version in the world manifest regardless.

## D4. Laundering LLM latency into deterministic order

This is the mechanism [`07`](07-time-emergence-and-observation.md) asserts ("no resident gains advantage from model-provider response latency") without specifying. The pattern is standard in deterministic simulation testing and lockstep game networking: **the kernel never observes arrival order; arrival order is laundered into a logical-time decision that is recorded as an event.**

### The decision-barrier protocol

1. **Emit.** Kernel tick at simulated time `T` ends by emitting `DecisionRequested` events. Each carries a deterministic `decision_id = H(world, branch, T, actor_id, trigger_kind, sequence_within_tick)`. The kernel's work for tick `T` is now finished; it does not wait.
2. **Dispatch.** An orchestrator *outside* the kernel resolves each request: check the content-addressed response cache, otherwise call the provider. Latency, retries, provider failover, and concurrency all happen here and are invisible to the kernel.
3. **Resolve.** Each response is appended as a `DecisionResolved` event bound to a *logical* barrier — either a fixed offset `T+k` (turn buffering, as in classic lockstep RTS) or "the first tick after all requests issued at `T` have resolved or timed out." The choice is a config parameter; both are deterministic.
4. **Ingest.** At the barrier tick the kernel consumes all resolved decisions **sorted by `decision_id`**, never by arrival time, and validates each through the normal command pipeline.
5. **Resolve live failure explicitly.** A wall-clock deadline and retry budget may decide whether a response is accepted in the live service. The first durable resolution wins. Low-significance requests may record a resident-specific routine fallback; unresolved high-significance requests pause the world at that barrier. Recorded-history reconstruction consumes this resolution and never reruns the race.

Consequence: network arrival order never breaks ties between already-resolved resident actions. Provider failure may affect wall-clock pace and whether the live world pauses, and that operational history is visible rather than laundered away.

### Decision-level idempotency

Command-level idempotency keys (already in [`06`](06-architecture-and-data.md)) prevent a *duplicate delivery* of the same command from applying twice. They do **not** cover the more likely failure: a provider call times out, the orchestrator retries, and the model returns a *different* command the second time. Both are validly signed, neither is a duplicate, and the world silently forks from the replay.

Rule: **the `decision_id` is the idempotency unit, not the command.** The first response to be durably recorded for a given `decision_id` wins permanently. Late-arriving responses for a resolved `decision_id` are discarded and counted in a metric; they never reach the kernel. This must be enforced by a unique constraint on `decision_id` in the resolution table, not by application logic.

## D5. The model-response cache is canonical, not an optimization

No provider offers reproducible sampling. As of August 2026: OpenAI's `seed` is documented best-effort with no guarantee; Gemini's `seed` is likewise best-effort; Anthropic has no seed parameter at all and its newest models reject `temperature`/`top_p` entirely; DeepSeek and MiniMax expose no reproducibility mechanism. Temperature 0 is not deterministic on any of them.

Therefore:

- The content-addressed prompt/response cache is **part of the canonical world artifact**, backed up and versioned with the event log. It is not a disposable performance cache.
- The cache key is the full request as sent: prompt bytes, model ID *and* provider-reported version/fingerprint, tool/schema definitions, and every sampling parameter.
- **Replay hard-fails on a cache miss.** It must never silently call a live model — that would fabricate a divergent history under the banner of reproduction. A replay that encounters a miss aborts and reports the missing `decision_id`. This is a required test.
- Re-running with fresh model responses is not a replay. It is a **new branch** with its own `branch_id`, and the UI must label it as such.
- Prompt/response bodies are stored encrypted at rest where feasible and are subject to the retention policy in [`08`](08-models-cost-operations-security.md).

## D6. State hashing that does not cost O(state) per event

[`06`](06-architecture-and-data.md) requires `pre_state_hash` and `post_state_hash` on every event. Implemented naively — serialize the world, hash it — this is O(total state) per event and makes the event pipeline quadratic in world size. With 10⁴–10⁶ entities and millions of events it is not merely slow, it is the dominant cost of the entire simulation.

**Phase 1 minimum:** hash-chain event envelopes, keep expected aggregate versions, compute hashes for changed aggregates, and compute a canonical full-state hash at snapshots. This is sufficient for reconstruction, corruption detection, and divergence localization at December’s starting scale.

Only if measurement shows snapshot hashing or aggregate comparison is too slow should December add incremental homomorphic hashing. An LtHash-style construction would maintain a running digest under addition and subtraction:

```text
H' = H − h(entity_id ‖ canonical_bytes_before) + h(entity_id ‖ canonical_bytes_after)
```

Properties that matter here: update cost is O(changed entities) rather than O(state), the digest is order-independent (so it cannot accidentally encode iteration order), and it parallelizes trivially. This is the same primitive Solana adopted to hash its entire account set every block, which is direct evidence it holds up at far larger scale than December needs.

Supplement it with:

- **Periodic full recomputation** — at every snapshot, and at a configurable event interval — to catch drift and implementation bugs. A homomorphic digest that has silently desynchronized from reality is worse than no digest.
- **A Merkle tree over entity partitions, rebuilt at snapshots only.** A flat homomorphic hash tells you two states differ; it cannot tell you *where*. When a nightly replay check fails, the Merkle tree localizes the diverging subtree in O(log n) instead of forcing a manual diff of the whole world. Divergence localization is an operational necessity, not a nicety.

Do not use verkle trees. They solve proof-size problems December does not have, and Ethereum itself has moved toward a unified binary hash tree ([EIP-7864](https://eips.ethereum.org/EIPS/eip-7864)) for simplicity and post-quantum reasons.

Until that escalation, event envelopes carry the affected aggregate’s pre/post version and hash plus the previous event hash. Snapshot records carry the global state hash and algorithm version. Do not make lattice hashing a Gate 1 dependency without evidence.

## D7. Reading the event log in commit order

**The `sequence: 123` field in the event envelope must not be consumed with a naive high-water mark.** This is the single most common way an event-sourced system on PostgreSQL loses data, and the current architecture doc walks straight into it.

The failure: `bigserial` values are allocated at insert time, but transactions commit in a different order. A projection reading `WHERE sequence > :last_seen` can observe sequence 300 before sequence 250 has committed, advance its watermark past 300, and then never see 250. Sequences are also non-transactional, so rollbacks leave permanent gaps that are indistinguishable from not-yet-committed rows. The projection is now permanently, silently wrong — and because it is silent, the "projection rebuild equals live projection" invariant in [`06`](06-architecture-and-data.md) is the only thing that would ever catch it.

December’s Phase 1 solution is deliberately small:

**Enforced serialized writer.** The canonical kernel is logically single-threaded, so one fenced leader appends events. The sequence/stream version is assigned and events are committed inside that serialized transaction. Projections may consume only committed batches and checkpoint the batch/stream version, not an independently allocated `bigserial` watermark.

If December later introduces multiple event writers, it must adopt and test a real commit-order protocol—such as transactional batches with a committed batch table, database commit timestamps/LSN where appropriate, or a verified snapshot-fencing design. `xid8` ordering is not treated as commit ordering by itself.

The prior audit proposed the following snapshot-fencing query as defence in depth:

```sql
SELECT * FROM events
WHERE txid < pg_snapshot_xmin(pg_current_snapshot())
  AND (txid, sequence) > (:last_txid, :last_sequence)
ORDER BY txid, sequence;
```

It is retained as a research note, not the Phase 1 design. Transaction IDs are not commit sequence numbers, wraparound and visibility semantics require care, and the serialized writer already removes the race.

Additional operational rules:

- **`LISTEN`/`NOTIFY` is a doorbell, not a delivery mechanism.** It is not durable, it is lost on disconnect, and `NOTIFY` at commit takes a global exclusive lock that serializes all notifying commits — a measured ceiling in the low thousands of commits per second. Use it only to wake a poll loop that is already correct without it.
- **Isolation:** `READ COMMITTED` plus the single-writer lock and optimistic `(stream_id, expected_version)` concurrency. `SERIALIZABLE` buys nothing on a single-writer append path and adds predicate-lock overhead and retryable failures.
- **Partition the event table by simulated time** once past tens of millions of rows; keep the append path's index set minimal; keep partition count in the low hundreds.
- Expect roughly 5k events/s from a single writer on moderate hardware. See D8 — that is far above December's requirement, so throughput is not the binding constraint. Storage growth is.

## D8. Event volume and storage budget

No prior draft estimated how much history December produces, while committing to "keep canonical history indefinitely." The two must be reconciled before Phase 1 chooses a grid resolution, because **grid resolution is the dominant driver of event volume.**

Order-of-magnitude estimate, to be replaced by measurements at Gate 1:

| Source | Events per simulated day | Note |
|---|---|---|
| Resident activity, movement, transfers, speech | 300–1,500 | ~25–80 per full resident |
| Projects and construction | 50–300 | Bursty; near zero between projects |
| Health, physiology, demography | 50–200 | Daily boundary settlements |
| World processes (weather, hydrology, crops, vegetation, prey) | **100 – 40,000** | Entirely determined by event granularity policy |
| **Total** | **~500 – 42,000** | Two orders of magnitude of uncertainty |

That spread is a design decision, not an unknown. A 5 km × 5 km valley at 50 m resolution is 10,000 cells; at 25 m it is 40,000. Emitting one event per cell per day for vegetation and soil moisture produces 3.6–14.6 million events per simulated year *from vegetation alone* — which at ~1 KB per row is 4–15 GB per simulated year, before residents do anything.

**Policy:**

1. **World processes emit batched events with array payloads** — one `world.daily_advanced` event per subsystem per day carrying a compact typed array of per-cell deltas, not one event per cell.
2. **Emit only on material change.** A cell whose state is unchanged within declared tolerance emits nothing.
3. **Per-cell granularity is reserved for cells with residents, claims, structures, crops, or active hazards** — typically tens of cells, not thousands.
4. Target: **≤ 5,000 events per simulated day**, verified at Gate 1. Under this policy, at 72 simulated days per real day, the log grows roughly 100–400 MB per real day, or 40–150 GB per real year. That is affordable on local disk but it is not free, and it makes the backup and restore-drill requirements in [`08`](08-models-cost-operations-security.md) load-bearing rather than ceremonial.
5. **The prompt/response cache adds its own volume** — roughly 1–5 MB per simulated day after deduplicating stable prefixes. It is canonical (D5), so it is backed up too.
6. **Cold-tier archival is permitted; deletion is not.** Events older than a configured horizon may move to compressed object storage with their hashes retained online, so the chain remains verifiable without the bodies being hot.

## D9. Required tests

These belong in CI from Phase 1, not in a later hardening phase.

| Test | Asserts | Phase |
|---|---|---|
| Replay-from-empty golden histories | State hashes match at every checkpoint | 1 |
| Replay-from-snapshot | Snapshot + subsequent events equals full replay | 1 |
| Cache-miss abort | Replay with a deliberately evicted cache entry **fails loudly** and names the `decision_id` | 2 |
| Latency-shuffle | Same manifest, randomized artificial provider delays and completion order → identical history | 2 |
| Decision-retry divergence | A timed-out call whose retry returns a different command → first recorded resolution wins; no fork | 2 |
| Cross-platform divergence | Same log replayed on x86-64 and ARM64; report first diverging event, or pass under Option A | 1 |
| Unordered-iteration lint | No `set`/`frozenset` iteration, no `id()` ordering, no wall-clock call in kernel modules | 1 |
| Hash-seed sensitivity | Run under three `PYTHONHASHSEED` values → identical history | 1 |
| Incremental-vs-full digest | Homomorphic digest equals full recomputation at every snapshot | 1 |
| Sequence-gap injection | Deliberately commit events out of sequence order; every projection still sees all of them | 1 |
| Cosmetic-draw isolation | Adding draws to a cosmetic stream does not perturb any physical outcome | 1 |
| Dependency-bump replay | Bumping NumPy re-runs golden histories; any stream change is caught, not silently absorbed | ongoing |

A failure in any of these is a **Blocker** for the gate it belongs to. Determinism is not a property that can be added later; it is a property that is either maintained continuously or lost permanently.
