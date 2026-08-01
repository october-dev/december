# 10 — Phased Roadmap and Decision Gates

## Rule: build from causality outward

The project should resist the temptation to begin with a pretty town and talking avatars. Every phase has an artifact, experiments, acceptance gate, and explicit exclusions.

## Phase 0 — Design and audit

**Goal:** turn ambition into a falsifiable, implementable specification.

Deliverables:

- this wiki and ADRs;
- ODD skeleton per subsystem;
- traceability matrix from promise to state/rule/test/UI;
- parameter registry template and source-quality rubric;
- threat model and cost envelope template;
- external audit report with blocking/non-blocking findings;
- resolution log signed off by owner and reviewer.
- lab charter, claims ladder, and first preregistration-ready experiment card.

Gate 0:

- no unresolved contradiction about authoritative truth, time, death, authority, or observer intervention;
- MVP scope and realism tiers accepted;
- audit finds no missing mechanism that would make the core promise impossible;
- public language matches the claims ladder in [`18`](18-lab-charter-and-research-program.md), and any human-participant solicitation is disabled;
- the canonical world is designated as an exhibit/soak while research claims are assigned to controlled cohorts;
- **version control initialized** — provenance and pre-registration claims are unverifiable without it, and the audit template already asks for a plan commit;
- **the pre-Phase-1 owner decisions in [`11`](11-risks-decisions-open-questions.md) are answered**: monthly spend cap, licensing posture, deployment target, pace range, and publication intent;
- implementation remains unstarted until this gate.

## Phase R0 — Identity-measurement spike

**Goal:** test the proposed research wedge before building a civilization around it.

In a two-to-three-week disposable prototype, create a small suite of repeated decisions, autobiographical recall, commitment tracking, irrelevant-context perturbations, bounded memory damage/restoration, and model transplant. Compare history-conditioned agents against clean-slate, prompt-only, and history-only baselines. Publish the experiment card, raw outputs, scoring code, failure analysis, and cost.

This spike may run before or alongside the early kernel work. It is intentionally not the canonical world.

Gate R0:

- at least one continuity measure has acceptable inter-rater or test-retest reliability;
- the measure distinguishes meaningful continuity from mere phrase/style matching;
- adaptive change is not incorrectly scored as identity loss;
- the model-transplant comparison and all exclusions are specified before results are inspected;
- results justify integrating the measurement harness into Phase 2, or the research wedge is revised without discarding the causal-world project.

## Phase 1 — Headless causal kernel

**Goal:** prove the material world without LLMs.

Build:

- IDs/units, command pipeline, events, RNG, snapshots/replay;
- small grid, season/weather, water, renewable resources;
- food/energy, lots, activity/time, travel;
- crops/stores/spoilage, basic tools and construction DAG;
- minimal health/demography;
- scripted policies and experiment runner;
- raw metrics/reconciliation reports.

Do not build: dialogue, elections, war, 3D world, rich UI.

Experiments: thousands of seeds, conservation/property tests, famine/overshoot scenarios, Mesa versus custom runtime benchmark.

Gate 1 — **quantified**, because "large safety margin" is not a gate:

- deterministic replay and all invariants pass, including the full determinism suite in [`14`](14-determinism-replay-and-state-integrity.md) §D9;
- **the numeric representation and quantization policy is made and recorded** (ADR-006). Physical stocks may use fixed units or explicitly quantized arithmetic; portable bit-identity is not promised by default;
- no dominant infinite-resource or starvation exploit;
- target ecological/subsistence patterns are tunable across plausible ranges, including the depletion halo and the seed-grain constraint;
- **the null demographic model is built and its extinction-rate curve against founding population size is published** — this sets the final founding population, and every later causal claim is measured against it;
- **≤ 5,000 events per simulated day** under the batched-event policy, measured;
- **≥ 500 simulated days per wall-clock hour** in headless no-LLM mode, giving roughly 25× headroom over the fastest canonical pace;
- **measured activation counts and context sizes replace the estimates in [`16`](16-cost-model-and-model-selection.md) §1**, and the cost model is re-derived.

## Phase 2 — Four minds in a hut

**Goal:** prove bounded cognition and private memory.

Build:

