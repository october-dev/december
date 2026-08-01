# 06 — Technical Architecture and Data

## Architecture overview

```text
                      ┌──────────────────────────┐
                      │ Observer UI / API        │
                      │ map · timeline · why     │
                      └─────────────┬────────────┘
                                    │ read models
┌───────────────┐       ┌───────────▼───────────┐       ┌─────────────────┐
│ Model gateway │◀─────▶│ Cognition orchestrator│──────▶│ Memory service  │
│ route/budget  │       │ private contexts      │       │ subjective only │
└───────────────┘       └───────────┬───────────┘       └─────────────────┘
                                    │ typed commands
                      ┌─────────────▼────────────┐
                      │ Command/API boundary     │
                      │ schema · auth · feasible │
                      └─────────────┬────────────┘
                                    │ accepted commands
                      ┌─────────────▼────────────┐
                      │ Authoritative kernel     │
                      │ world · people · rules   │
                      │ scheduler · RNG streams  │
                      └─────────────┬────────────┘
                                    │ immutable events
                ┌───────────────────▼───────────────────┐
                │ Event store + snapshots + projections │
                └──────┬───────────────┬───────────────┘
                       │               │
             ┌─────────▼──────┐  ┌────▼────────────────┐
             │ Metrics/traces │  │ Optional world view │
             │ cost/health    │  │ 2D or Luanti adapter│
             └────────────────┘  └─────────────────────┘
```

Only the command boundary writes to the kernel. The observer, director, memory service, model gateway, and visual adapter cannot mutate canonical state directly.

## Recommended stack (subject to spikes)

- Python 3.14 domain/kernel services (3.14 is the current stable line; 3.15 is due October 2026). Run the kernel on the **default GIL build** — free-threading is officially supported as of 3.14 but reintroduces interleaving nondeterminism that the replay guarantee depends on excluding.
- Mesa or a custom event loop behind a narrow `SimulationRuntime` interface.
- Pydantic or equivalent for command/event schemas.
- PostgreSQL for events, read models, policies, jobs, and configuration; JSONB only for versioned payloads, not untyped everything. Single-writer append path under an advisory lock, `READ COMMITTED` with optimistic `(stream_id, expected_version)` concurrency, and time-partitioned event tables. `LISTEN`/`NOTIFY` may serve as a wake-up doorbell only — it is not durable and its commit-time global lock serializes notifying transactions.
- Object storage/local content-addressed files for snapshots, prompt packets, response caches, and artifacts.
- pgvector or a separate vector store only for subjective semantic retrieval.
- FastAPI for read/control APIs.
- React/TypeScript visualization after the headless milestones.
- Redis is optional for ephemeral queues/locks, never authoritative truth.
- LiteLLM-compatible gateway and Langfuse/OpenTelemetry-compatible tracing.

No stack choice is final until its phase gate.

## Service boundaries

Begin as a modular monolith with separate packages and one database transaction boundary. Premature microservices would make replay and invariants harder. Logical modules:

```text
domain/       IDs, units, state types, commands, events
kernel/       scheduler, command pipeline, projections, snapshots, RNG
world/        geography, climate, hydrology, ecology, hazards
people/       physiology, health, demography, activities
economy/      lots, claims, transfers, recipes, tools, stores
projects/     blueprints, task DAGs, construction, maintenance
society/      relationships, groups, institutions, rules, elections
conflict/     grievances, mobilization, encounters, aftermath
cognition/    context, routing, action schemas, reviews
memory/       observations, testimony, beliefs, retrieval, consolidation
observer/     timelines, causal graphs, summaries, alerts
experiments/  seeds, sweeps, shadow worlds, metrics, reports
adapters/     web UI, Luanti/Craftium/Minecraft spikes
ops/          budgets, provider health, backups, migrations
```

Extract a service only after profiling, scaling, or security proves the need.

## Command processing

1. Receive command with idempotency key, originating `decision_id`, and expected state version.
2. Authenticate actor/service and check infrastructure capability.
3. Validate schema, unit types, referenced entities, timestamp, and visibility assumptions.
4. Evaluate physical/social preconditions from authoritative state.
5. Compute deterministic consequences and schedule future processes.
6. Draw from named RNG streams only where specified.
7. Append events atomically.
8. Update projections or rebuild them asynchronously.
9. Return an outcome observation appropriate to the caller.

