# 17 — Initial Conditions: Declared Authorship and Experimental Variation

**Status:** added by the 2026-08-01 audit pass.

## The gap this closes

[`09`](09-validation-and-experiments.md)'s emergence audit asks: *"Did any prompt, fixture, or director text contain the outcome label beforehand?"* That is the right question, and the plan had no answer for the largest fixture of all — **the founding world itself**.

Nowhere did any prior document specify who writes the twelve residents' biographies, values, traits, skills, and relationships; who sets the initial stores, claims, and land quality; or where the founding charter comes from. Yet [`03`](03-world-model-and-scenario.md) already ships a scenario in which the founders "disagree about property, leadership, risk, and relations with a neighboring mobile band," claims over the best land are "ambiguous," and the charter conveniently leaves assembly procedure "unsettled."

Those are not neutral initial conditions. They are **the plot, pre-installed.** If the settlement later fractures over a property dispute and elects a leader to resolve it, December will have observed the thing it planted. The causal graph will be perfectly honest and completely uninformative, because the first cause lies outside the recorded history.

This is a Blocker-class confound for the project's central claim. It is also entirely fixable.

## The authorship boundary

> **Principle.** Every initial condition is authored, including one produced by a generator: developers choose variables, distributions, correlations, exclusions, validation bands, and which seed becomes canonical. The honest objective is not an “un-authored” state; it is **declared, reproducible, varied, and non-cherry-picked authorship**.

Initial conditions are part of the experimental design. Research cohorts sample registered initial-condition families. The public canonical world may be selected for observer legibility, but if it is selected rather than randomly drawn it is labeled an **exhibit** and excluded from unbiased cohort claims.

Three consequences:

1. Anything hand-authored in the founding state is **a developer intervention at t=0** and must be visible as such in the audit lineage.
2. Any initial condition that names or structurally guarantees an outcome later claimed as emergent is a confound. An outcome-word scan is useful but insufficient; review must also inspect proxy features and correlations that plant the same result without naming it.
3. The founding state must be **resampleable**, so that ensembles vary initial conditions rather than treating one hand-built world as ground truth.

## What must be removed from the current scenario

The Founding Valley description in [`03`](03-world-model-and-scenario.md) must be rewritten to state *material and structural* facts only. Specifically:

| Currently stated | Problem | Replacement |
|---|---|---|
| Founders "disagree about property, leadership, risk, and relations with the neighboring band" | Pre-installs the four axes of every subsequent conflict | State the **material** facts that could produce disagreement: unequal stores, overlapping use claims, differing household sizes and dependency ratios, different distances to water |
| Claims over the best land are "ambiguous" | Pre-installs the dispute | Record actual claims with actual evidence and actual overlaps; let ambiguity be a *derived* property of the claim ledger |
| Charter leaves assembly procedure "unsettled" | Pre-installs the constitutional crisis | Either the charter specifies a procedure or there is no assembly; "deliberately underspecified so it can be fought over" is authorship |
| "Neither utopian nor already doomed" | Reasonable as a design intent, but unfalsifiable as a spec | Express as a **measurable** initial condition: stores cover *N* days at current consumption, and the ensemble's 1-year survival rate under scripted policies falls in a declared band |

The general rule: **a founding fact is legitimate if it is a quantity, a location, a relationship with evidence, or a capability. It is illegitimate if it is a disposition toward a future conflict.**

Traits and values are the hard case. Residents do need heterogeneous values — [`07`](07-time-emergence-and-observation.md) correctly lists "heterogeneous but plausible goals/values" as a driver of possibility space. The distinction:

- **Permitted:** sampling each resident's values from a declared distribution over the value vocabulary in [`04`](04-agents-cognition-and-memory.md) (reciprocity, autonomy, tradition, security, status, generosity, truthfulness), with the sampling seed and distribution recorded.
- **Prohibited:** authoring a specific resident as "resents the steward" or "believes the upper field is hers by right," which is a grievance and a claim, not a value.

Biography is likewise permitted as *history* (where someone came from, what they know how to do, who they are related to, what they have done) and prohibited as *foreshadowing*.

## Generation procedure

The founding world is produced by a **seeded generator**, versioned like any other kernel component, and run before t=0.

