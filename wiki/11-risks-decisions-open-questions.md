# 11 — Risks, Decisions, and Open Questions

## Risk register

| ID | Risk | Likelihood / impact | Early signal | Mitigation | Owner/gate |
|---|---|---|---|---|---|
| R-01 | LLM role-play dominates causal behavior | High / Critical | dialogue volume grows while projects/stocks barely change | typed actions, significance routing, silence/routine policy, behavioral scenarios | Cognition / Gate 2 |
| R-02 | Hidden-state leakage destroys partial observability | Med / Critical | agents mention canary facts or coordinate impossibly | private context builder, source labels, strict services, canary suite | Memory / Gate 2 |
| R-03 | “Random drama” sneaks into director or fixtures | Med / Critical | headline events lack hazard/decision parents | no director writes, causal audit, grep/config review for outcome labels | Kernel / all gates |
| R-04 | Token spend explodes | High / High | input tokens per sim-day trend upward | sparse activation, tiering, summaries, caps, slow/pause policy | Ops / Gate 3 |
| R-05 | Memory compression fabricates identity/history | High / High | source confusion, repeated false beliefs | raw retention, source lineage, contradiction checks, periodic rebuild | Memory / Gate 2 |
| R-06 | World is sterile/boring | Med / High | no cooperation/conflict/institutional change across ensembles | richer dependencies/asymmetry/delays; diagnose ablations; never inject plot | Design / Gate 3–5 |
| R-07 | World is a catastrophe machine | Med / High | frequent early extinction/war across plausible seeds | hazard calibration, external support options, sensitivity region, no drama tuning | World / Gate 5 |
| R-08 | RTS/3D engine captures architecture | Med / High | domain truth duplicated in renderer | adapter contract, headless-first, Gate 6 weighted decision | Architecture / Gate 6 |
| R-09 | Fake precision/historical stereotyping | High / High | unsourced parameters or cultural claims | fictional setting, provenance registry, uncertainty, expert review | Research / all |
| R-10 | Emergence claims are cherry-picked | High / High | only showcase run reported | ensembles, definitions, ablations, branch provenance | Evaluation / all |
| R-11 | Conflict becomes simplistic or entertainment-optimized | Med / High | kill/territory metrics drive tuning | logistics/aftermath, plural goals, no engagement reward, ethical review | Conflict / Gate 5 |
| R-12 | Rules in natural language are ambiguous/exploitable | High / High | office actions depend on prompt interpretation | bounded policy grammar and capabilities; ambiguity remains disputable norm | Society / Gate 4 |
| R-13 | Simulation nondeterminism breaks replay | Med / Critical | hash mismatch under identical manifest | named RNG, deterministic ordering, cached LLM output, nightly replay | Kernel / Gate 1 |
| R-14 | Provider drift changes personalities | High / Med | conformance distributions shift | version profiles, quarantine/retest, model change events | Ops / Gate 2+ |
| R-15 | Retry duplicates irreversible action | Med / Critical | duplicated transfer/vote/work | idempotency keys, expected version, transactional append | Kernel / Gate 1 |
| R-16 | Small population makes demography too volatile | High / Med | most worlds die before institutions matter | aggregate outsiders/migration, parameter sweeps; accept some extinction | World / Gate 1/5 |
| R-17 | Hybrid lightweight people feel morally/design-wise fake | Med / Med | dependants matter only as resources | retain individual state/relationships; relevance promotion; viewpoint audit | Cognition / Gate 3 |
| R-18 | Construction grammar is too restrictive | High / Med | all projects are reskinned recipes | compositional primitives, experimental prototypes, expansion plugin path | Projects / Gate 3 |
| R-19 | Construction grammar admits magic/exploits | High / High | impossible structures/efficiency | material/geometry/prerequisite validation and adversarial blueprint tests | Projects / Gate 3 |
| R-20 | Canonical save is lost or silently changed | Low / Critical | restore/hash failure | append-only events, manifests, replicated backups, restore drills | Ops / Gate 7 |
| R-21 | Scope never ends | High / High | new domain added before prior gate | expansion-pack rule, realism tiers, phase exclusions | Owner / all |
| R-22 | Scientific ABMs are copied outside valid domain | Med / High | COVID/historical parameters used as generic truth | adapt structure, independently source parameters, document validity | Research / Gate 1/5 |
| R-23 | Replay is not actually reproducible | High / Critical | hash mismatch across machines; float divergence; cache miss silently calling a live model | pinned-environment claim, integer-state option at Gate 1, replay hard-fails on cache miss, cross-platform divergence suite | Kernel / Gate 1 ([`14`](14-determinism-replay-and-state-integrity.md)) |
| R-24 | Projections silently miss events committed out of sequence order | Med / Critical | rebuild ≠ live projection; unexplained state drift | one serialized event writer/transaction batch; rebuild equality and sequence-gap tests; add a measured commit-order protocol only before multi-writer operation | Kernel / Gate 1 |
| R-25 | Integrity machinery consumes Phase 1 before a world exists | Med / High | time spent on exotic hashes/fencing exceeds domain modeling | hash-chained events, affected-aggregate versions/hashes, full snapshot hashes; incremental hashing only after profiling | Kernel / Gate 1 |
| R-26 | Retry after timeout produces a *different* command and forks history | Med / Critical | two valid non-duplicate commands for one decision | `decision_id` as the idempotency unit, enforced by unique constraint | Cognition / Gate 2 |
| R-27 | Founding state contains the plot | High / Critical | seeded "disagreements"; outcome labels in fixtures; emergence claims that restate initial conditions | declare generator authorship, vary conditions, audit proxy features/seed selection, use controls and pre-registered definitions | Design / Gate 0–3 ([`17`](17-initial-conditions-and-authorship.md)) |
| R-28 | Disease module encodes a rate that cannot exist at n=18 | High / High | SEIR tuned until epidemics "feel right" | scale-honest mechanisms; validate finite-population outbreak distributions without banning intermediate outcomes | World / Gate 5 ([`15`](15-parameter-registry.md) §D) |
| R-29 | Small-population noise is reported as causal emergence | High / High | collapse narratives with no baseline comparison | mandatory null demographic model; all cascades reported as differences from it | Evaluation / Gate 1+ |
| R-30 | Provider refusal silently biases behavior | High / High | agents never escalate; conflict rate falls after a model swap | refusal benchmark in admission, refusals logged as a distinct class, rates reported with every behavioral claim | Ops / Gate 2 ([`16`](16-cost-model-and-model-selection.md) §6) |
| R-31 | Twelve residents on one model become one person twelve times | High / High | interchangeable decisions; no factions; uniform voice | diversity metrics, per-resident model/prompt variation, homogeneity check in admission | Cognition / Gate 2 |
| R-32 | Sparse activation defeats prompt caching and inverts the cost model | High / High | cache hit rate falls while call count falls | cache-aware activation batching; TTL as a model-selection criterion; hit rate as a primary metric | Ops / Gate 2 ([`16`](16-cost-model-and-model-selection.md) §4) |
| R-33 | Cheap models cannot honor the schema contract | High / High | schema failures concentrated on the affordable tier | validity ladder with escalation to a schema-guaranteed model; per-model failure rates | Cognition / Gate 2 |
| R-34 | Injected text corrupts the director's account to the observer | Med / High | summaries assert motives with no supporting citation | delimited untrusted data, citation-enforced factuality check, UI escaping, dedicated red-team scenario | Observer / Gate 6 |
| R-35 | Rejection reasons leak hidden state | Med / Critical | agents act on quantities or locations they never observed | visibility filter on all rejection responses; canary probes of the rejection channel | Kernel / Gate 2 |
| R-36 | Canonical history outgrows its storage and backup plan | Med / Med | log growth tracks grid resolution; restore drills slow | batched world events, ≤5,000 events/sim-day target, time partitioning, cold-tier archival | Ops / Gate 1 |
| R-37 | The experiment programme, not the world, blows the budget | High / High | ensemble spend exceeds canonical spend by an order of magnitude | separate hard cap and approval; cheapest tier plus batch pricing | Ops / Gate 3 |
| R-38 | Operational identity is laundered into consciousness or human-survival claims | High / Critical | marketing copy treats consistency as personhood; conclusions jump claim levels | claims ladder, claim review, explicit forbidden inferences, ADR-009 | Research / Gate 0+ |
| R-39 | Human-subject or third-party data is collected without adequate governance | Med / Critical | public nomination form; life histories in GitHub issues; unverifiable consent | fictional-only boundary; disable solicitation; separate first-party private reviewed protocol | Ethics / Gate 0 |
| R-40 | The canonical world becomes anecdotal evidence | High / High | one dramatic run dominates papers or tuning | canonical = exhibit/soak; hypotheses tested on new registered cohorts | Evaluation / all |
| R-41 | “AI lab” becomes branding without research practice | Med / High | no registered questions, negative results, replications, or versioned experiment cards | lab operating system in [`18`](18-lab-charter-and-research-program.md); annual evidence review; kill/pivot criteria | Owner / Gate 0+ |
| R-42 | Resident diversity encodes stereotypes or spectacle-seeking personalities | Med / High | protected proxies predict violence/labor; “interesting” seeds selected | heterogeneous motives without engagement reward; proxy audits; disclose distributions and rejected seeds | Design / Gate 2–5 |

