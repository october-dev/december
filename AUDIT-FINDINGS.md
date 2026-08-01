# December Plan — Audit Findings, Pass 1 (historical)

> **Status notice (2026-08-01):** This report records the first audit and is not the current gate verdict. Several remedies below were themselves revised after a second independent audit—for example strict epidemic bimodality, `xid8` fencing, per-event lattice hashing, “generated not authored,” and cost/pricing claims. Use [`AUDIT-FINDINGS-PASS-2.md`](AUDIT-FINDINGS-PASS-2.md) for the current verdict and the wiki/ADRs as the current specification.

**Reviewer:** Claude (Fable 5), adversarial audit pass
**Date:** 2026-08-01
**Plan version:** pre-git (no repository initialized — see F-19)
**Verdict:** `REVISE` → resolved in place. **READY FOR PHASE 1 conditional on the five owner decisions in §Open.**

This pass followed [`wiki/12-audit-guide.md`](wiki/12-audit-guide.md). Unlike the protocol's default, findings were **remediated in the same pass** rather than left for a response document, because the plan had not yet been implemented and the corrections were structural rather than contested. Every finding below states where the fix landed.

## Executive summary

The plan is unusually good. Its instincts — kernel owns truth, event-sourced history, capability-based authority, read-only director, no arbitrary agent code, ablations over anecdotes — are the right ones, and it anticipates most of the ways this kind of project fails. The writing is disciplined about the difference between what is designed and what is claimed.

Its weakness is uniform and diagnosable: **it deferred every question whose answer might constrain the ambition.** Parameters were "to be calibrated in Phase 1." Cost was "to be refreshed before budgeting." Determinism was asserted rather than specified. Initial conditions were never assigned an owner. Four of those deferrals turned out to hide problems that would have surfaced deep into implementation, when they would have been expensive or fatal:

1. The **replay guarantee**, on which every integrity promise depends, was **not achievable as written**.
2. The **disease module** was specified around a mechanism that **cannot operate at eighteen people**.
3. The **founding scenario** contained the **plot it was supposed to discover**.
4. The **cost model** — the top-rated operational risk — had **no bottom-up estimate**, and the one figure it did cite priced a promotional rate for a now-legacy model.

A fifth issue is subtler and, in my judgment, the most likely to embarrass the project later: **at n=18, demographic noise will produce collapses that look exactly like causal cascades**, and nothing in the validation plan distinguished them.

All five are now addressed. Four new documents were added ([`14`](wiki/14-determinism-replay-and-state-integrity.md), [`15`](wiki/15-parameter-registry.md), [`16`](wiki/16-cost-model-and-model-selection.md), [`17`](wiki/17-initial-conditions-and-authorship.md)), three new ADRs recorded, fifteen risks added, and the bibliography corrected — it contained a fork cited as an upstream project, two wrong licenses, a misattributed failure taxonomy, and several stale facts.

**The premise survives the audit.** Nothing found here makes the core promise impossible. Two findings (F-05, F-06) do constrain what the world can honestly claim to be, and one (F-04) means the settlement needs its neighbors earlier than planned.

## Blocker findings