**Idempotency operates at two levels, and the second is easy to miss.** A command idempotency key prevents a duplicate *delivery* from applying twice. It does not prevent the more likely failure: a model call times out, the orchestrator retries, and the model returns a *different* command. Both are valid, neither is a duplicate, and history forks silently. The `decision_id` — derived deterministically from world, branch, simulated time, actor, and trigger — is therefore the idempotency unit for cognition, enforced by a unique constraint rather than application logic. The first durably recorded resolution for a `decision_id` wins permanently.

Rejections are first-class records for debugging but need not enter canonical world history unless the attempted action itself was observable.

**Rejection responses are an information-leak channel and must be filtered.** [`04`](04-agents-cognition-and-memory.md) has the kernel return "feasible alternatives and reasons" when it rejects a command. Done naively this violates the epistemic-realism contract R3 outright: telling a resident that a transfer failed *because the granary holds only four measures* hands them a hidden quantity they never observed; offering a feasible-alternative list that omits a location silently reveals who is standing there. Every rejection reason and alternative must pass through the same visibility filter as an observation packet, and the hidden-state canary suite must include rejection-channel probes specifically. A rejection may say the action is not possible; it may only say *why* using facts the actor could already know.

## Event schema

All canonical mutations emit an envelope:

```json
{
  "event_id": "evt_...",
  "event_type": "inventory.transferred.v1",
  "world_id": "world_...",
  "branch_id": "canonical",
  "sim_time": "...",
  "recorded_at": "...",
  "sequence": 123,
  "actor_ids": ["person:..."],
  "entity_ids": ["lot:...", "store:..."],
  "command_id": "cmd_...",
  "causal_parent_ids": ["evt_..."],
  "correlation_id": "process_...",
  "authorization": ["capability:..."],
  "rng_draw_ids": [],
  "code_version": "git:...",
  "config_version": "cfg:...",
  "payload": {},
  "pre_state_hash": "...",
  "post_state_hash": "..."
}
```

Event types are immutable. Schema changes create a new version plus upcasters for read models. Historical payloads are never rewritten in place.

Three constraints on this envelope, specified in [`14`](14-determinism-replay-and-state-integrity.md):

- **`sequence` must not be consumed with a naive independently allocated high-water mark.** December starts with one fenced serialized writer and transactionally committed event batches/stream versions. A multi-writer design requires a separately proven commit-order protocol; transaction ID order is not assumed to be commit order.
- **Per-event hashes cover the event chain and affected aggregates, not the full world.** A canonical full-state hash is computed at snapshots. Incremental global/lattice hashing is optional only after profiling demonstrates the need.
- **The envelope gains `decision_id`** on any event originating from a model decision, which is the idempotency unit for cognition — see below.

## Major command/event families

| Domain | Commands | Events |
|---|---|---|
| Activity | start, continue, interrupt, rest | activity_started/progressed/interrupted/completed |
| Movement | plan route, depart, redirect | departed/entered_edge/arrived/blocked |
| Resources | harvest, process, transfer, consume, store | extracted/transformed/transferred/consumed/spoiled |
| Projects | propose, revise, authorize, contribute, test | proposed/compiled/authorized/worked/defect_found/completed |
| Communication | speak, signal, send messenger, publish | uttered/delivered/overheard/record_created |
| Society | invite, join, leave, promise, claim, dispute | group_formed/membership_changed/obligation_created/claim_contested |
| Government | propose rule, call election, vote, certify | rule_enacted/election_stage_changed/ballot_cast/result_certified/office_transferred |
| Health | provide care, isolate, treat | exposed/infected/symptom_changed/injured/recovered/died |
| Conflict | threaten, mobilize, raid, defend, negotiate | grievance_recorded/mobilized/encounter_resolved/truce_enacted |
| World | none or authorized maintenance | weather_realized/crop_advanced/fire_ignited/fire_spread/stock_regenerated |

## Causal links

We need more than temporal adjacency. Each process stores causal parents:

