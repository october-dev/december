# December Plan — Independent Audit Findings, Pass 2

**Reviewer:** Codex  
**Date:** 2026-08-01  
**Scope:** first audit’s changes, revised wiki, cost/parameter/determinism additions, and public lab/identity framing  
**Verdict:** `REVISE` — the engineering premise remains strong; Gate 0 is not closed

## Executive verdict

December has real depth. Its strongest near-term research contribution is not a simulated civilization by itself and not a claim about immortality. It is a causal, longitudinal testbed for persistent synthetic agency: complete life histories, private information, model-independent identity state, counterfactual forks, and rigorous evaluation under change.

The previous audit made several excellent corrections—especially scale honesty, decision-level idempotency, refusal measurement, initial-condition provenance, null demographic controls, and director prompt-injection defenses. It also introduced new overclaims and overengineering. Most importantly, the new public identity framing outruns the protocol: the valley cannot establish consciousness or human survival through substrate change.

This pass adds a lab charter and claims ladder, corrects the resident-objective policy, separates three meanings of replay, demotes the parameter registry from “verified truth” to provisional evidence, corrects current pricing interpretation, and places a hard boundary around human-participant work.

## Blockers

| ID | Finding | Consequence | Resolution/status |
|---|---|---|---|
| P2-F01 | The landing page said the experiment made personal continuity testable and solicited human participants, while the wiki listed conscious-being research as an anti-goal and contained no identity protocol. | Brand promise and evidence were misaligned; risk of misleading users and collecting personal information without adequate governance. | **Resolved 2026-08-01:** claims ladder and Track D boundary added in [`18`](wiki/18-lab-charter-and-research-program.md); both rendered implementations now lead with the living-world dream and keep consciousness/human continuation as an explicitly unproven horizon. |
| P2-F02 | “Request a human participant” permitted nomination of another person and opened a public GitHub issue containing a name/alias and reason their life should be studied. | Consent could not be verified; public personal data, family/third-party disclosure, reputational and emotional risks. | **Resolved for the current scope 2026-08-01:** participant UI, form, and client-side issue generation removed from both implementations. December accepts fictional residents only; future human work remains blocked behind the separate protocol in [`18`](wiki/18-lab-charter-and-research-program.md). |
| P2-F03 | The first audit repaired and verified its own findings in one pass, contrary to the project’s audit protocol, then declared readiness. | “Independent audit complete” overstates assurance. | README now records two passes and Gate 0 remains open. This report is the independent re-audit artifact. |
| P2-F04 | The identity/continuity thesis had no registered dependent variables or baseline. | Any coherent persona could be called “identity”; the flagship lab claim was unfalsifiable. | Track A and the first three experiments in [`18`](wiki/18-lab-charter-and-research-program.md); metrics added to validation plan; a preregistration-ready R0 protocol and template added in [`19`](wiki/19-experiment-card-template-and-r0-protocol.md). It remains a draft until frozen in version control before confirmatory runs. |

## High findings

| ID | Finding | Consequence | Resolution/status |
|---|---|---|---|
| P2-F05 | Replay, deterministic re-execution, and fresh counterfactual simulation were conflated. | Floating-point caveats were applied to event replay unnecessarily, while live branch semantics remained unclear. | [`14`](wiki/14-determinism-replay-and-state-integrity.md) and ADR-006 now define three guarantees. |
| P2-F06 | The decision barrier requires timeouts in simulated time while the simulation can be blocked waiting for the decision. | Potential deadlock; provider availability silently affects whether agency exists. | Live wall-clock/retry policy may choose the recorded outcome; replay consumes that recorded resolution. High-significance missing decisions pause rather than become a universal “survival” choice. |
| P2-F07 | Per-event global lattice hashing, `xid8` fencing, custom inverse-CDF distributions, and a project-owned transcendental library were placed into Phase 1 before measurements. | The integrity layer risks consuming the project before a resident exists; some mechanisms solve scale December does not have. | Normative minimum reduced to one serialized writer, hash-chained events, aggregate versions/hashes, canonical snapshot hashes, named RNG streams, and replay tests. Advanced mechanisms are escalation options. |
| P2-F08 | “Generated, not authored” treats a seeded generator as neutral. | Authorship is hidden in distributions, constraints, exclusions, and seed selection; emergence claims can still be planted without outcome words. | Reframed as declared, randomized, and varied initial conditions; canonical exhibition separated from research cohorts. |
| P2-F09 | The parameter registry labels rows “verified” without a source ID/locator per row and converts heterogeneous evidence into implementation prescriptions. | Another reviewer cannot reproduce provenance; ecological fallacy and false precision can enter code. | Registry is now explicitly provisional; source-ID/locator and transfer-justification columns are required before admission to code. Harmful prescriptive prose corrected. |
| P2-F10 | Resident objectives still said “plural goals and survival,” and a universal survival fallback was used during outages. | Suppresses martyrdom, dominance, revenge, risk-seeking, self-destruction, and other human-like variation; creates artificial peace/survival bias. | Society, cognition, and operations docs now distinguish no *system-wide engagement reward* from heterogeneous resident motives. High-stakes cognition pauses on failure. |
| P2-F11 | The cost table assigns GPT-5.6 Luna the old GPT-5-nano price and calls MiniMax M3’s published permanent reduction temporary. | Cost comparisons and model-routing recommendations are factually wrong. | Corrected against official 2026-08-01 provider pages. Model choice remains benchmark-driven. |
| P2-F12 | A public canonical world, research cohort, and hypothesis test were treated as one artifact. | Tuning the exhibit contaminates research; a single beautiful history may be presented as a result. | [`18`](wiki/18-lab-charter-and-research-program.md) separates the canonical exhibit from registered cohorts and controls. |

