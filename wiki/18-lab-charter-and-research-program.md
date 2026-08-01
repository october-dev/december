# 18 — Wega Labs Charter and the December Research Program

**Status:** proposed by independent audit pass 2  
**Purpose:** separate the serious research program from the distant aspiration

## The candid thesis

December can support a real AI lab. It cannot honestly begin as an immortality experiment.

The tractable research object is **persistent synthetic agency**: whether an artificial resident can remain behaviorally and historically identifiable across long periods, memory loss and consolidation, model changes, bodily change, social change, and counterfactual forks. The terrarium is valuable because identity is tested through consequential action in a shared causal world rather than through self-description in chat.

That question has scientific and engineering depth even if artificial consciousness never appears and human uploading proves impossible. It can produce:

- benchmarks for longitudinal agent identity and model-swap continuity;
- methods for separating persona performance from persistent agency;
- an event-sourced causal testbed for generative social simulation;
- measurements of memory, relationship, embodiment, and provider effects;
- open datasets of complete synthetic life histories;
- infrastructure useful for games, agent evaluation, training environments, and simulation research.

The distant question—whether a human life could continue beyond biology—may motivate the lab. December does not currently contain a method capable of answering it.

## Four questions that must remain separate

| Question | December can test now? | Evidence available |
|---|---|---|
| Does a synthetic resident remain operationally identifiable over time? | Yes | behavior, commitments, beliefs, relationships, recovery after perturbation |
| Which scaffold components causally support that continuity? | Yes | randomized ablations and counterfactual branches |
| Can a model predict or emulate a particular human across contexts? | Later, with consent and a human-subject protocol | held-out behavioral predictions and participant judgments |
| Is the resident conscious, numerically identical to a human, or a continuation of that human? | No | December supplies no decisive consciousness or numerical-identity test |

Personal identity is not one settled scientific variable. Psychological continuity, bodily continuity, narrative identity, social recognition, and numerical identity can come apart—especially under copying or branching. A system that behaves like someone may be a useful model of them without being them. A system that says it is conscious is not thereby conscious.

## Claims ladder

Public and research claims must climb this ladder one level at a time.

### L0 — Infrastructure integrity

The world conserves state, enforces information boundaries, records provenance, survives failures, and replays recorded history.

**Required before:** any behavioral or emergence claim.

### L1 — Agentic continuity

A resident remains distinguishable from other residents and internally coherent across time, compaction, restarts, and bounded perturbations.

**Possible claim:** “This scaffold preserved the resident’s commitments and behavior better than the baseline over 90 simulated days.”

**Forbidden inference:** “The resident remained the same conscious person.”

### L2 — Causal components of continuity

Randomized experiments identify whether episodic memory, relationship state, embodiment, commitments, social recognition, or model weights contribute to measured continuity.

**Possible claim:** “Removing relationship history reduced held-out choice consistency after controlling for biography and model.”

### L3 — Human-model fidelity

With ethics review, explicit first-party consent, and held-out evaluation, a research persona predicts some choices or judgments of a participant better than baselines.

**Possible claim:** “The model predicted this participant’s answers on this registered task family at this measured accuracy.”

**Forbidden inference:** “The model contains or continues the participant.”

### L4 — Consciousness or substrate survival

Whether a system has subjective experience or whether numerical personal identity survives copying/substrate change.

**Current status:** outside December’s evidential reach. Work here is philosophical and consciousness-science collaboration, not a result of running the valley longer.

## Flagship research tracks

### Track A — Persistent agent identity

Primary question: which state and architectural relationships make a long-running agent identifiable and resilient without freezing it into a caricature?

Initial registered experiments:

1. **Memory architecture:** raw retrieval versus consolidated beliefs versus structured commitments.
2. **Social grounding:** isolated biography versus biography plus relationship history and others’ expectations.
3. **Embodiment:** text-only resident versus resident whose choices have persistent bodily/material consequences.
4. **Model transplant:** same structured identity state across different approved models, measured against within-model variance.
5. **Perturbation recovery:** temporary memory loss, false testimony, conflicting commitments, and restoration from cold history.
6. **Fission:** clone one state into two branches and measure divergence. This tests the limits of “same person” language rather than assuming a unique answer.

Primary measures must include held-out action prediction, commitment completion, preference/relationship consistency, source accuracy, distinctiveness from other residents, appropriate change after experience, and robustness across prompts/models. Self-reported identity is secondary evidence.

### Track B — Causal generative social simulation

Primary question: when do language-model decisions embedded in a material world produce macro patterns not reducible to prompt labels, initial-condition selection, or provider policy?

Outputs:

- the causal kernel and world protocol;
- emergence definitions and confound tests;
- provider/refusal/homogeneity measurements;
- comparisons among scripted, LLM, and hybrid residents;
- full provenance for positive and negative results.

### Track C — Longitudinal agent evaluation infrastructure

Primary question: how should persistent agents be evaluated when their state, environment, relationships, and model providers change?

Outputs:

- identity-continuity benchmark tasks;
- replay/branch/evidence tooling;
- model admission and drift suites;
- portable “life history” artifact format;
- reproducible experiment cards and datasets.

This track is the most credible near-term wedge for collaboration and product value.

### Track D — Human continuity (future, separately governed)

No human persona collection begins under the current protocol. Before L3 work, Wega Labs needs:

- a named research question and data-minimization argument;
- independent ethics review appropriate to jurisdiction and publication intent;
- first-party informed consent with withdrawal/deletion procedures;
- private intake—not public GitHub issues;
- security, retention, access, incident, and posthumous-data policies;
- controls for emotional dependency, impersonation, reputational harm, and family/third-party data;
- a clear statement that prediction, imitation, consciousness, and personal survival are different claims.