## Decisions made

| Decision | Status | Rationale |
|---|---|---|
| Build a terrarium containing agents, not an agent chat society | Accepted | Makes habitat, causality, and observation first-class |
| Fictional early agrarian valley | Accepted for audit | High social richness with bounded technology; avoids false exact history |
| New headless causal kernel | Accepted for audit | No candidate supplies the required material + institutional truth |
| Mesa behind replaceable runtime interface | Proposed | Best current Python ABM scaffold; benchmark before lock-in |
| Event sourcing + snapshots | Accepted | Replay, audit, forks, recovery, causal evidence |
| 12 full adults + 6 lightweight dependants + aggregate neighbor | Proposed | Balances social richness, demography, and token cost |
| LLM chooses; kernel validates/resolves | Accepted | Preserves autonomy without magical state mutation |
| No arbitrary agent code execution | Accepted | Not needed for creative building; severe integrity/security risk |
| Constitution/policy compiles to bounded grammar | Accepted | Makes office powers auditable while retaining natural-language norms |
| 2D first, 3D at Gate 6 | Accepted | Prevents visual engine from dictating truth |
| Extinction preserved, not auto-reset | Accepted | History must have stakes and integrity |
| Observer/director read-only | Accepted | No hidden plot manipulation |
| Pinned-environment determinism, not portable bit-identity | Accepted (audit) | Portable float determinism is unavailable in Python; integer-state option decided at Gate 1 (ADR-006) |
| Model-response cache is canonical; replay hard-fails on a miss | Accepted (audit) | No provider offers reproducible sampling, so the cache *is* the record |
| Founding state is declared, randomized, and varied—not unauthored | Accepted (audit pass 2) | A generator is authored through its distributions, constraints, correlations, exclusions, and seed-selection policy (ADR-007) |
| Five-mechanism health model replaces generic SEIR | Accepted (audit) | Acute immunizing infections cannot be endemic at n=18 |
| Aggregate neighbor moves to Phase 3 | Accepted (audit) | 18 founders are not viable in isolation; institutional experiments must not run in a dying world |
| Null demographic model is a prerequisite for causal claims | Accepted (audit) | Small-population noise otherwise masquerades as emergence |
| Cheap-model-first with escalation ladder | Proposed | Cost model puts Tier C at ~89% of spend; cheap models lack strict schema decoding (ADR-008) |
| Operational identity before consciousness claims | Accepted (audit pass 2) | December can test behavioral continuity and perturbation recovery; it cannot currently test numerical identity or consciousness (ADR-009) |
| Canonical world is an exhibit/soak, not the research sample | Accepted (audit pass 2) | Findings require preregistered cohorts, baselines, and ablations |
| Fictional residents only until a separate human-subject protocol exists | Accepted (audit pass 2) | Public or third-party life-history intake lacks defensible consent and governance |