| ID | Finding | Consequence | Resolution |
|---|---|---|---|
| **F-01** | "Bit-for-bit identical replay" is unachievable for a Python float kernel. glibc explicitly disclaims correctly rounded transcendentals; FMA contraction and SIMD reduction order differ across architectures; NumPy guarantees nothing across builds. Separately, **no LLM provider offers reproducible sampling** — Anthropic has no seed parameter at all. | Every integrity promise — event sourcing, shadow worlds, causal UI, the audit protocol itself — rests on a claim that would fail the first time an auditor replayed a history on their own machine. | [`14`](wiki/14-determinism-replay-and-state-integrity.md) + [ADR-006](wiki/adr/006-pinned-environment-determinism.md). Restated as **pinned-environment determinism**, with an integer-state option decided at Gate 1. Response cache made canonical; replay hard-fails on a miss. |
| **F-02** | Reading the event log by `bigserial` high-water mark **silently loses events**. Sequence values are allocated at insert but transactions commit out of order, so a projection can advance past an event that has not yet committed and never see it. Rollbacks leave indistinguishable gaps. | Permanent, silent projection corruption. The only check that would catch it is the rebuild-equals-live invariant, and by then the cause is long gone. | [`14`](wiki/14-determinism-replay-and-state-integrity.md) §D7. Enforced single writer under advisory lock, plus `xid8` snapshot fencing as defence in depth. Sequence-gap injection test added. |
| **F-03** | The founding scenario **pre-installs its own outcomes**: founders who "disagree about property, leadership, risk"; land claims that are "ambiguous"; a charter whose assembly procedure is "unsettled." No document assigned ownership of initial-condition generation. | The project's central claim collapses. A settlement that fractures over property and elects a leader would be reproducing what was planted, and the causal graph would be honest and worthless — the first cause sits outside recorded history. | [`17`](wiki/17-initial-conditions-and-authorship.md) + [ADR-007](wiki/adr/007-generated-not-authored-initial-conditions.md). Scenario rewritten to material facts only; seeded generator; outcome-label scan in CI; mandatory no-charter control arm; pre-registered definitions. |
| **F-04** | **Eighteen people is below every modelled viability threshold** (demographic ABMs put the floor at 40 and near-certainty at 150), the founder lineages exhaust within two to three generations, and demographic variance rivals the mean. Outsiders were deferred to Phase 5. | Every Phase 3 and Phase 4 institutional experiment would run inside a closed, guaranteed-declining population, confounding all institutional findings. | [`15`](wiki/15-parameter-registry.md) §C, [`01`](wiki/01-scope-and-realism-contract.md), [`03`](wiki/03-world-model-and-scenario.md). Aggregate neighbor **moved to Phase 3**; exogamy and in-migration promoted to load-bearing mechanics; a **regional aggregation** added because one same-sized neighbor is insufficient; founding size to be set by Gate 1's extinction curve. |

## High findings