## Medium findings

| ID | Finding | Resolution/status |
|---|---|---|
| P2-F13 | The fixed founding population of 18 conflicts with the audit’s own statement that Gate 1 should determine size. | Public page should call 18 the current design cohort, not a scientifically established optimum. |
| P2-F14 | Acute epidemic “bimodality” was stated as a strict invariant using large-population approximations at n=18. | Reworded as an ensemble expectation; intermediate outbreaks are possible and not automatically bugs. |
| P2-F15 | Conflict “frequency” was proposed as an input sweep. | Sweep mechanisms/dispositions/conditions; use observed conflict rates only as outputs and broad plausibility checks. |
| P2-F16 | Historical examples and population-genetic detail exceed the needs of the first terrarium and may create false authority. | Keep as research notes; genetics deferred beyond initial demography unless it becomes an explicit question. |
| P2-F17 | The licensing table calls LGPL/GPL components “not usable,” which is too categorical and resembles legal advice. | Recast as integration obligations requiring deliberate review; source reading is distinct from code reuse. |
| P2-F18 | December was presented publicly like a mature scientific program before a research operating system, registered experiment, versioned corpus, or result existed. | **Public-framing portion resolved 2026-08-01:** Wega Labs remains correctly identified as the company and AI lab, while December now leads as one of its long-term dreams and clearly says the world is not alive yet. [`18`](wiki/18-lab-charter-and-research-program.md) still defines how the project earns stronger research claims over time. |
| P2-F19 | Two unrelated projects use the December name: the living-world/identity program and “December Sato,” an autonomous Mac mini agent with broad privileges and Twitter access. | Brand confusion and a security posture incompatible with the terrarium’s containment story. Rename or clearly separate December Sato; do not describe unrestricted computer ownership as a lab method. |
| P2-F20 | The top-level research documents are not version-controlled even though two nested website directories are separate Git repositories. | Gate 0 still requires a repository containing the wiki, ADRs, audits, and experiment registrations. Owner action remains open. |

## What is genuinely strong

- The authoritative causal kernel is the correct foundation.
- Objective events and subjective memory are cleanly separated.
- Capability-based institutions avoid giving prose magical authority.
- Event provenance, private information lineage, and counterfactual branches can become distinctive research infrastructure.
- Scale honesty and null baselines are excellent additions.
- Provider refusal, homogeneity, schema failure, and model drift are correctly treated as experimental confounds.
- The project is unusually explicit about claims it must not make.

## Documentation changes made in this pass

- Added [`18`](wiki/18-lab-charter-and-research-program.md), ADR-009, and [`19`](wiki/19-experiment-card-template-and-r0-protocol.md): lab thesis, claims ladder, research tracks, human-data boundary, experiment-card template, and the R0 protocol.
- Updated the README, vision, validation, roadmap, risks, audit guide/template, and landing-page brief so operational identity, canonical exhibit, and registered research cohorts are distinct concepts.
- Corrected cognition and conflict policy so the system has no observer-engagement reward while individual residents may still value dominance, territory, revenge, glory, risk, altruism, or self-sacrifice.
- Split recorded-event replay, pinned kernel re-execution, and fresh counterfactual branching; replaced Phase 1’s advanced hashing/fencing mandate with a serialized writer and proportional integrity checks.
- Recast initial conditions as authored but declared/randomized/varied, with proxy-feature and seed-selection audits.
- Demoted the parameter registry to a provisional research notebook and corrected prescriptive or scale-inappropriate claims, including strict epidemic bimodality and conflict-rate tuning.
- Corrected current model-price interpretation and clarified that schema transport validity is not semantic/action validity.
- Recast reciprocal-license components as review decisions rather than categorically unusable software.
- Initially marked the participant intake as a release blocker, then removed it from both rendered implementations in the follow-up landing-page copy pass. Calls to action now invite questions and project ideas, not human-life data.
- Marked the first audit historical so its superseded remedies cannot be mistaken for the current specification.

## Gate 0 status

Gate 0 remains open until:

1. the five owner decisions in the first audit are supplied;
2. the research corpus is under version control;
3. ADR-009 and the claims ladder are accepted or revised;
4. ~~public participant solicitation is disabled or replaced~~ — resolved 2026-08-01;
5. a first registered continuity experiment and experiment-card template exist;
6. parameter rows used by Phase 1 have reproducible source locators and transfer justifications;
7. the Phase 1 integrity minimum is accepted, with advanced machinery deferred until measurement requires it.

## Final assessment

Proceed—but proceed as a lab that happens to have a beautiful long-horizon vision, not as a vision looking for scientific language. If the first year produces a credible continuity benchmark, a replayable causal-agent testbed, and two careful negative or positive studies, Wega Labs will have earned the label. If it produces only a striking website and one cinematic valley history, it will not.
