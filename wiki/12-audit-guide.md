# 12 — Independent Audit Guide

## Purpose

This guide is for the second agent or human reviewer. The audit should be adversarial and evidence-based. It is not a copyedit or a vote on whether the premise sounds fun.

## Required audit output

Create `AUDIT-REPORT.md` beside the project README containing:

1. verdict: `BLOCK`, `REVISE`, or `READY FOR PHASE 1`;
2. executive summary;
3. findings table with ID, severity, affected files, evidence, consequence, and required remediation;
4. unresolved questions and assumptions;
5. traceability gaps;
6. security/threat-model findings;
7. cost/operational findings;
8. realism/validation findings;
9. prioritized changes;
10. re-audit checklist.

Severity:

- **Blocker:** core promise cannot be achieved, canonical integrity/security is unsound, or a crucial decision is absent.
- **High:** likely to cause false emergence, state corruption, runaway cost, or unusable operation.
- **Medium:** meaningful quality/maintainability/validity weakness.
- **Low:** clarity, optimization, or future concern.

## Audit questions

### Causal integrity

- Can any narrative/model component mutate truth without a typed command?
- Does every random event have eligibility, distribution, named stream, and evidence?
- Are stock/flow, time, location, death, authority, and information invariants complete?
- Could a headline event be produced by labeling rather than mechanisms?
- Can compound outcomes be traced across modules without post-hoc model invention?

### Agent autonomy

- Are residents actually choosing consequential actions, or are kernel policies choosing everything?
- Conversely, can language outputs bypass physical or institutional constraints?
- Is refusal, revision, interruption, deception, learning, and failure represented?
- Does model tiering preserve identity and decision quality?
- Are lightweight people treated consistently and promotable?

### Emergence

- Are elections, factions, war, construction, and extinction defined operationally?
- Are mechanisms rich enough for multiple outcomes, not only the expected demo?
- Does the design accidentally reward drama?
- Are ensembles and ablations sufficient to distinguish emergence from randomness/prompt bias?
- Is the canonical world treated as an exhibit/soak rather than a statistical sample?
- Were hypotheses inspired by the canonical world tested on new, registered cohorts?

### Research claims and identity

- Which claim-ladder level does each public statement occupy, and does the evidence reach that level?
- Is behavioral continuity distinguished from consciousness, personhood, numerical identity, and human survival?
- Can identity metrics distinguish continuity from style imitation, stubbornness, self-report, or prompt leakage?
- Are clean-slate, prompt-only, history-only, model-transplant, and perturbation controls present where relevant?
- Are negative results, exclusions, model versions, refusal rates, and task-family generalization reported?
- Is “AI lab” supported by registered questions, reproducible artifacts, external criticism, and kill/pivot criteria?

### Realism and validity

- Does each realism claim map to evidence and a tier?
- Are historical/scientific sources used within their domain?
- Are parameter provenance, uncertainty, sensitivity, and known limitations planned?
- Is the fictional setting protected from implicit cultural stereotypes?
- Are the initial population and boundary-world assumptions coherent?

### Construction and institutions

- Can novel projects be more than reskinned recipes while remaining physically bounded?
- Can ambiguous norms exist without bypassing executable authority?
- Do elections cover eligibility, information, ballots, counts, disputes, succession, and legitimacy?
- Can institutions fail, split, be ignored, or dissolve?
- Can an office or generated rule escalate its own infrastructure permissions?

### Conflict and hazards

- Is war local, logistical, costly, and consequential?
- Can peaceful outcomes occur for structural reasons?
- Are disease/fire/outside groups grounded and testable?
- Are extinction and settlement abandonment distinguished?
- Does the design avoid sensationalizing violence?

### Architecture and operations

- Is the event store genuinely authoritative and replayable?
- Are module boundaries and transactional invariants sufficient?
- Can provider timeouts, retries, budget exhaustion, migrations, and crashes corrupt history?
- Is a seven-day unattended run realistically operable?
- Can renderer/UI/director accidentally become a second truth source?

### Security

- Can resident text inject prompts or action definitions?
- Can generated actions reach network, shell, filesystem, secrets, or arbitrary code?
- Are authorization, idempotency, expected version, and bounds enforced server-side?
- Are private memories/rationales separated and redacted?
- Is public sharing/data retention addressed?

### Human data and research ethics

- Does any page, form, issue template, API, or dataset solicit identifiable life histories or third-party nominations?
- If human-participant research exists, is intake first-party and private, with informed consent, review, minimization, withdrawal/deletion, retention, access control, and incident handling?
- Are vulnerable participants, relatives, bystanders, impersonation, grief, and posthumous-data risks explicitly addressed?
- Does the project forbid telling a participant or family that an emulation is the person or that continuity has been established?

## Traceability matrix

The auditor should verify and extend this matrix.

