# 00 — Vision and North Star

## One-sentence vision

Build a tiny, persistent civilization that produces unscripted but causally explainable history while remaining cheap enough to run continuously and transparent enough to audit like an experiment.

For the larger Wega Labs thesis, this world is an instrument for studying **persistent synthetic agency**—not a direct test of consciousness or immortality. The research claims ladder and first falsifiable experiments are defined in [`18`](18-lab-charter-and-research-program.md).

## Terrarium versus autonomous-agent society

The phrases describe different design commitments.

| Dimension | “Society of autonomous agents” | “Observable AI terrarium” |
|---|---|---|
| Center of attention | Agent personalities and autonomy | The coupled system: people, material world, institutions, ecology, and observer instruments |
| Typical implementation | Several LLMs chat and call tools | Deterministic/stochastic simulation plus bounded LLM decisions |
| Source of events | Often dialogue, prompts, or a narrator | State transitions and conditional hazards |
| Truth | Frequently distributed through prose | One authoritative typed world state |
| Observer | Watches transcripts | Can inspect causal chains, maps, metrics, beliefs, and replay |
| Surprise | Model improvisation | Emergence from interacting mechanisms, with language adding interpretation |
| Failure mode | Expensive role-play; incoherent resources and memory | Over-engineered toy ecology or legible but less theatrical early runs |
| Scientific posture | Demonstration of agents | Instrumented computational world with declared validity limits |

We still want a society of autonomous agents, but it lives **inside** a terrarium. “Terrarium” reminds us that habitat, constraints, observation, and experimental control matter as much as minds.

## The desired return-after-two-days experience

The home screen should answer four questions in under a minute:

1. **What changed?** Population, stores, territory, buildings, offices, law, factions, health, ecological indicators.
2. **What happened?** A ranked timeline of births, deaths, projects, votes, disputes, discoveries, migrations, disasters, and battles.
3. **Why?** A causal graph from outcome back to decisions, observations, physical constraints, and random draws.
4. **What might have happened?** Optional shadow branches from selected decision points.

An illustrative—not scripted—history might read:

> Year 3, late dry season: low winter rainfall cut the east stream to 38% of its median flow. The council rationed irrigation, but two households concealed grain. A child’s testimony shifted the election. The defeated steward refused the audit, left with four supporters, and occupied the upstream weir. A confrontation injured three people. Close-contact care spread a respiratory infection. With labor unavailable, the millet harvest failed; eight residents migrated and the original settlement ended the winter with five survivors.

Each sentence must link to underlying events and evidence. The system is a failure if it can produce the paragraph but not justify it.

## Experience pillars

### 1. Causal depth

Consequences should cross systems. Rain affects soil and streams; those affect labor and harvest; stores affect bargaining power; institutions affect distribution; distribution affects health and loyalty; injury affects productive capacity. Modules cannot be isolated minigames.

### 2. Persistent personhood

Agents have bodies, histories, relationships, obligations, skills, incomplete knowledge, and limited time. Their choices should reflect these without collapsing into fixed personality stereotypes.

### 3. Institutional emergence

There is no compulsory “democracy module.” Residents can create offices, voting rules, councils, customary law, ownership norms, sanctions, alliances, or authoritarian arrangements using a bounded institutional grammar. Elections become possible when people enact them.

### 4. Constructive agency

Residents can propose genuinely new combinations of known capabilities: buildings, work processes, symbols, schedules, organizations, records, and policies. New things enter reality through blueprints, bills of materials, labor, tests, and use—not by being mentioned.

### 5. Legible surprise

Surprise is valuable only if it is neither pre-authored nor inexplicable. We optimize for **retrospective inevitability**: after seeing the causes, the outcome makes sense, though it was not obvious beforehand.

### 6. Long-horizon durability

The world survives restarts, provider outages, malformed model output, budget limits, and schema upgrades. It can run headlessly for weeks. Every canonical history is versioned and backed up.

## Success criteria

The project is successful when all are true. **Every criterion below that uses a label — "governance form," "faction," "cascade" — requires a pre-registered operational definition before the runs that test it**, per [`17`](17-initial-conditions-and-authorship.md). A criterion whose definition is chosen after seeing the results is not a criterion.

- In blinded review, observers distinguish independent causal histories and can correctly identify major causes from evidence.
- **Replays reproduce identical state hashes at every checkpoint within a pinned environment** — same code commit, config, dependency lockfile, interpreter build, CPU architecture, and model-response cache. Replay hard-fails rather than calling a live model on a cache miss. Portable bit-identity across machines is *not* claimed unless the kernel adopts integer-valued state; see [`14`](14-determinism-replay-and-state-integrity.md).
- Removing any one major pressure—seasonality, resource conservation, social memory, institutions—measurably changes population-level outcomes **relative to a null demographic model**, so that small-population noise is not mistaken for mechanism.
- Agents accomplish multi-day construction and institutional projects without developer-authored sequences.
- At least three governance forms arise across seeded runs that are **structurally distinct under the pre-registered definition** and persist beyond a declared duration — including in runs seeded without an inherited charter.
- Rare cascades such as settlement fission, introduced-disease outbreaks, war, or extinction occur in some parameter regions but are not guaranteed. At this population size, imported acute infections should show substantial stochastic fade-out and occasional large outbreaks across ensembles; intermediate outbreaks remain possible ([`15`](15-parameter-registry.md) §D).
- An auditor can trace every material mutation to code version, command, preconditions, authorization, and random seed.
- A seven-day soak test completes without human repair, unbounded costs, state corruption, or narrative/world divergence.
- **Observed cost per simulated day stays within the owner-approved envelope** ([`16`](16-cost-model-and-model-selection.md)), and model refusal rates are measured and reported alongside any behavioral finding.

## Explicit anti-goals

- A scientific forecast of real human societies.
- A conscious-being claim or moral-patient experiment.
- A chatroom with biographies and a simulated clock.
- A god-game where the observer secretly nudges events in the canonical run.
- Maximum population, graphical fidelity, or token consumption.
- A system in which agents write and execute unrestricted code.
- A world optimized to produce violence or catastrophe on demand.
- A single giant prompt containing the entire civilization.

## Lab-level success

The canonical valley is a compelling exhibit and operational test, not by itself a scientific cohort. Wega Labs earns the “lab” label by producing registered experiments, baselines, reconstructable artifacts, negative results, and changes of belief. In the first year, success means a credible longitudinal identity benchmark, controlled model-transplant and social-grounding results, and a replayable causal-agent testbed—even if the canonical world never produces a spectacular war or extinction.

## Working title and terminology

“December” is the project codename. “The Living Terrarium” is the product concept. “Canonical world” means the one continuous history visible to the observer. “Shadow world” means a non-canonical fork used for analysis. “Resident” means an individually simulated person. “World kernel” means the authoritative transition system. “Director” means a read-only summarizer and camera planner; it has no mutation authority.