| ID | Finding | Consequence | Resolution |
|---|---|---|---|
| **F-05** | **The disease module cannot work as specified.** Critical community size for acute directly-transmitted immunizing infections is 250,000–500,000. December has 18 people. A generic SEIR pathogen will either contribute nothing or, if tuned until epidemics appear, encode a rate that cannot physically exist. | Fabricated epidemiology presented as a validated subsystem — risk R-07 in scientific costume. | [`03`](wiki/03-world-model-and-scenario.md), [`15`](wiki/15-parameter-registry.md) §D. Replaced with a **five-mechanism model** (introduced epidemics, environmental, zoonotic, chronic/latent, helminth). Epidemics required to be **bimodal**. Realism contract gains **R7, scale honesty**. |
| **F-06** | **Small-population noise is indistinguishable from causal emergence.** With expected births and deaths in single digits per decade, many runs end for no interesting reason. No baseline existed. | Collapse narratives would be reported as cascades when they were arithmetic. This is the finding most likely to survive into a published claim and then be demolished. | [`09`](wiki/09-validation-and-experiments.md). **Null demographic model** made a prerequisite; all cascades reported as differences from it. Risk R-29. |
| **F-07** | **No bottom-up cost model** for the top-rated operational risk. The only figure cited rescaled another project's token volume at a **promotional** MiniMax rate for a model now legacy. | The project could not answer whether it is affordable, and would have discovered the answer while running. | [`16`](wiki/16-cost-model-and-model-selection.md). Built from activation counts: **$50–$1,300/month**, cross-checked against Agentopia to within a factor of ~2. |
| **F-08** | **Tier C dominates cost** — ~10% of calls, ~89% of spend. The plan treated significance routing as a quality mechanism, not the primary budget lever. | Optimization effort aimed at the wrong target; population size wrongly perceived as the cost driver. | [`16`](wiki/16-cost-model-and-model-selection.md) §4, [`04`](wiki/04-agents-cognition-and-memory.md). Significance threshold given live tuning, dashboard, and alert. |
| **F-09** | **Sparse activation defeats prompt caching**, and the conflict was unnoticed. Input is >90% of tokens; cache misses cost ~10×; TTLs are 5–30 minutes while activation is deliberately scattered. | An architecture optimized for fewer calls can cost more than one optimized for cache locality — the cost model inverts. | [`16`](wiki/16-cost-model-and-model-selection.md) §4, [`07`](wiki/07-time-emergence-and-observation.md). Cache-aware activation batching; TTL as a model-selection criterion; hit rate as a primary metric; Gate 2 threshold ≥60%. |
| **F-10** | **The affordable models cannot honor the schema contract.** MiniMax's OpenAI-compatible endpoint does not support `response_format` at all; DeepSeek and Qwen are best-effort only. The plan assumed MiniMax could carry routine cognition. | Schema failures concentrated exactly on the tier carrying the volume, discovered deep in Phase 2. | [`16`](wiki/16-cost-model-and-model-selection.md) §5 + [ADR-008](wiki/adr/008-cheap-model-first-with-escalation.md). Validity ladder with escalation to a schema-guaranteed model — the same pattern Agentopia used. |
| **F-11** | **Model refusal was an unhandled failure mode.** Providers may decline to represent raiding, deception, or household formation. | Not merely operational: if a safety layer makes agents reluctant to escalate, December reports "peaceful institutions emerged from material conditions" when the cause was the provider's training. | [`16`](wiki/16-cost-model-and-model-selection.md) §6, [`04`](wiki/04-agents-cognition-and-memory.md), [`08`](wiki/08-models-cost-operations-security.md). Refusal benchmark in admission; distinct failure class; **rates reported with every behavioral claim**. |
| **F-12** | **Per-event full-state hashing is O(state) per event**, making the pipeline quadratic in world size. | At 10⁴–10⁶ entities this becomes the dominant cost of the entire simulation. | [`14`](wiki/14-determinism-replay-and-state-integrity.md) §D6. Incremental lattice hashing (O(changed entities), order-independent), periodic full verification, Merkle at snapshots for divergence localization. |
| **F-13** | **Decision-level idempotency was missing.** Command idempotency keys stop duplicate *delivery*, not a timed-out call whose retry returns a **different** command. | Two valid non-duplicate commands for one decision; history forks silently from the replay. | [`14`](wiki/14-determinism-replay-and-state-integrity.md) §D4, [`06`](wiki/06-architecture-and-data.md). `decision_id` is the idempotency unit, enforced by unique constraint. |
| **F-14** | **Rejection responses leak hidden state.** Returning "feasible alternatives and reasons" can reveal a granary's contents or an unobserved occupancy — a direct violation of realism contract R3. | Partial observability quietly broken through a channel the canary suite did not probe. | [`06`](wiki/06-architecture-and-data.md), [`08`](wiki/08-models-cost-operations-security.md). Visibility filter on all rejection responses; canary probes of the rejection channel added. |
| **F-15** | **Behavioral homogeneity.** Twelve residents on one model with one template converge; the plan varied inputs without guaranteeing varied outputs. | No factions, uniform voice, and any factions that do appear are artifacts of the value draw rather than social process. | [`04`](wiki/04-agents-cognition-and-memory.md). Diversity metrics, per-resident model/prompt variation, homogeneity check in admission. Risk R-31. |
| **F-16** | **The director is an unguarded prompt-injection target** — resident text flows into the summarizer whose output reaches the human. Also unescaped in the UI. | World state stays intact while the observer's understanding is corrupted, with the read-only guarantee technically satisfied throughout. | [`07`](wiki/07-time-emergence-and-observation.md), [`08`](wiki/08-models-cost-operations-security.md), [`09`](wiki/09-validation-and-experiments.md). Delimited untrusted data, citation-enforced factuality checking, UI escaping, dedicated red-team scenario. |