| Promise | State | Mechanism | Evidence/UI | Test/gate |
|---|---|---|---|---|
| Gather resources | spatial stocks, lots, body, tools | extraction/regrowth/activity | map, lot ledger, causal event | conservation + depletion / Gate 1 |
| Build own things | blueprint, materials, task DAG, skill, structure | propose→compile→authorize→work→test | project page/replay | adversarial blueprints / Gate 3 |
| Hold elections | charter, roll, ballots, office capabilities | staged election lifecycle | institution/election page | tie/fraud/succession / Gate 4 |
| Create government | rules, institutions, roles, legitimacy | group and policy grammar | charter lineage | multiple forms/ablation / Gate 4 |
| Form factions | memberships, goals, identity, coordination | invitations, meetings, collective actions | social/group graph | persistence/fission scenarios / Gate 4 |
| Trade/share/steal | lots, custody, claims, obligations | transfers and detection | ledger/person timeline | conservation/private info / Gate 3 |
| Learn/invent | skills, techniques, teaching/prototypes | practice, teaching, recombination/test | knowledge lineage | prerequisite/novelty tests / Gate 3+ |
| Disease | body/pathogen/contact state | introduction/transmission/progression/care | health/contact traces | route/fade-out tests / Gate 5 |
| Fire/disaster | fuel, weather, structures, hazard state | ignition/spread/damage | map/causal replay | zero-fuel/wind scenarios / Gate 5 |
| War | grievances, groups, supplies, participants, encounters | escalation/mobilization/logistics/combat/aftermath | conflict timeline/why | peace/war sensitivity / Gate 5 |
| Migration/fission | membership, route, supplies, destination | departure and boundary resolution | map/group history | no-teleport/conservation / Gate 5 |
| Extinction | living people/membership/settlement occupancy | mortality/migration + terminal classifier | preserved final report | classification/replay / Gate 5/7 |
| Return after 2 days | event log, projections, significance | read-only director | Since-you-left dashboard | factuality + soak / Gate 6/7 |
| Explain why | causal parents, observations, RNG, commands | provenance graph | Why page | causal completeness sampling / all |
| Run within tokens | activations, model profiles, usage/caps | tiering/routing/degradation, cache-aware batching | cost dashboard, cache hit rate | budget chaos tests / Gate 2/3/7 |
| Reproduce a history | event log, manifest, response cache, state digests | pinned-environment replay, decision barrier | replay status, divergence report | determinism suite / Gate 1–2 |
| Survive as a population | vital rates, migration, exogamy, kin graph | demography plus boundary-world exchange | population page, lineage view | null-model comparison / Gate 1/3 |
| Claim something emerged | pre-registered definitions, founding manifest | declared/randomized initial-condition cohorts, ablations | emergence audit report | proxy audit, seed-selection disclosure, no-charter control / Gate 3–5 |
| Behave like distinct people | values, biography, per-resident routing | diversity metrics, prompt/model variation | person pages, divergence stats | homogeneity check / Gate 2 |
| Preserve operational identity | commitments, memories, relationships, policies, model/history manifest | perturbation/recovery and transplant protocol | blinded scores and failure traces | R0 reliability/confound gate + Gate 2 |
| Make a research claim | registered hypothesis, conditions, seeds, exclusions, metrics | controlled cohort + baselines/ablations | experiment card, raw outputs, analysis | independent reproduction / each claim |
| Protect human subjects | consent record, minimized private data, retention/withdrawal state | separate reviewed intake and access workflow | private participant portal/audit log | ethics and security review / before collection |

## Specific red flags

The auditor should issue at least a High finding if any of these appear:

- “the LLM decides what happens” without kernel transition rules;
- “random event” without a conditional hazard definition;
- global memory or full-state prompts for residents;
- event replay dependent on calling a live model again;
- currency, elections, police, war, or religion installed as assumptions despite emergence claims;
- observer/editor intervention hidden from canonical lineage;
- outcome-tuned “interestingness” feeding back into the world;
- arbitrary code/shell/browser tools given to residents;
- numerical historical claims without provenance/confidence;
- irreversible actions without idempotency/version checks;
- a 3D engine treated as canonical physics before Gate 6;
- an unqualified "bit-for-bit deterministic" claim over floating-point state;
- replay that would call a live model on a cache miss instead of failing;
- a mechanism borrowed from a population thousands of times larger, without a validity-at-n=18 argument;
- a collapse or cascade reported without comparison to a null demographic model;
- a founding fixture that names a future tension, or an operational definition written after the runs;
- a behavioral finding reported without the model's refusal rate;
- a repository cited as upstream that turns out to be a fork, or a license claimed from a README rather than a LICENSE file.

## Sign-off protocol

1. Reviewer writes the report without editing the plan.
2. Plan author responds in `AUDIT-RESPONSE.md`, accepting, disputing with evidence, or deferring each finding.
3. Accepted fixes update the wiki and decision log.
4. Reviewer rechecks Blocker/High findings and updates verdict.
5. Owner explicitly approves Gate 0 and the Phase 1 spend/deployment constraints.

“Both agents are satisfied” means no open Blocker/High finding. Medium/Low findings may remain only with owner-visible disposition and a target gate.