```text
world_seed
  → terrain and hydrology synthesis (elevation, soil, water, vegetation, resource stocks)
  → resource and structure placement
  → household composition (sizes, ages, kin links) sampled from the demographic ranges in [15]
  → per-resident skills, values, and biography sampled from declared distributions
  → initial stores, tools, claims, and the founding charter
  → validation pass
  → world manifest entry recording generator version, seed, and every distribution used
```

Rules:

1. **Seeded and reproducible.** Same seed and generator version produce the same founding world, verified by the state-hash machinery in [`14`](14-determinism-replay-and-state-integrity.md).
2. **No LLM in the canonical generator.** Names, biography text, and flavor may be LLM-generated *as a separate, cached, content-addressed step*, but no LLM decides a quantity, relationship, claim, or capability. Prose describes the founding state; it never determines it.
3. **The generator is ablatable.** Ensembles must be able to resample residents while holding terrain fixed, and vice versa, so [`09`](09-validation-and-experiments.md) can attribute outcome variance to initial conditions versus dynamics. This is the only way to answer "would this have happened in a different founding world?"
4. **Validated before use.** The founding state passes the same invariants as any other state: no negative stocks, consistent claims, reachable water, feasible travel times, conserved totals.
5. **Recorded as genesis events.** The founding world enters the log as a genesis event set with `actor: generator@version` and `authorization: scenario_config`, so the audit trail begins before the first resident acts rather than at an unexplained initial snapshot.

## The founding charter

[`03`](03-world-model-and-scenario.md)'s three consensual rules are a reasonable *minimum institutional seed*, but they must be justified rather than assumed, because [`12`](12-audit-guide.md) lists "elections, police, war, or religion installed as assumptions despite emergence claims" as an automatic High finding.

The defensible position: the founders left an existing community, so they carry inherited norms. That is a fact about their history, not a designed outcome. Therefore:

- The charter is **generated as inherited culture** with recorded provenance, not hand-written to be interesting.
- A **no-charter condition belongs in the factorial design** when the question concerns institutional emergence. It need not appear in every unrelated ensemble. If institutions form only with inherited rules, that is evidence that cultural inheritance is causal, not a void result; the reported claim must say so.
- The charter's contents are **swept**, not fixed: charter-with-3-rules, empty charter, and a differently-seeded charter should all appear across runs.

## Operationalizing the success criteria

[`00`](00-vision-and-north-star.md) claims outcomes such as "at least three distinct governance forms arise across seeded runs." As written this is unfalsifiable — nothing defines what makes two governance forms *distinct*, and the emergence audit demands operational criteria for exactly this kind of label.

Each headline success criterion needs a definition fixed **before** the runs that test it, registered in the traceability matrix, and never adjusted afterward to fit an observed result. For governance form, a workable definition is a tuple over structural properties — *(selection method, scope of authority, term structure, enforcement mechanism, amendment rule)* — with two forms counted as distinct when they differ in at least two components and both persist beyond a declared duration and number of decisions.

The specific definition matters less than three properties: it is **structural** (readable off the institution registry, not off a summary), it is **pre-registered**, and it has a **persistence requirement** so a momentary configuration does not count. The same treatment is required for "faction," "war," "religion," "trade convention," and "settlement fission" before any of them is claimed.

## Required tests

| Test | Asserts |
|---|---|
| Generator determinism | Same seed and version → identical founding state hash |
| Outcome-label scan and feature review | No explicit target labels appear in founding fixtures; automated grep is followed by review for proxy features and guaranteed outcomes |
| Initial-condition ablation | Outcome variance is attributable to dynamics, not solely to founding draw |
| Charter factorial | When testing institutional emergence, compare registered charter/no-charter or alternative-inheritance conditions |
| Founding-state invariants | The generated world passes every kernel invariant before t=0 |
| Pre-registration check | Every operational definition used in a claim existed in the repository before the runs it describes — verifiable from version history |

## A note on version control

The project directory is **not currently a git repository**, yet [`12`](12-audit-guide.md)'s audit template asks for a "plan commit/version," [`06`](06-architecture-and-data.md)'s event envelope records `code_version: git:...`, and the pre-registration test above depends on being able to prove *when* a definition was written.

**Initialize version control before any further work.** Provenance claims that cannot be checked against history are assertions, and this plan asks the reader to trust rather a lot of them.