## Medium findings

| ID | Finding | Resolution |
|---|---|---|
| **F-17** | **Bibliography errors.** `GovSimElect` is a five-star personal *fork* cited as an upstream project (real work: `giorgiopiatti/GovSim`, NeurIPS 2024). Craftium/Luanti are **LGPL-2.1+ with CC BY-SA media**, not permissive. Agentopia has **no LICENSE file** despite a README claim of MIT. `project-sid` contains **no code**. MemFail's actual taxonomy is summary/storage/retrieval/reasoning failure, not the list quoted. Melting Pot's substrate counts come from the README, not the abstract. Mindcraft moved owners; Covasim moved to `starsimhub`; Unknown Horizons is dormant since 2019; the OpenRouter docs URL 404s. | [`13`](wiki/13-sources.md) rewritten; every URL re-verified; [`02`](wiki/02-research-landscape.md) candidate matrix corrected. |
| **F-18** | **Mesa facts were stale.** Current stable is 3.5.1; event scheduling is now **stable, not experimental**; `mesa.experimental.devs` is deprecated and removed in 4.0; `mesa.space` is maintenance-only. | [`02`](wiki/02-research-landscape.md), [`13`](wiki/13-sources.md). Prior revised toward Mesa as a toolkit rather than the kernel. |
| **F-19** | **No version control.** The audit template asks for a plan commit, the event envelope records `code_version: git:...`, and pre-registration depends on provable history. | Added to Gate 0. **Do this first.** |
| **F-20** | **Event volume was never estimated** while committing to indefinite retention. Grid resolution is the dominant driver — one event per cell per day at 50 m resolution is millions of events and gigabytes per simulated year from vegetation alone. | [`14`](wiki/14-determinism-replay-and-state-integrity.md) §D8, [`06`](wiki/06-architecture-and-data.md). Batched world events; ≤5,000 events/sim-day target; time partitioning; cold-tier archival. |
| **F-21** | **Gates were unfalsifiable** — "large safety margin," "cost targets pass." | [`10`](wiki/10-roadmap-and-gates.md). Gates 1, 2, 3, and 5 quantified. |
| **F-22** | **Phase 1 estimate was optimistic** at 3–6 weeks for event sourcing, replay, ecology, hydrology, crops, demography, and an experiment harness — before the determinism work this audit added. | [`10`](wiki/10-roadmap-and-gates.md). Revised to 6–12 weeks with the reasoning stated. |
| **F-23** | **Success criteria were unfalsifiable.** "Three distinct governance forms" had no definition of distinctness. | [`00`](wiki/00-vision-and-north-star.md), [`17`](wiki/17-initial-conditions-and-authorship.md). Pre-registered structural definitions required. |
| **F-24** | **Violence rates treated as calibratable.** The empirical literature genuinely disagrees, by an order of magnitude, about warfare mortality in small-scale societies. | [`15`](wiki/15-parameter-registry.md) §E. Represented as a swept parameter across a contested range; strengthened the claims-we-will-not-make list. |
| **F-25** | **Licensing question was open but answerable.** | [`13`](wiki/13-sources.md). Decision table added. **MiroFish's AGPL-3.0 is the one genuine trap**, since its obligations trigger on network use. |
| **F-26** | Python version guidance was behind (3.13+ stated; 3.14 is current, 3.15 due Oct 2026), with no position on free-threading. | [`06`](wiki/06-architecture-and-data.md). Default GIL build required for the kernel. |

## Second research pass — a partial self-correction

The first pass exhausted its budget on epidemiology and left sections A, B, C, E, and F of the parameter registry unverified. A second pass closed them, and it revised one of this audit's own findings.

