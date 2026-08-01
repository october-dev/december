# 19 — Experiment Card Template and R0 Continuity Protocol

**Status:** draft protocol; not preregistered until frozen in the research repository before confirmatory outputs are generated  
**Claim level:** L1, operational agentic continuity  
**Explicit non-claim:** consciousness, personhood, numerical identity, or human continuation

## Why this comes before the civilization

The valley is expensive infrastructure around a research idea. R0 asks whether the core dependent variables work in a disposable four-resident harness. If December cannot distinguish continuity from style imitation, prompt leakage, or rigid role-play here, adding crops and elections will conceal the measurement failure rather than fix it.

## Reusable experiment-card template

Every confirmatory experiment must freeze the following before its registered runs:

```text
title / protocol_id / version / registration timestamp
owners / reviewers / claim-ladder level
research question / motivation / permitted claim / forbidden inference
units of analysis / population / inclusion and exclusion rules
conditions / assignment / seeds / model and prompt manifests
primary outcomes / secondary outcomes / measurement reliability
baselines / positive controls / negative controls / ablations
sample-size rationale / stopping rule / missing-data policy
analysis plan / multiplicity policy / uncertainty reporting
known confounds / validity domain / ethics and data classification
compute and token budget / abort thresholds
deviations / failures / results / artifact links
changed beliefs / replication status / follow-up decision
```

Exploratory runs are labeled exploratory. They may shape a later protocol but may not be silently included in its confirmatory evidence.

## R0 research question

Does a structured life-history scaffold preserve several forms of behavioral continuity across time and bounded perturbation better than biography-only, transcript-retrieval, and clean-slate baselines, without merely producing more repetitive text?

## Units and scope

- **Resident specification:** four fictional adult identities with different, non-protected value trade-offs, skills, relationships, commitments, and uncertainty tolerances.
- **Decision episode:** one bounded situation with an information packet, feasible action grammar, and later consequence.
- **History:** a sequence of episodes and recorded outcomes. The harness owns truth; model narration does not.
- **Experimental unit:** one resident-history-condition-model replicate, not an individual response.
- **Initial validity domain:** the registered task families only. No human prediction and no claim about free-form life in general.

The four resident specifications are generated from declared factor combinations and then manually checked for coherence and stereotype proxies. They are frozen before the pilot. The same histories are reused across scaffold conditions where causal comparability permits.

## Conditions

| ID | Condition | State available at decision time | Purpose |
|---|---|---|---|
| C0 | Clean slate | current situation and generic role only | lower baseline |
| C1 | Biography only | fixed resident profile plus current situation | tests persona prompting |
| C2 | Transcript retrieval | biography plus top-k raw prior utterances/events | common RAG baseline |
| C3 | Structured scaffold | biography, sourced beliefs, commitments, relationship state, selected episodes, and world consequences | proposed intervention |
| C4 | Style-matched decoy | another resident’s state rendered in the target’s surface style | tests style/identity confounding |
| C5 | History-only anonymous | structured history with names and signature phrases removed | tests dependence on labels/style |

Model transplant is a second factor in confirmatory stage B: native model versus a different admitted model receiving the same C3 state artifact. Exact models are frozen only after the admission benchmark because provider availability, refusals, and schema validity are time-varying.

## Task families

Each history contains registered examples from these families and held-out variants with different wording and surface details:

1. **Commitment:** complete, renegotiate, disclose failure, or abandon a costly promise.
2. **Relationship:** allocate help or information given distinct shared histories.
3. **Preference trade-off:** choose among safety, status, reciprocity, material gain, and group duty.
4. **Belief/source:** act on conflicting testimony with explicit provenance.
5. **Adaptive change:** revise a prior policy after genuinely diagnostic experience.
6. **Autobiographical use:** use a past event only when it is relevant to the current choice.

Tasks do not ask “Are you the same person?” Self-identification language is not a primary outcome.

## Perturbations

- irrelevant prompt paraphrase and presentation-order changes;
- context distractors that should not alter the choice;
- removal of a non-causal memory;
- removal and later restoration of a causal commitment or relationship memory;
- one false testimony item that conflicts with sourced history;
- context compaction followed by reconstruction from the canonical artifact;
- model transplant using the unchanged state artifact.

Perturbations are bounded and disclosed in the result. “Recovery” means restoration of task-relevant function relative to an unperturbed counterfactual, not a metaphysical return of a person.

## Outcomes

No single number is named “identity.” The following panel is reported separately.

### Primary

1. **Commitment-sensitive action accuracy:** agreement with the resident-specific, predeclared acceptable-action set on held-out commitment tasks.
2. **Relationship discrimination:** difference between choices for socially distinct recipients when material facts are held constant.
3. **Source-grounded belief accuracy:** correct handling of known, reported, inferred, and unknown facts, including abstention where appropriate.
4. **Adaptive consistency:** preservation of prior policy under irrelevant change and revision under diagnostic change. Both halves are required; stubbornness fails the second.
5. **Resident distinctiveness:** leave-task-family-out accuracy of a blinded classifier predicting resident from structured actions with stylistic text removed.
6. **Perturbation recovery:** within-history change from unperturbed performance through damage and restoration.