## Open questions that do not block writing code until their gate

### Product and pace

1. ~~What monthly and daily spend cap is acceptable after existing token balances?~~ **Partly answered:** the balances are **$2,000 MiniMax + $1,000 OpenRouter**, worth roughly **8,000 simulated days** in the recommended configuration ([`16`](16-cost-model-and-model-selection.md) §7a). What remains open is the *allocation*: those credits fund either a canonical world to one generational transition **or** the ensemble programme, not both, and no marginal cash cap has been set for when they are exhausted.
2. Should the canonical pace target weeks, seasons, or generations over a real month?
3. Is the observer allowed to pause/resume freely, or should that be an administrative event?
4. Will any history be public, and should developer-private rationales be exposed?

### Scenario and anthropology

5. Exact map scale, latitude/seasonal regime, crops, and subsistence mix?
6. What minimal reproductive/kinship model is acceptable and respectful?
7. Should elders/children ever be full cognition automatically, or only by relevance/budget?
8. How are names, language style, ritual, and material culture generated without becoming a culture stereotype?
9. What routes keep a 12-person population viable—migration, neighboring band, staged founders?

### Mechanics

10. Continuous spatial model, cells, or regions-with-routes?
11. How detailed must nutrition be: energy only, macro proxies, or deficiency states?
12. Which two crops and which generic pathogens best exercise mechanics without false specificity?
13. Does death resolution need only functional injury classes or anatomical detail?
14. When should an aggregate outsider become a named resident, and how are aggregate histories instantiated consistently?
15. How much rule ambiguity is interpreted socially versus blocked by the compiler?

