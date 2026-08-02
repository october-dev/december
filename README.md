# December: The Living Terrarium

**Status:** design revised after two audit passes; Phase 1 underway  
**Site:** [wegalabs.com](https://www.wegalabs.com/) · [the argument, in 6 minutes](https://www.wegalabs.com/plan)  
**Implementation status:** the determinism spine and `december.observer.v2` replay contract are built and tested ([`src/`](src/), [`tests/`](tests/)). Four scripted bodies now move, metabolize, eat, drink, lose health, and can die in the [visual preview](https://www.wegalabs.com/world). No ecology, cognition, or autonomous action selection exists yet.
**Audit status:** Gate 0 remains open. See the [first audit](AUDIT-FINDINGS.md) and [independent pass 2](AUDIT-FINDINGS-PASS-2.md). The second pass accepted the engineering premise. The unsafe public human-participant flow has since been removed; versioning, owner decisions, preregistration, parameter provenance, and scope decisions remain open.

December is a plan for an always-running, observable settlement whose inhabitants can survive, form relationships, build, govern, trade, disagree, elect leaders, split into factions, fight, migrate, reproduce, and die. The ambition is not a scripted AI soap opera. It is a small causal world capable of producing histories that surprise us for reasons we can inspect.

As a Wega Labs research program, its credible near-term subject is **persistent synthetic agency**: what allows an artificial resident to remain identifiable and causally continuous across memory consolidation, model changes, bodily and social change, and counterfactual forks. Consciousness and human continuity beyond biology are long-horizon motivations, not questions the current terrarium can decide. See the [lab charter and claims ladder](wiki/18-lab-charter-and-research-program.md).

The recommended first world is a fictional early agrarian valley. Its limited technology keeps the model tractable while still allowing scarcity, seasons, construction, property, commons, kinship, ritual, law, elections, disease, migration, raiding, war, and extinction. The current design cohort is 12 cognitively rich adults, 6 lightweight dependants, and a neighboring band represented at lower resolution until contact makes individuals relevant; Gate 1 demographic ensembles determine whether that number survives as the canonical choice.

## The core promise

When the observer returns after two days, something consequential may have happened—but not because a narrator rolled “war” on a story table. A drought may have reduced stream flow, damaged crops, depleted stores, intensified a property dispute, empowered a faction, caused a failed raid, spread infection among the wounded, and left the settlement near extinction. Every link is recorded. Recorded-event replay reproduces state exactly; kernel re-execution is deterministic only within its declared pinned environment and manifest.

This is an **observable AI terrarium**, not a claim that we have recreated humanity. “Realistic” means causally coherent, materially constrained, behaviorally plausible within declared limits, statistically tested, and auditable. It does not mean scientifically validated human prediction.

Reproducibility has three meanings: portable reconstruction from recorded events, deterministic re-execution of the kernel within its declared numeric environment, and fresh counterfactual simulation. Only the first is an event-log replay; a branch with new model responses is a new experiment. See [determinism and replay](wiki/14-determinism-replay-and-state-integrity.md).

## Start here

**[DECEMBER-BOOK.html](DECEMBER-BOOK.html)** — the entire product, research, architecture, ADR, and audit corpus in one searchable, self-contained review edition. It includes per-chapter notes, read tracking, and Markdown feedback export.

**[OVERVIEW.md](OVERVIEW.md)** — an 11-minute introduction in prose. What December is, the handful of ideas that actually matter, and what it refuses to claim. Read this before the wiki. A shorter version is on the web at [wegalabs.com/plan](https://www.wegalabs.com/plan).

**The kernel** is in [`src/december/`](src/december/) and the independently buildable read-only frontend is in [`viewer/`](viewer/). Phase 1 begins with the parts that cannot be retrofitted — integer-valued world state, hash-chained events, reproducible RNG streams, and exact replay — running on a deliberately small world so the foundation is tested before anything is built on it. `pytest` runs the determinism suite from [`wiki/14`](wiki/14-determinism-replay-and-state-integrity.md) §D9.

The documents below are a specification, not an introduction: roughly 48,000 words organised by subsystem, with the reasoning and sources behind every choice. They are meant to be audited against and referred to, not read front to back.

## Reading order

1. [Vision and north star](wiki/00-vision-and-north-star.md)
2. [Scope and realism contract](wiki/01-scope-and-realism-contract.md)
3. [Research landscape](wiki/02-research-landscape.md)
4. [World model and scenario](wiki/03-world-model-and-scenario.md)
5. [Agents, cognition, and memory](wiki/04-agents-cognition-and-memory.md)
6. [Society, economy, governance, and conflict](wiki/05-society-economy-governance-conflict.md)
7. [Architecture and data](wiki/06-architecture-and-data.md)
8. [Time, emergence, and observation](wiki/07-time-emergence-and-observation.md)
9. [Models, cost, operations, and security](wiki/08-models-cost-operations-security.md)
10. [Validation and experiments](wiki/09-validation-and-experiments.md)
11. [Roadmap and gates](wiki/10-roadmap-and-gates.md)
12. [Risks, decisions, and open questions](wiki/11-risks-decisions-open-questions.md)
13. [Independent audit guide](wiki/12-audit-guide.md)
14. [Sources](wiki/13-sources.md)
15. [Determinism, replay, and state integrity](wiki/14-determinism-replay-and-state-integrity.md)
16. [Parameter registry](wiki/15-parameter-registry.md)
17. [Cost model and model selection](wiki/16-cost-model-and-model-selection.md)
18. [Initial conditions and authorship](wiki/17-initial-conditions-and-authorship.md)
19. [Lab charter and research program](wiki/18-lab-charter-and-research-program.md)
20. [Experiment card template and R0 continuity protocol](wiki/19-experiment-card-template-and-r0-protocol.md)
21. [Open-source adoption and boundaries](wiki/20-open-source-adoption-and-boundaries.md)
22. [Four Bodies Need Food](wiki/21-four-bodies-need-food.md)

Documents 15–18 were added by the first audit pass. Documents 19–20 and ADR-009 were added by pass 2 to connect the terrarium to a falsifiable lab program, define the first experiment, and prevent operational identity from being confused with consciousness or human survival.

Architectural decisions are in [`wiki/adr/`](wiki/adr/).
The reviewer can copy [the audit report template](AUDIT-REPORT-TEMPLATE.md) to `AUDIT-REPORT.md`.

## Non-negotiable principles

- **The simulator owns truth.** Language models propose intentions and actions; typed systems decide what is possible and what occurs.
- **No invisible storyteller.** Exogenous events arise from explicit, state-conditioned hazard models. Narrative summaries never mutate the world.
- **Conservation before conversation.** Food, water, fuel, materials, labor, distance, health, and time cannot be invented in prose.
- **Private viewpoints.** Agents see local observations, testimony, records they can access, and fallible memories—not global state.
- **Consequences persist.** Death, injury, burned buildings, broken trust, law, debt, and ecological depletion survive context-window resets.
- **History is replayable.** All mutations are events with causal parents, seeds, actor, authorization, and before/after hashes.
- **Silence is allowed.** Agents do not need to manufacture drama. Uneventful seasons are valid.
- **Cost is a world constraint.** Budgets degrade cognition gracefully; they never corrupt physics or silently stop time.
- **Extinction is allowed.** It is a terminal historical outcome, followed by preservation and optional counterfactual forks—not a forced reset.
- **Claims climb one level at a time.** Behavioral continuity is not consciousness; human-model fidelity is not human continuation.
- **No human persona intake yet.** Human-subject work requires a separate ethics, consent, privacy, retention, and withdrawal protocol.
- **No implementation before audit.** Phase 0 ends only after all blocking audit findings are resolved or explicitly accepted.

## What “done with planning” means

Planning is complete only when the audit can trace each promised behavior to:

1. an authoritative state variable;
2. a transition rule or approved LLM decision boundary;
3. observable evidence;
4. an invariant or validation test;
5. a failure policy;
6. a phased implementation gate.

The current document is intended to reach that standard conceptually. Numerical parameters remain provisional until Phase 1 calibration; provisional values must be labeled and stored with provenance.