- four adult residents, cognition loop, typed actions, provider gateway;
- objective/subjective information separation;
- episodic/belief/social/commitment memories;
- communication, promises, joint tasks, refusal;
- simple grid UI, person timeline, prompt/event trace;
- model admission and hidden-state canary suite.

Do not build: full politics, neighboring group, organized combat.

Scenarios: shared meal, missing tool, contradictory testimony, rescue versus hunger, multi-day shelter, provider outage/model swap.

Gate 2 — quantified:

- agents never directly mutate truth or access hidden facts, **including through rejection reasons and feasible-alternative packets**;
- multi-day plans and promises survive restarts/context compaction;
- schema/fallback/cost targets pass across approved models, with the **validity ladder** demonstrated end to end on a provider that lacks strict schema decoding;
- **refusal rate and character-break rate measured** for every admitted model over the full action grammar, and recorded in its profile;
- **behavioral diversity demonstrated**: residents with materially different values and histories produce measurably different decisions;
- **cache hit rate ≥ 60%** on Tier B under the activation scheduler, or the scheduler is redesigned;
- **latency-shuffle and decision-retry tests pass** — identical history regardless of provider timing;
- conversation does not dominate time without social cause.

## Phase 3 — Founding settlement

**Goal:** establish the 12-adult social/economic world.

Build:

- households/dependants, relationships, claims/gifts/debts;
- **the aggregate neighboring group, with migration, exogamy, and exchange** — moved forward from Phase 5;
- the seeded founding-world generator per [`17`](17-initial-conditions-and-authorship.md);
- project compiler v1 and settlement construction;
- groups, norms, meetings, disputes, simple rules;
- sparse activation, cognition tiers, and cache-aware activation batching;
- “Since you left,” event/why/person/project pages;
- accelerated integrated experiment harness.

**Why the neighbors moved earlier.** Twelve founders cannot sustain a population ([`01`](01-scope-and-realism-contract.md)). Deferring outsiders to Phase 5 means every Phase 3 and Phase 4 experiment runs inside a closed, guaranteed-declining population — institutional findings would be confounded by a dying world. The *exchange and migration* path ships here; the *raiding* path still waits for Phase 5, so the neighbors arrive as a lifeline before they arrive as a threat.

Gate 3:

- at least three useful un-scripted multi-person projects complete across runs;
- inequality/cooperation/free-riding vary by conditions without ledger violations;
- identity and memory remain stable over a multi-season test;
- **the founding generator is deterministic, and the outcome-label scan passes** — no grievance, dispute, faction, or governance term appears in any founding fixture;
- **in-migration keeps population viable across a multi-year accelerated run** at a rate distinguishable from the null model;
- daily cost estimates fit the owner-approved envelope, **measured rather than projected**.

## Phase 4 — Institutions, elections, and collective failure

**Goal:** allow residents to create and contest governance.

Build:

- institutional grammar, offices/capabilities, rule lifecycle;
- proposal/deliberation/decision/appeal;
- multiple election procedures and audits;
- enforcement, legitimacy, group/faction lifecycle;
- commons and disputed-water scenario suite.

Gate 4:

- isolated election/governance tests pass, including ties, fraud attempts, refusal, succession;
- multiple governance forms arise across conditions;
- legal validity, compliance, and legitimacy remain distinct;
- no office can exceed compiled capabilities.

## Phase 5 — Disease, fire, outsiders, and conflict

**Goal:** add rare high-consequence cascades only after their foundations are trustworthy.

Build:

- the **five-mechanism health model** from [`03`](03-world-model-and-scenario.md) — introduced epidemics, environmental transmission, zoonoses, chronic/latent infection, and helminths — not a single generic SEIR pathogen;
- fire fuel/ignition/spread/damage;
- materialization of named individuals from the aggregate neighbor (the group itself shipped in Phase 3);
- diplomacy, escalation, mobilization, encounter combat, aftermath;
- extinction/abandonment classification and preservation.

Gate 5:

- hazards have provenance, named RNG, validation scenarios, and sensitivity report;
- introduced acute outbreaks show the expected finite-population distribution across ensembles—including fade-outs and potentially large outbreaks—without treating intermediate final sizes as bugs, and no endemic acute immunizing infection persists at n=18;
- **helminth load and rodent zoonoses emerge from sedentism, sanitation, and storage variables** rather than being set parametrically;
- neither inevitable peace nor constant war/extinction across the accepted region, **with conflict frequency reported as a swept parameter inside the contested empirical range, never as a calibrated finding**;
- combat conserves participants/equipment, respects logistics, and causes persistent aftermath;
- **every conflict statistic is reported with its model refusal rate**;
- director cannot initiate or alter hazards/conflict.

## Phase 6 — Embodiment and presentation

**Goal:** make the world beautiful to observe without moving truth into the renderer.

Build/spike:

- polished 2D/isometric UI and Craftium/Luanti adapter comparison;
- animations from authoritative events;
- replay/viewpoint/causal graph;
- read-only director summaries with factuality checking;
- optional generated art/audio only after a separate asset plan.

Gate 6 decision matrix:

| Criterion | Weight |
|---|---:|
| Preserves determinism/replay | 25% |
| Makes causal state legible | 20% |
| Integration/maintenance burden | 15% |
| Supports resident construction | 15% |
| Performance/headless operation | 10% |
| Visual wonder/observer appeal | 10% |
| License/distribution fit | 5% |

Choose 3D only if it clears the weighted gate. A gorgeous view that hides truth is a regression.

## Phase 7 — Canonical launch

**Goal:** one continuously running, preserved history.

Before launch:

- seven-day staging soak;
- restore drill and provider/budget chaos tests;
- final independent audit and known-limit report;
- version-lock code/config/prompts/models;
- set canonical seed, initial world manifest, hard budgets, alerts;
- declare observer intervention policy.

After launch:

- do not tune the world because a particular story is boring or upsetting;
- version behavioral changes and test in forks;
- publish weekly integrity/cost/known-anomaly report;
- preserve extinction rather than secretly undo it.

## Phase 8 — Expansion packs, not core creep

Possible later modules:

- metallurgy and specialist production;
- animals, traction, transport, expanded trade;
- writing, archives, schools, religion/ritual institutions;
- multiple fully simulated settlements;
- richer inheritance, marriage/kinship systems after review;
- environmental disease routes and more ecology;
- 3D construction; observer-controlled noncanonical experiments.

Each expansion states new variables, transition rules, validation patterns, compute/token impact, migration path, and failure modes. It cannot enter the canonical world merely because an agent mentions it.

## Rough effort shape, not a promise

For one experienced builder using coding agents, this is a multi-month project, not a weekend demo. A plausible order-of-magnitude is:

- Phase 0: 1–2 weeks including audit/revision;
- Phase 1: **6–12 weeks**;
- Phase 2: 3–5 weeks;
- Phase 3: 6–10 weeks;
- Phases 4–5: 8–14 weeks;
- Phase 6–7: 4–8 weeks.

**Phase 1 was revised upward by the audit.** The original 3–6 weeks already covered event sourcing, replay, RNG discipline, snapshots, terrain, seasons, weather, hydrology, renewable resources, energy, lots, activities, travel, crops, storage, spoilage, tools, a construction DAG, health, demography, scripted policies, and an experiment runner. It now also covers the determinism suite, explicit numeric policy, simple state/event hashes, serialized commit-order-correct writing, and the null demographic model. Advanced incremental hashing and multi-writer fencing are profiling-driven later options, not Phase 1 obligations. Six weeks remains optimistic for the retained list.

These ranges remain planning placeholders and should be replaced after Phase 1 throughput and complexity measurements. A compelling smaller launch could stop after Phase 4 and add hazards incrementally.

## Kill/pivot criteria

Pause or change architecture if:

- causal invariants cannot be kept across LLM actions;
- meaningful behavior requires global-state leakage;
- cost per simulated day stays above the approved envelope after sparse activation;
- outcomes are dominated by prompt wording rather than world conditions;
- replay cannot be made reliable;
- the project requires an omniscient storyteller to remain interesting;
- a selected engine prevents necessary observability or autonomy;
- seven-day operation needs repeated human repair.
- operational-identity metrics collapse to writing style, self-report, or prompt-template artifacts;
- public attention rewards stronger claims faster than evidence can support them;
- the canonical exhibit repeatedly becomes the source of post-hoc scientific claims.