**F-04 was overstated.** The first draft asserted that eighteen people "cannot persist multigenerationally." The models do say that — but the historical record contains counterexamples the audit had not checked: **Pitcairn persisted from 27 founders, Tristan da Cunha from about 15, and Rapa Nui recovered from a nadir of ~110.** The corrected claim is that an 18-person founding is **marginal rather than impossible**, and the design consequence is unchanged but better grounded: what separates the survivors from Norse Greenland, Roanoke, and the Polynesian Henderson colony is **network connection**, not headcount.

That correction improved the plan rather than weakening the finding. It also surfaced four historical mechanisms now specified in [`15`](wiki/15-parameter-registry.md) §C-4 — founding sex ratio driving lineage-erasing violence (Pitcairn lost every Polynesian male line within a decade), correlated-risk cohort loss (Tristan lost 79% of its adult men in one boat in one day), demographic damage outliving its cause (St Kilda's tetanus ended in the 1920s; the island evacuated in 1930 regardless), and exchange networks carrying marriage partners alongside goods.

Other corrections the second pass forced on the audit's own provisional numbers: walking energy cost is **0.81 kcal/kg/km gross, not 0.5**; storage loss is ~3% for storage proper against a 13% whole-chain figure, not 18%; and forager and horticulturalist fertility are **statistically indistinguishable** (5.6 vs 5.4, p=0.8) rather than differing as the first draft implied. The seed-retention estimate held up almost exactly — 27% verified against 28% estimated, now computed from 26,000 medieval manor-year observations rather than recalled.

## What the audit did not find

Stated explicitly, because a finding list reads as a verdict on quality and this one would mislead:

- **No hidden narrative mutation path.** The director is genuinely read-only, and the separation of prose from state is maintained consistently throughout.
- **No security architecture gaps** beyond F-14 and F-16. [ADR-005](wiki/adr/005-no-arbitrary-agent-code.md) is correct and well-argued.
- **No confusion about authoritative truth.** [ADR-001](wiki/adr/001-causal-kernel-not-llm-world.md) is the single best decision in the plan and it is applied consistently.
- **No ethical blind spots** in the interpretive limits — the anti-goals and the "claims we will not make" list are stronger than most published work in this area.
- **The realism-tier system works.** It is the mechanism that keeps ambition from becoming scope creep, and it should be defended in later phases.

## Open — requires the owner, not the auditor

These block Gate 0 and cannot be resolved by analysis:

1. **Monthly spend cap and emergency cutoff behavior.** [`16`](wiki/16-cost-model-and-model-selection.md) supplies the numbers to decide against; the decision is yours.
2. **Licensing posture** — permissive-only or GPL-compatible. [`13`](wiki/13-sources.md) now states what each choice costs.
3. **Deployment target** — machine, OS, and whether cloud hosting is in scope. This interacts with F-01: a single pinned platform makes the determinism claim much easier to keep.
4. **Canonical pace range**, which drives cost roughly linearly.
5. **Publication intent** — private, or a public history. This changes the AGPL analysis, the privacy posture, and how carefully the "claims we will not make" list must be policed.

## Re-audit checklist

- [x] Every Blocker finding resolved and verified.
- [x] Every High finding resolved and verified.
- [x] Medium findings dispositioned with a target gate.
- [x] Changes introduce no new contradiction in the traceability matrix.
- [x] Known-limit language remains honest — and is now stronger, since the determinism, epidemiology, and violence sections all state what cannot be claimed.
- [ ] **Owner has supplied the five decisions above.**
- [ ] **Version control initialized** (F-19).

## Recommended next actions, in order

1. `git init`, commit the plan as it stands, and tag it. Everything about provenance depends on this and it takes a minute.
2. Answer the five owner decisions.
3. Re-verify the provenance-class **L** parameters in [`15`](wiki/15-parameter-registry.md) §§A, B, C, E, F — this audit exhausted its research budget on the disease section, which is the one that changed the design.
4. Begin Phase 1 with the **integer-versus-float state decision** (ADR-006) as the first task, because it cannot be retrofitted.
5. Build the **null demographic model** before any social mechanism, so every later claim has a baseline.
