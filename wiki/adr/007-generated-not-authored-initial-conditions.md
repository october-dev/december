# ADR-007 — Initial conditions are declared, randomized, and varied

- **Status:** Accepted for audit
- **Date:** 2026-08-01 (added by audit pass)

## Context

December's central claim is that its histories are unscripted but explainable. Its own emergence audit asks whether any prompt, fixture, or director text contained an outcome label beforehand.

No prior document said who authors the founding state. Meanwhile the scenario shipped with founders who "disagree about property, leadership, risk, and relations with a neighboring mobile band," land claims that are "ambiguous," and a charter whose assembly procedure is "unsettled."

Those are not initial conditions. They are the plot. A settlement that later fractures over property and elects a leader to adjudicate it would be reproducing what was planted, and the causal graph would be perfectly honest while explaining nothing — because the first cause sits outside the recorded history.

## Decision

Initial conditions are authored even when generated: the generator’s variables, distributions, exclusions, correlations, and accepted seeds are human choices. The founding state is produced by a **seeded, versioned generator** whose full provenance is recorded in the world manifest and whose output enters the log as genesis events attributed to `generator@version`.

A founding fact is legitimate if it is a **quantity, a location, a relationship with evidence, or a capability**. It is illegitimate if it is a **disposition toward a future conflict**. Values may be sampled from a declared distribution; grievances and claims-of-right may not be authored.

No LLM decides a quantity, relationship, claim, or capability. Prose may describe the founding state; it never determines it.

The inherited charter is permitted as recorded cultural inheritance. Registered charter/no-charter or alternative-inheritance conditions are required when an experiment makes a claim about how institutions form.

Every success criterion that uses a label — "governance form," "faction," "war" — requires a **pre-registered operational definition**, verifiable from version history as predating the runs it describes.

## Consequences

- [`03`](../03-world-model-and-scenario.md)'s Founding Valley description was rewritten to state material and structural facts only.
- An automated outcome-label scan over scenario fixtures runs in CI.
- Ensembles can resample residents while holding terrain fixed and vice versa, so outcome variance can be attributed to dynamics rather than to the founding draw.
- Version control becomes a prerequisite: pre-registration claims are unverifiable without history.
- A canonical observer world selected for legibility is labeled an exhibit and excluded from unbiased cohort claims.

## Rejected alternatives

- **Hand-authoring an evocative founding scenario.** It produces better first runs and destroys the ability to claim anything about them.
- **Generating biographies and tensions with an LLM.** It moves the authorship rather than removing it, and makes it harder to audit.
- **Declaring initial conditions out of scope for the emergence audit.** The founding state is the largest fixture in the system.
