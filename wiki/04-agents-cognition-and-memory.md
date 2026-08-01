# 04 — Agents, Cognition, and Memory

## Division of responsibility

The LLM is responsible for interpretation and choice under ambiguity. It is not responsible for arithmetic, physics, hidden state, permissions, or final outcomes.

| LLM may do | Kernel must do |
|---|---|
| Infer priorities from needs, values, relationships, and beliefs | Determine needs and feasible actions |
| Form goals and plans | Reserve time/resources and validate dependencies |
| Choose whom to contact and what to say | Deliver messages only through valid channels/range |
| Propose projects, policies, groups, and bargains | Compile/validate them and mutate state |
| Interpret events and update subjective beliefs | Preserve objective events and information provenance |
| Vote, negotiate, teach, deceive, forgive, threaten | Enforce capabilities, transfers, combat, health, and law |

## Cognitive loop

The default full-resident loop is adapted from long-horizon agent work:

1. **Trigger:** need threshold, scheduled commitment, new observation/message, project dependency, danger, social request, or periodic reflection.
2. **Perceive:** kernel produces a private observation packet from line of sight/proximity, body state, accessible artifacts, and incoming communication.
3. **Recall:** memory service retrieves relevant episodic, semantic, social, commitment, and procedural records with source/confidence.
4. **Appraise:** compact model call identifies salient changes, urgency, opportunities, and belief updates.
5. **Deliberate:** agent chooses a goal or revises an existing plan; expensive call only for consequential/novel decisions.
6. **Propose:** typed command or multi-step intent with expected preconditions.
7. **Validate:** kernel accepts, rejects, or returns feasible alternatives and reasons.
8. **Act/communicate:** action consumes simulated time; interruptions are possible.
9. **Observe outcome:** result packet includes only knowable consequences.
10. **Review:** update memories, relationship evidence, commitments, and future triggers.

The loop may finish without dialogue. Physical work and silence are normal.

## Model tiers

### Tier A — deterministic/reactive

Used for sleep, eating routine, continuing reserved work, simple travel, emergency reflexes, and lightweight background people. No LLM call.

### Tier B — small/cheap model

Used for appraisal, short speech, memory compression, routine choice, and checking plans. A low-cost model is appropriate, but note that most cheap models — MiniMax and DeepSeek among them — offer only best-effort JSON rather than schema-guaranteed decoding, so Tier B depends on the validity ladder in [`16`](16-cost-model-and-model-selection.md) §5. **Prompt-cache TTL is a first-rank selection criterion at this tier**, because Tier B is where the token volume lives.

### Tier C — stronger model

Used for constitutional proposals, conflict mediation, long project decomposition, novel design, high-stakes bargaining, and major life choices. It is invoked by a bounded “decision significance” score and budget policy.

### Tier D — offline analyst

Used outside canonical causality for summaries, anomaly review, clustering histories, and shadow-world comparisons. It never acts as a resident.

## Decision significance

Significance is computed by the kernel from:

- irreversible consequences (death risk, migration, office transfer);
- resource value and number of affected people;
- novelty relative to known plans;
- social/political impact;
- uncertainty/conflicting commitments;
- time since last deep deliberation.

This routes tokens based on consequence, not the verbosity of an agent.

**The significance threshold is December's single most important cost control.** In the modelled configuration, Tier C accounts for roughly 10% of calls and 89% of spend ([`16`](16-cost-model-and-model-selection.md) §4) — doubling the population costs less than upgrading the Tier C model one tier. This parameter therefore needs live tuning, its own dashboard, and its own alert, rather than a constant in a config file.

## Structured action protocol

Model output must validate against a versioned schema. A command contains:

```json
{
  "schema_version": "1.0",
  "actor_id": "person:...",
  "intent": "construct|transfer|speak|travel|propose_rule|vote|...",
  "target_ids": [],
  "parameters": {},
  "preconditions_believed": [],
  "reason_codes": [],
  "commitment_ids": [],
  "fallbacks": [],
  "private_rationale_summary": "..."
}
```

Free text is allowed only inside bounded fields. The server ignores unknown fields, rejects invalid enum/ID/unit values, checks authority and feasibility, and never executes generated code.

## Needs, values, goals, and traits

These must not collapse into a single utility number.

- **Needs:** body-derived pressure such as hydration, energy, sleep, safety, belonging, care obligations.
- **Values:** priorities such as reciprocity, autonomy, tradition, security, status, generosity, truthfulness.
- **Goals:** explicit, revisable desired states with deadlines and dependencies.
- **Commitments:** promises, offices, work assignments, debts, care roles, and scheduled meetings.
- **Traits:** stable tendencies with uncertainty, used as context rather than deterministic rules.
- **Appraisals:** short-lived interpretations that approximate emotion: loss, threat, injustice, gratitude, shame, hope.

The kernel calculates needs; agents interpret their importance. A thirsty resident can still finish rescuing someone, but incurs the bodily cost.

## Memory architecture

### Objective event store

Immutable world history. Never summarized away. This is not resident memory.

### Observation memory

What the resident directly perceived, with event reference, timestamp, sensory/source channel, fidelity, and visibility constraints.

### Testimony memory

What another person claimed, preserving speaker, chain of transmission, confidence, and possible contradiction. Rumor never becomes direct observation.

### Episodic memory

Resident-centered experiences and their appraisals. Episodes may be compressed, but compression retains source links.

### Semantic belief memory

Claims about people/world with confidence, supporting/contradicting evidence, last revision, and visibility. Beliefs can be false.

### Social memory

Relationship-specific evidence and domain trust. Updates are bounded; one dramatic conversation cannot arbitrarily overwrite years of history.

### Commitment and procedural memory