- **mechanistic parent:** rainfall realization caused moisture change;
- **decision parent:** observation and deliberation caused an irrigation command;
- **resource parent:** specific seed and labor events contributed to crop output;
- **institutional parent:** charter/rule/capability authorized a transfer;
- **stochastic parent:** named draw produced an accident or transmission.

The UI can therefore answer “why did this person die?” with a graph rather than an LLM guess. Causal links describe simulator dependency, not philosophical total causation.

## Deterministic randomness

Use splittable/counter-based RNG streams keyed by world seed, branch, subsystem, entity/process, and draw purpose. Adding a cosmetic random draw must not perturb crop yields. Every stochastic event stores distribution version, parameters, and sampled result.

LLM sampling is external nondeterminism. Canonical prompts and raw responses are content-addressed and cached; replay uses the cached response and **hard-fails on a cache miss rather than calling a live model**. A fresh-model rerun is a new branch.

**[`14`](14-determinism-replay-and-state-integrity.md) is the normative specification** for everything in this section and the three that follow. It separates portable reconstruction from recorded events, pinned-environment kernel re-execution, and fresh counterfactual branches. Phase 1 prefers fixed-unit conserved state, event/aggregate hash chains, serialized append, named RNG streams, and canonical snapshot hashes; more exotic integrity machinery is added only when measured scale requires it.

## Snapshots and replay

- Append-only events are the source of truth.
- Periodic snapshots accelerate recovery but are disposable derivatives.
- On startup, load the latest compatible snapshot and replay subsequent events.
- Nightly verify a random snapshot by rebuilding from an earlier checkpoint and comparing hashes.
- Before schema/config/model changes, fork a staging world and replay.
- Backups include database, snapshots, prompt/response cache, configuration, and code/version manifests.

## Read models

Separate projections serve:

- current map and entity state;
- person biography and subjective beliefs;
- inventory/claim ledger;
- institution/rule/office registry;
- timeline and story arcs;
- causal graph;
- metrics and alerts;
- cost/provider usage;
- audit diffs and replay status.

The director summarizes only projections and linked evidence. Its generated copy is cached as commentary, never canonical fact.

## World adapters

The kernel exposes a minimal adapter contract:

- render current public/spatial state;
- translate accepted physical commands into animations or engine actions;
- report adapter completion/failure without deciding domain outcomes;
- reconcile positions against kernel truth;
- support pause, reset from snapshot, and replay.

Phase order:

1. headless + simple web grid;
2. richer 2D canvas/isometric view;
3. Craftium/Luanti spike;
4. choose 2D or 3D based on observability, determinism, work, and performance—not spectacle alone.

## Invariants and transactional boundaries

Critical mutations—transfer, consumption, death, office transfer, project material use—append all necessary events in one transaction. Property-based tests generate arbitrary command sequences and assert:

- no negative stocks or duplicate custody;
- total conserved quantities reconcile with source/sink events;
- no overlapping exclusive activities;
- no action by dead/nonexistent actors;
- authority valid at event time;
- causality acyclic and parents precede children;
- event sequence and hashes are continuous;
- projection rebuild equals live projection;
- **no projection misses an event under crash/retry/batch-boundary injection**; if multiple writers are ever introduced, deliberate out-of-order commit injection becomes mandatory;
- **one `decision_id` yields at most one applied command**, even under retry with divergent model output;
- **rejection reasons and feasible alternatives leak no state the actor could not observe**;
- **affected-aggregate and event-chain hashes verify, and the snapshot state hash equals a full recomputation**.

## Event volume is a design decision, not a discovered quantity

Grid resolution is the dominant driver of history size, and the plan commits to keeping canonical history indefinitely. A 5 km × 5 km valley at 50 m resolution is 10,000 cells; emitting one event per cell per day for vegetation alone produces millions of events and gigabytes per simulated year before any resident acts.

Policy, specified fully in [`14`](14-determinism-replay-and-state-integrity.md) §D8: world processes emit **batched events with typed array payloads**, one per subsystem per day, not one per cell; nothing is emitted for a cell unchanged within tolerance; per-cell granularity is reserved for cells with residents, claims, structures, crops, or active hazards. Target **≤ 5,000 events per simulated day**, verified at Gate 1. The prompt/response cache is canonical and is backed up alongside the log.
