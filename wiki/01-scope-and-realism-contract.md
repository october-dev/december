# 01 — Scope and Realism Contract

## Why an early agrarian settlement

Modern society would require finance, mass media, electricity, industrial supply chains, bureaucracy, transport, medicine, law, and thousands of invisible institutions before one convincing day could occur. A prehistoric hunter-gatherer band is tractable but offers less construction, durable surplus, office, property, and formal governance.

The recommended starting point is a **fictional early agrarian frontier**, inspired by but not presented as any specific culture. It has mixed farming, gathering, hunting, fishing, pottery, fiber, wood and stone construction, storage, simple water works, and oral/marked records. This gives us:

- seasons, harvests, spoilage, soil decline, and food storage;
- households, kinship, commons, inheritance, and inequality;
- multi-day buildings and infrastructure;
- enough surplus for specialists and offices;
- nearby groups, trade, migration, territorial conflict, and epidemic contact;
- few enough technologies that recipes and capabilities can be enumerated.

The fictional setting avoids claiming historical authenticity. Every parameter inspired by scholarship must carry provenance, confidence, and sensitivity range.

## Initial scope

### Current design cohort—not a validated optimum

- 12 full-cognition adult residents in 6 households.
- 4 child dependants and 2 elders initially use lightweight policy cognition but retain bodies, relationships, needs, memory, and promotion to full cognition when relevant.
- One neighboring band begins as an aggregate population with stores, territory, disposition, and internal factions. Named individuals are materialized when contact, migration, diplomacy, or conflict makes them relevant.
- Births create lightweight persons; maturation promotes them. Death is permanent.

This hybrid “level of detail” policy spends tokens on consequential perspectives without turning dependants or outsiders into mere counters.

#### The candidate population is marginal, and that is a design constraint rather than a caveat

Eighteen people is below many modeled recommendations for a viable isolated human population, while historical small-founder cases depended on conditions and outside contact that are not clean substitutes for December ([`15`](15-parameter-registry.md) §C). These sources bound questions; they do not establish a universal threshold or validate this cohort.

So the honest statement is that December's founding group is **marginal, not impossible** — and the interesting design question is what makes the difference. Four consequences follow, and all four are binding:

1. **Demographic stochasticity dominates.** With expected births and deaths each in the single digits per decade, run-to-run variance is comparable to the mean. A substantial fraction of runs will end for no interesting reason. Validation must therefore compare every claimed collapse cascade against a **null demographic model** with no social mechanisms, or it cannot distinguish causality from noise.
2. **Partner availability matters immediately.** Chance age/sex-ratio skews and socially permitted matching can constrain births before genetic load becomes the dominant concern. December therefore models partner eligibility explicitly and treats any literature-derived multiplier as a sensitivity range, not a law.
3. **Network severance is one plausible failure mechanism.** Historical cases suggest outside exchange and migration can matter, but they do not identify one universal cause of small-settlement failure. December tests boundary connectivity as a mechanism instead of importing a historical narrative.
4. **In-migration and exogamy are therefore load-bearing mechanics.** The boundary world is not primarily a source of conflict and disease; it is the lifeline. It must exist from **Phase 3, not Phase 5**, or every institutional experiment runs inside a closed, guaranteed-declining population.

One neighbor of similar size is not enough — two settlements of 18 give a pool of ~36, roughly a quarter of the minimum viable mating network of ~150–500. See [`03`](03-world-model-and-scenario.md) for the recommended regional-aggregation mechanic.

If the observer experience depends on generational turnover or inherited institutions, the founding size must be revisited. Gate 1's ensembles report extinction rate as a function of founding population, and that curve sets the final number.

### Map

A hex or square grid representing roughly a valley-scale walkable region. Cells store elevation, slope, soil class, moisture, surface water, vegetation/fuel, resource stocks, ownership/use claims, structures, and current occupants. Exact scale is a Phase 1 decision; distance and travel time must be internally consistent.

### Technology boundary

Initial capabilities include fire, shelters, storage pits, wood/stone tools, cordage, baskets, pottery, fishing, hunting, gathering, two staple crops, and simple irrigation. Metal, writing, animal traction, wheeled transport, and complex fortification are absent until deliberately added as tested expansion packs.

### Time horizon

- Target canonical pace: configurable, initially 1 real hour = 1 simulated day while attended and up to 1 real hour = 3 simulated days while unattended.
- Kernel tick: event-driven with daily physiological/ecological boundaries.
- Cognition cadence: on meaningful triggers, not every tick.
- Initial soak target: seven real days / several simulated months, then multi-year accelerated experiments.

The mapping is not sacred. We choose it only after cost and behavioral tests. Long-term historical change needs accelerated experimental branches even if the canonical world moves slowly.

## The realism contract

“Super realistic” is otherwise an invitation to hide hand-waving. This project uses six testable meanings.

### R1. Material realism

Resources have quantities, locations, quality, ownership/custody, and transformations. Actions consume time, energy, tools, inputs, and access. Outputs cannot exceed inputs plus modeled growth or extraction.

**Required evidence:** stock-flow ledgers, conservation/property tests, capacity limits, spoilage and loss events.