Promises, tasks, deadlines, rules, techniques, recipes, and skills. These use structured records, not vector retrieval alone.

## Retrieval

Memory retrieval combines:

- exact filters for entity, time, place, commitment, rule, and project;
- recency and unresolved status;
- salience computed when the event occurred;
- semantic similarity for fuzzy recall;
- relationship relevance;
- a diversity penalty to prevent one event dominating context.

The prompt includes source labels: `DIRECT`, `TOLD_BY`, `PUBLIC_RECORD`, `INFERENCE`, `RUMOR`. A hidden-state leak test inserts canary facts that an agent must never mention before receiving them.

## Forgetting and consolidation

Raw observations remain in cold storage for audit. An agent’s accessible memory changes:

- routine episodes decay in retrieval weight;
- repeated experiences consolidate into beliefs/habits;
- important unresolved events remain salient;
- reflection may revise interpretation but cannot rewrite source facts;
- sleep or low-activity periods run consolidation jobs;
- memory budgets are per resident, not one shared context.

Memory systems are a documented source of severe agent failure, and the failure taxonomy should be tested directly. Recent stress-testing work classifies the modes as **summary failure** (information deleted or malformed during compression), **storage failure**, **retrieval failure**, and **reasoning failure** over retrieved content. December's exposure differs by mode: summary failure threatens the consolidation jobs below, retrieval failure threatens the diversity penalty and salience weighting, and reasoning failure is where a resident confidently acts on a correctly retrieved but misread memory.

Each mode needs its own test rather than a general "memory works" assertion. Note that source confusion — a resident treating rumor as direct observation — is a December-specific concern arising from our source-labeling design rather than a category from that literature, and it is covered by the canary suite.

## Communication

Communication is an action with location/range, duration, audience, interruption risk, and speech-act type. Channels include face-to-face, shout/signal, messenger, meeting, and durable public artifact. The kernel records utterance content but only delivers it to actual recipients.

Agents may deceive. The system records what was said, not whether it is “really true” in the speaker’s mind. Private rationale is sensitive developer telemetry and must never automatically leak to other residents.

## Learning and culture

Skills increase through practice and teaching with diminishing returns. Techniques require prerequisite concepts, tools, and demonstrations. Cultural items—stories, norms, symbols, rituals, names—can be proposed in language, but become socially real only through repeated use, transmission, or institutional recognition.

Novel technology is constrained:

1. agent proposes a function or design using known concepts;
2. project compiler maps it to allowed material primitives;
3. unknown mechanisms are rejected or marked experimental;
4. prototype consumes materials/labor;
5. test events determine function and defects;
6. successful technique becomes teachable procedural knowledge.

This allows invention without letting prose manufacture capability.

## Identity continuity and model swaps

An agent is not identical to its current model. Its operational identity state includes structured biography, body, memories, relationships, values, goals, commitments, speech-style hints, and causal history. Whether that state is sufficient for personal identity is a research question, not an architectural fact. Model changes are logged, and controlled transplant experiments compare what persists with within-model and between-resident baselines ([`18`](18-lab-charter-and-research-program.md)).

Residents need heterogeneous motives as well as heterogeneous styles. Survival is a body pressure, not a universal objective. A resident may prioritize kin, status, dominance, territory, revenge, novelty, devotion, honor, ideology, or self-sacrifice above their own safety. These tendencies are persistent, state-conditioned, and socially reinforced or suppressed—not a flat “chance of evil” roll.

## Behavioral diversity is a requirement, not an emergent luxury

Twelve residents driven by one model with one prompt template converge. They adopt similar phrasing, similar risk postures, and similar reasoning, because they are one distribution sampled twelve times. A settlement of near-identical minds cannot produce factions, and any factions it does produce are artifacts of the initial value draw rather than of social process.

This is not covered by the trait and value machinery above, which varies *inputs* without guaranteeing varied *outputs*.

- **Measure it.** Behavioral diversity is an operational metric: distribution of chosen action types per resident per context class, lexical divergence across residents, and disagreement rate in shared decisions. Track it continuously; a falling trend is a defect.
- **Mitigate structurally.** Distinct value and biography draws, per-resident prompt variation, and — where budget allows — assigning different residents to different models, which is the strongest available lever and also hedges provider drift.
- **Test it.** A homogeneity check belongs in the model admission suite: if two residents with materially different values, needs, and histories produce interchangeable decisions across a scenario battery, the configuration fails admission.

## Failure policies

- Invalid output: constrained decoding where supported, then local validation, then one repair attempt, then **escalation to a schema-guaranteed model** rather than a retry on the same one, then safe deterministic fallback. The full ladder is in [`16`](16-cost-model-and-model-selection.md) §5 — it exists because the models December can afford largely do **not** support strict JSON-schema decoding.
- Provider timeout: retry under the same `decision_id`; the first durably recorded resolution wins, and a late divergent response is discarded and counted.
- **Model refusal or character break:** logged as a distinct failure class, never silently retried into compliance. A model that declines to represent conflict, deception, or household formation is imposing a systematic behavioral bias that would be misread as an emergent finding — see [`16`](16-cost-model-and-model-selection.md) §6. Refusal rates are part of every model profile and are reported alongside any behavioral result.
- Repeated contradiction: force appraisal refresh from authoritative private state.
- Context overflow: deterministic context builder truncates low-priority memories and logs omissions.
- Budget exhausted: stop noncanonical analysis, downgrade routine cognition, and pause at unresolved consequential decisions if no admitted model is available; world physics may continue only to the next cognition barrier.
- Agent stuck in rejected loop: cooldown, feasible-alternative packet **filtered for visibility**, then the resident’s predeclared low-stakes routine policy—not a universal survival-maximizing personality.