### Technology

16. Mesa versus custom scheduler after Phase 1 benchmark? *(The audit's prior: Mesa as a spatial/data-collection toolkit, not the kernel — its event scheduling churned in 3.5/4.0 and `mesa.space` is maintenance-only.)*
17. PostgreSQL-only job queue initially, or Redis from start?
18. Local embeddings versus provider embeddings for private memory?
19. Which models pass each tier at implementation time? *(Now constrained by three criteria the audit added: strict-schema support, prompt-cache TTL, and measured refusal rate.)*
20. Which visual adapter wins Gate 6: custom 2D, Luanti/Craftium, or another substrate? *(Now also a licensing decision — Craftium and Luanti are LGPL-2.1+ with CC BY-SA media.)*

### Questions the audit answered

These are no longer open. Recorded here so the reasoning is not relitigated.

| Question | Answer | Where |
|---|---|---|
| What does "bit-for-bit replay" actually mean? | Pinned-environment determinism; portable bit-identity only if canonical state is integer-valued | [`14`](14-determinism-replay-and-state-integrity.md) §D1 |
| Permissive-only reuse, or GPL-compatible? | Decidable from evidence — a permissive posture excludes Craftium/Luanti, AgModel, ForeFire, and the RTS engines; **MiroFish's AGPL is the one real trap** | [`13`](13-sources.md) |
| Which generic pathogens best exercise mechanics? *(was Q12)* | Wrong question at this scale. No acute immunizing pathogen can be endemic; use the five-mechanism model | [`15`](15-parameter-registry.md) §D |
| What routes keep a 12-person population viable? *(was Q9)* | In-migration and exogamy, required from Phase 3 — not optional flavor | [`15`](15-parameter-registry.md) §C-1 |
| What does a month of operation cost? | Roughly $50–$1,300 depending on Tier C model and pace; experiments likely cost more than the world | [`16`](16-cost-model-and-model-selection.md) |

### Evaluation

21. Who can provide domain review for demography/anthropology, epidemic mechanics, and conflict?
22. What numerical distribution of extinction/conflict is considered non-pathological without tuning for spectacle?
23. Which observer panel can rate behavioral plausibility, and how will disagreement be handled?
24. What exact seven-day soak success thresholds apply to cost, fallbacks, and anomaly count?
25. Which operational-identity metric survives a small R0 reliability and confound test?
26. What legal entity, governance model, and external review arrangement would make “lab” accountable rather than merely a brand?
27. Which project keeps the December name: the living terrarium or the existing “December Sato” autonomous-computer experiment?

## Questions that must be resolved before Phase 1

- Owner-approved maximum monthly spend and emergency cutoff behavior **beyond the existing $3,000 in credits**, plus the canonical-versus-ensemble allocation of those credits ([`16`](16-cost-model-and-model-selection.md) §7a).
- Licensing policy (permissive-only code reuse versus GPL-compatible project).
- Whether canonical history is private/local or intended for public streaming.
- Initial simulated-time pace range.
- Choice of target deployment machine/OS and whether cloud hosting is in scope.
- Public landing page participant solicitation removed or disabled; no third-party nominations.
- Claims ladder and first experiment card approved.
- Distinct public naming and security boundaries established for December versus December Sato.

## Questions that must be resolved before canonical launch

- Final parameter provenance and known-invalidity statement.
- Expert/domain review disposition.
- Reproduction/kinship and violence content policy.
- Observer intervention/publication policy.
- Model-provider data handling and retention policy.
- Backup location, retention, and recovery owner.
- What happens after whole-world extinction: ruins continue, canonical ends, or a new separately identified world begins.