### R2. Temporal and spatial realism

People cannot be in two places, learn news instantly, complete work without elapsed time, or respond before observing an event. Travel, communication, construction, disease, crops, injuries, and institutions operate at different timescales.

**Required evidence:** interval overlap checks, path/travel events, message provenance, scheduled processes.

### R3. Epistemic realism

World truth, an agent’s observations, their beliefs, public records, rumor, and retrospective narration are separate objects. Memory may be lossy or biased, but the event log is not.

**Required evidence:** information lineage for every decision; tests preventing leakage of hidden state.

### R4. Behavioral plausibility

LLMs choose among feasible actions using needs, commitments, norms, goals, emotions-as-appraisals, relationships, and bounded plans. Behavior is neither perfectly rational nor unconstrained improvisation. Traits modulate decisions; they do not dictate them.

**Required evidence:** scenario tests, repeated-seed behavioral distributions, ablations, contradiction rates, independent human review.

### R5. Structural realism

Macro events must arise from plausible micro mechanisms and feedback loops. “War” is mobilization, logistics, communication, risk, combat encounters, injury, morale, and political aftermath—not a scalar event. “Election” is eligibility, candidacy, information, voting, counting, disputes, transition, and powers.

**Required evidence:** causal graphs and module-level ODD descriptions.

### R6. Empirical humility

The model declares what is calibrated, borrowed, speculative, or designed. It reports sensitivity and uncertainty rather than presenting a cinematic outcome as human science.

**Required evidence:** parameter registry ([`15`](15-parameter-registry.md)), provenance, ensemble runs, validation report, “known invalid” list.

### R7. Scale honesty

A mechanism must be valid **at December's population size**, not merely valid somewhere. Parameters and model structures borrowed from populations of thousands or millions are frequently meaningless at n=18, and a mechanism tuned until it "works" at this scale may be encoding a rate that cannot physically exist.

The disease module is the worked example: no acute, directly transmitted, immunizing infection can be endemic in eighteen people, because critical community size for such infections is in the hundreds of thousands ([`15`](15-parameter-registry.md) §D). An SEIR model tuned until epidemics appear at a satisfying frequency would be fabricated epidemiology wearing the costume of rigor.

**Required evidence:** for every subsystem, an explicit statement of the population range over which its structure is valid, and a test that the subsystem behaves correctly — including degenerately, where that is the correct behavior — at n=18. Where the honest answer is "this mechanism cannot operate at our scale," the subsystem is redesigned around one that can, not tuned until it produces output.

## Realism tiers

Every subsystem receives a tier so ambition does not become accidental scope.

| Tier | Meaning | Example |
|---|---|---|
| 0 Placeholder | Interface only; not allowed in canonical long runs | Combat returns a fixed result |
| 1 Causally coherent | Correct stocks, timing, preconditions, broad feedback | Crop yield responds to labor, water, soil, weather |
| 2 Pattern-calibrated | Reproduces several target qualitative/quantitative patterns | Seasonal hunger and storage reduce variance in intake |
| 3 Domain-reviewed | Assumptions and results reviewed by a relevant expert | Epidemic module reviewed by an epidemiologist |

Canonical launch requires Tier 2 for food/water, energy/health, demographics, construction, information, and core social exchange; Tier 1 for conflict and government; no Tier 0 modules enabled. Tier 3 is aspirational.

## Laws of the world

These are invariants, not configurable personality choices:

1. **Identity:** every entity and event has a stable ID.
2. **No negative stocks:** transfers and consumption are atomic and bounded.
3. **Conservation:** mass-like resources are created only by declared source processes and destroyed only by declared sinks.
4. **Single location:** a person occupies one location or one travel edge at a time.
5. **No retrocausality:** decisions use information available before their timestamp.
6. **Mortality:** dead agents cannot act; estates and obligations transition by a declared rule.
7. **Authority:** an institutional action requires a currently valid capability.
8. **Idempotency:** repeated command delivery cannot duplicate its effect.
9. **Seeded randomness:** all stochastic draws use named streams recorded with events.
10. **Narrative impotence:** summaries, cameras, and observer queries have no world-write capability.

## What can be random

Randomness represents modeled uncertainty or variation, not authorial convenience. Each hazard has:

- eligibility conditions;
- a rate or probability conditioned on state;
- a named RNG stream and draw ID;
- severity distribution;
- spatial footprint;
- downstream mechanics;
- provenance/confidence;
- tests for impossible and degenerate rates.

Examples include rainfall, lightning ignition, conception, accident, pathogen introduction, transmission, hunting success, and combat injury. A generic “dramatic event” roll is forbidden in the canonical world.

## Ethical and interpretive limits

- The agents are software personas; we avoid claims of consciousness, suffering, or moral equivalence to people.
- Population attributes should not encode race, ethnicity, or real-world protected-group stereotypes.
- Reproduction and kinship remain non-explicit, abstract state transitions with consent constraints.
- Violence is represented analytically, without graphic content and without optimizing for cruelty.
- The observer is told when a claim is a model inference, a resident belief, or direct world state.
- No outcome should be used to make policy claims about real communities without an entirely separate, domain-reviewed validation effort.