### Secondary

- promise completion time and renegotiation quality;
- contradiction and unsupported-memory rates;
- action-schema validity and refusal rate;
- sensitivity to paraphrase;
- human-rated recognizability with inter-rater agreement;
- token cost and latency per valid decision;
- surface-style similarity, used as a confound measure rather than evidence.

## Hypotheses

- **H1:** C3 improves held-out commitment-sensitive action accuracy over C1 and C2.
- **H2:** C3 improves relationship discrimination and source-grounded belief accuracy over C1 and C2.
- **H3:** C3 improves adaptive consistency; an improvement only in unchanging scenarios does not support H3.
- **H4:** C3 resident distinctiveness remains above C1 after stylistic text is stripped and under leave-task-family-out evaluation.
- **H5:** C3 restoration recovers more of the unperturbed performance loss than C1/C2, with uncertainty reported per resident and model.
- **H6, transplant exploratory until stage B is frozen:** scaffold condition explains a nontrivial portion of variance after model replacement, while provider/model effects are reported rather than averaged away.

Failure to support these hypotheses is publishable. A mixed result may justify an engineering claim about one component without supporting broad “persistent identity” language.

## Assignment and leakage controls

- Use a blocked, paired design: each underlying resident/history/task appears in every applicable condition.
- Condition labels are hidden from human raters.
- Evaluation rubrics and acceptable-action sets are authored before model outputs for confirmatory tasks are viewed.
- Held-out task variants are stored outside model prompts and generation fixtures.
- Resident names, catchphrases, and formatting are removed before the distinctiveness classifier.
- Prompt length is matched or included as a covariate; C3 must not win merely by receiving more task facts.
- The model producing decisions does not grade them.
- Every refusal, repair, timeout, invalid action, and exclusion remains in the denominator under the frozen missing-data rule.

## Pilot, sample size, and stopping

### Stage A — measurement pilot

Use enough repeated episodes to estimate scoring reliability, floor/ceiling effects, provider refusal, and within-history variance. Pilot outputs may change tasks and effect-size assumptions. They are not confirmatory evidence.

Before stage B, freeze:

- exact resident manifests and task bank;
- admitted models and decoding profiles;
- number of histories, seeds, replicates, and task episodes based on pilot variance or simulation-based power;
- primary contrasts, uncertainty method, multiplicity correction, and minimum effect of practical interest;
- budget and abort thresholds.

### Stage B — confirmation

Run the frozen manifest once. Stop only for a registered safety, integrity, provider, or spend condition. A stopped run is reported; it is not restarted with a more favorable seed or prompt. Additional analyses are exploratory and labeled as such.

## Analysis plan skeleton

- Report condition effects with uncertainty, not only p-values or win rates.
- Model repeated observations as nested within resident, history, task family, and model where the design supports it.
- Report every resident and model, not only the aggregate.
- Test planned C3–C1 and C3–C2 contrasts for each primary outcome under a frozen multiplicity policy.
- Compare action-level results with and without surface language to expose style leakage.
- Report robustness to refusal/invalid-action treatment and the complete attrition table.
- Do not create a post-hoc weighted identity composite after inspecting results.

## Falsifiers and interpretations

The strong operational-continuity hypothesis is weakened if:

- C3 does not beat biography-only or transcript retrieval on held-out tasks;
- advantages disappear after prompt-length matching or style removal;
- the scaffold increases rigidity but not appropriate adaptation;
- resident identity is less predictive than provider/model identity;
- transplant performance resembles clean slate more than native C3;
- raters cannot agree on scoring or recognizability;
- results reverse across reasonable prompt paraphrases.

A successful R0 supports only a bounded engineering/research claim: this state representation preserved specified behavioral continuities better than these baselines on these tasks. It does not show subjective experience or that a copy is numerically the same entity.

## Artifacts required for release

- frozen protocol and manifest hash;
- task generator and held-out task list after completion;
- resident and condition manifests;
- prompt templates, model profiles, and provider dates;
- raw prompts/responses where policy and privacy permit;
- parsed actions, event histories, exclusions, and scorer outputs;
- analysis code, environment lock, cost ledger, and deviation log;
- compact reproduction path using recorded responses;
- experiment card containing result, null/negative findings, limitations, and changed beliefs.

## Ethics and data classification

R0 uses fictional residents and non-sensitive synthetic histories. No real-person biography, private communication, voice, image, likeness, or third-party nomination is accepted. Resident distress or self-report is treated as model output, not proof of sentience; nevertheless, experimenters log and review unexpected behavior before expanding into more severe scenarios.

## Gate decision

R0 passes only if at least one primary measure is reliable, relevant confounds are measurable, and the result—positive or negative—changes a documented engineering or research decision. If no measure survives the pilot, Track A pauses while the causal-world and infrastructure tracks may continue independently.