Third parties may not nominate another person for modeling. “They gave me permission” is not verifiable consent.

## The first three publishable experiments

The lab should not wait for war, elections, and generations before producing knowledge.

### Experiment 1 — The continuity benchmark

- Four residents, 30–90 simulated days.
- Compare memory/scaffold variants under identical cached decisions and scripted events.
- Perturb memory and model assignment.
- Measure held-out choice prediction, commitments, source accuracy, and resident distinguishability.

**Success:** a preregistered scaffold beats biography-only and transcript-RAG baselines.  
**Useful negative result:** current LLMs do not maintain distinguishable identity under controlled perturbation.

### Experiment 2 — Model transplant

- Freeze one resident’s structured life-history artifact.
- Run it through multiple models and prompt implementations.
- Compare transplant variance with ordinary within-life change and between-resident differences.

**Success:** identify what persists in the scaffold versus what belongs to the base model.  
**Lab value:** a practical model/provider portability benchmark.

### Experiment 3 — Social grounding ablation

- Compare isolated identity memory with reciprocal social memory in a small causal resource task.
- Remove or scramble how other residents remember the target.
- Test whether identity continuity depends partly on social recognition and obligation.

**Success:** quantify a causal contribution from relationships rather than merely asserting that a “whole world” is necessary.

These experiments can run before the full agrarian ecology. They create a research spine while Phase 1 builds the material kernel.

## Lab operating system

Calling Wega an AI lab becomes credible through behavior, not the landing page.

Required practices:

1. **One explicit thesis per quarter.** State what would change the lab’s mind.
2. **Preregister outcome labels, hypotheses, exclusions, and primary analyses** before expensive runs.
3. **Version every protocol, prompt, model profile, parameter set, and dataset.** The documentation root needs version control; nested website repositories do not provide provenance for the research plan.
4. **Publish negative and null results.** A world that stays peaceful or agents that fail identity tests are findings.
5. **Separate demonstration from evidence.** The canonical valley is an exhibit and systems test; research claims come from registered cohorts and controls.
6. **Use experiment cards.** Each release states question, design, variables, validity range, power/replicates, results, cost, deviations, and artifacts.
7. **Invite adversarial replication.** Provide manifests, recorded model outputs where licensing/privacy permits, and reconstruction tools.
8. **Add outside expertise when a claim crosses domains.** At minimum: ABM methodology, psychology/identity measurement, philosophy of personal identity, security/privacy, and—before human data—research ethics.

### Brand and project boundary

Wega Labs may host multiple experiments, but each needs a unique public identity, threat model, repository, and claim set. The existing “December Sato” autonomous Mac mini project is not this December. Reusing the name makes the terrarium look like an unrestricted computer-control experiment and makes citations, incidents, results, and public expectations ambiguous. Before public launch, rename one project or establish an unmistakable parent/project naming scheme; unrestricted host privileges and social-media credentials are never inherited as this lab’s operating model.

## Research artifacts and possible moat

The defensible asset is not “we run agents continuously.” Many projects do that. It is the combination of:

- authoritative causal life histories;
- private information lineage;
- identity state that can survive model replacement;
- branchable counterfactual lives;
- longitudinal evaluations rather than transcript demos;
- provider-bias and refusal measurements;
- open, inspectable world mechanics.

Potential products—without corrupting the research agenda—include persistent NPC infrastructure, agent regression/evaluation services, simulation tooling, model-behavior observability, and licensed living-world experiences. Immortality should not be the business model.

## Twelve-month proof of seriousness

### Months 0–2

- Resolve Gate 0 owner decisions and version the research corpus.
- Publish the claims ladder, ethics boundary, and experiment-card template.
- Build the minimal event/decision/memory harness.
- Run the continuity benchmark without the full world.

### Months 3–5

- Complete the minimal material kernel and null baselines.
- Publish model-transplant and social-grounding results.
- Release the first open benchmark/data artifact.

### Months 6–9

- Add four-resident causal life experiments, construction, and reciprocal institutions.
- Demonstrate independent replay of recorded histories.
- Recruit external methodological reviewers.

### Months 10–12

- Run the first registered settlement cohorts.
- Launch the canonical observer world only if operational gates pass.
- Publish an annual report containing failures, costs, changed beliefs, and next hypotheses.

## Kill and pivot criteria

The lab should narrow or pivot December if, after controlled experiments:

- identity scores are explained almost entirely by prompt/persona leakage;
- different residents are not more distinguishable than repeated samples of one model;
- model-provider choice overwhelms memory, relationship, and world interventions;
- causal-world complexity adds no measurable value over simpler task environments;
- results cannot be independently reconstructed;
- human-continuity language consistently attracts attention while technical work produces no relevant evidence;
- the cost of registered cohorts prevents adequate replication.

Even under those outcomes, the kernel and evaluation tools may remain valuable. A serious lab is allowed to discover that its motivating theory was wrong.

## Public-language contract

Use:

- “December studies persistence and identity in synthetic agents.”
- “The long-horizon motivation is whether patterns relevant to a human life could persist beyond biology.”
- “The current experiments cannot establish consciousness or human survival.”

Avoid:

- “The experiment makes consciousness testable.”
- “Artificial people” without an immediate clarification that they are software personas.
- “Request a human participant” before a human-subject protocol exists.
- “What must be preserved for a person to continue” as if the relevant theory were settled.
- “Immortality is the question” as the primary project headline; it invites a conclusion the protocol cannot adjudicate.
