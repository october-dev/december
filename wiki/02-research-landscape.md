# 02 — Research Landscape and Starting Points

## Decision in brief

No single open-source project is the base we need. The strongest approach is a **composed architecture**:

- a new typed causal kernel, likely built with Mesa’s Python ABM/event primitives;
- Agentopia-inspired resident cognition, contact, review, memory, checkpoints, and long-horizon operation;
- GovSim and Melting Pot as libraries of social dilemmas and evaluation scenarios;
- VillagerAgent/APT ideas for decomposing construction into dependency graphs;
- disease mechanics adapted from established individual-based epidemic models, simplified for a tiny population;
- an optional Craftium/Luanti or custom 2D adapter only after the headless world works;
- LiteLLM for provider routing and Langfuse/OpenTelemetry-style tracing.

“Inspired/adapted” does not mean copy-paste. License compatibility and actual code quality must be checked before code reuse.

## Candidate matrix

| Project | What it gives us | What it does not give us | Proposed use |
|---|---|---|---|
| Agentopia | Long-running social simulation; Plan→Contact→Activity→Review; self-managed memory; append-only records/checkpoints; published token/cost figures | A grounded material world; mature ecosystem; **a LICENSE file** — the repo is three commits deep and legally unlicensed despite a README claim of MIT | Cognitive architecture and cost reference; do not vendor code |
| Stanford Generative Agents | Memory stream, reflection, planning, believable daily behavior | Resource conservation, institutions, long-horizon operations | Foundational cognition patterns and evaluation ideas |
| AI Town | Runnable multiplayer browser town and agent conversations | Deep material, demographic, ecological, or political causality | UI/product reference only |
| MiroFish | Multi-agent simulation and report generation around supplied seed material | Persistent embodied causal world; **AGPL-3.0, whose obligations trigger on network use** — the one genuine licensing trap in the candidate set | Observer-report inspiration only; do not vendor |
| Concordia | Configurable generative-agent simulations with a Game Master and components | Game Master can become an omniscient narrative bottleneck | Experimental harness; borrow component separation, constrain GM authority |
| Mindcraft | Mature Minecraft/Mineflayer action surface; OpenRouter; gathering/crafting/building; multi-agent support | Minecraft is game-balanced, not historically/ecologically realistic; code execution is dangerous | Fast embodied prototype or later adapter; arbitrary code disabled |
| Craftium + Luanti | Fully open sandbox; Gymnasium/PettingZoo APIs; synchronous stepping explicitly for slow agents such as LLMs; ICML 2025 paper | **LGPL-2.1-or-later plus CC BY-SA media**, not permissive; development slowed since Feb 2026; significant integration work | Preferred 3D research adapter candidate after Phase 4 — **and a licensing decision, not just a technical one** |
| MineLand | Multi-agent Minecraft benchmark and tasks | Benchmark rather than persistent civilization | Evaluation/task ideas |
| VillagerAgent | Collective task decomposition and dependency-aware execution | Full society/world simulation | Project compiler and work-allocation patterns |
| APT | Converts text construction goals to structured blueprints | Material society and institutions | Blueprint compilation inspiration |
| GovSim (Piatti et al., NeurIPS 2024) | Commons-governance scenarios with measurable outcomes; MIT | Persistent bodies, ecology, construction, life history; frozen since Jan 2025 | Governance tests and institutional mechanism library |
| GovSimElect | Elected/fixed/leaderless leader comparison over GovSim's fishery | **It is a five-star personal fork of GovSim, not an upstream project** — earlier drafts miscited it | Cite as a fork; useful only for the election variant |
| Agent Ballot Box | Commons framework with a voting/leadership component | Whole polity/world; zero adoption, dormant since mid-2025 | Weak citation; retained for completeness only |
| Melting Pot | 50+ social substrates and 256+ scenarios covering cooperation, competition, deception, reciprocity, trust, coalition behavior | Persistent historical world and LLM-native residents | Regression scenarios and social-mechanism catalog |
| MoralAgentSim | Prehistoric agents that hunt, gather, share, communicate, reproduce, and fight; ACL 2026 Main (oral) | Studies moral evolution, not a persistent material world; unknown engineering maturity | **The closest published analogue to December's premise** — highest-value comparative spike; borrow no claims uncritically |
| AgModel | Open forager–farmer transition model with annual demography/environment and event-based subsistence | LLM cognition and rich institutions | Parameter/mechanism reference for calories, labor, stores, birth/death |
| Artificial Anasazi | Household settlement, land productivity, drought and food surplus | Its own page warns it is unverified; ecology alone does not explain observed collapse | Warning and test case, never historical ground truth |
| Simulating Forager Mobility / archaeology ABMs | Mobility, resource distribution, water tethering, population dynamics, fission–fusion | Production software architecture | Mechanism and validation-pattern references |
| Covasim / Starsim / OpenABM | Individual disease states, contact networks, stochastic transmission, testing discipline | Tiny premodern generic disease out of the box | Adapt architecture and validation, not COVID parameters |
| WarAgent | Structured LLM diplomacy/war simulation | World-war abstraction; little local logistics/embodiment | Diplomacy action grammar reference only |
| 0 A.D. | Historical RTS engine with economy, building, units, battle | Designed balance, large codebase, wrong scale/cognition | Art/interaction inspiration; reject as authoritative base |
| Widelands | Detailed worker/ware/building economy; active open-source project | Economy-game assumptions; C++ integration cost | Recipe/logistics reference; possible visualization research |
| Unknown Horizons | Economy and settlement UI ideas | **Dormant** — last release Jan 2019; the Godot rewrite is a separate repo with no playable content; "Python/Godot" conflates two codebases | UI inspiration only; do not plan around it |
| Freeciv | Mature client/server and rulesets | Civilization-level turns, not individual lives | Ruleset/server architecture reference only |
| OPA | Auditable policy-as-code and capability checks | Natural social process or flexible emergent constitution | Later use for infrastructure authorization, not residents’ full law |
| LiteLLM | Unified gateway, routing, budgets, retries across providers | Simulation semantics | Model gateway candidate |
| Langfuse | LLM traces, cost, latency, prompt/version observability | Canonical world events | Operations telemetry linked to event IDs |

## Why not start by forking an RTS

0 A.D., Widelands, Freeciv, and Unknown Horizons are impressive, but their rules encode gameplay abstractions: accelerated production, balance-driven yields, omniscient players, fungible units, and combat designed for control. Retrofitting individual knowledge, kinship, physiology, continuous life history, institutional authority, and scientific event provenance would fight the engine.

We should still mine them for:

- production-chain and recipe data structures;
- pathfinding and job reservation;
- building placement and visualization;
- client/server separation;
- deterministic replay lessons;
- moddable rulesets and content pipelines.

## Why Mesa is the leading kernel scaffold

Mesa is an Apache-2.0 Python agent-based modeling framework with agent/model primitives, spatial components, data collection, browser visualization, and support for hybrid step/event scheduling. It aligns with the need for scientific experiments and fast iteration.

**Status as of August 2026** (verified during the audit pass — earlier drafts of this wiki were out of date):

- Current stable is **3.5.1** (March 2026), with a **4.0 line in alpha**.
- Discrete-event and hybrid scheduling are **stable, not experimental**: `model.schedule_event()`, `model.schedule_recurring()`, `run_for()`, `run_until()`.
- The `mesa.experimental.devs` simulator classes are **deprecated since 3.5.0 and removed in 4.0**. Any design targeting them is already stale.
- `mesa.space` is maintenance-only, and SolaraViz carries breaking-change risk across minor releases.

That last pair is the important finding: the parts of Mesa December would lean on hardest are the parts under active churn or reduced maintenance. It strengthens rather than weakens the case for the narrow interface. Regardless of the choice:

- event sourcing, deterministic RNG streams, typed commands, and causal provenance must be ours;
- performance must be benchmarked before commitment;
- the core domain must not inherit framework-specific serialization everywhere;
- a narrow `SimulationRuntime` interface must allow replacing Mesa without touching domain code;
- the determinism constraints in [`14`](14-determinism-replay-and-state-integrity.md) §D2 apply to any runtime — a framework that iterates unordered collections or reads wall-clock time inside the step loop is disqualified regardless of its other merits.

The decision gate is a Phase 1 spike comparing Mesa against a small custom event loop on determinism, throughput, profiling, checkpointing, and developer clarity. Given that December needs its own scheduler semantics, its own event store, its own RNG discipline, and its own provenance model, the honest prior is that Mesa earns its place as a **spatial and data-collection toolkit** rather than as the kernel.

## Research methods we adopt

### ODD

The Overview–Design concepts–Details protocol is a standard way to describe individual/agent-based models. Each kernel subsystem will have an ODD-compatible specification covering purpose, entities/state, process/scheduling, design concepts, initialization, input data, and submodels.

### TRACE-style evaluation

Documentation must include problem formulation, conceptual model, implementation verification, parameterization, data evaluation, model analysis, and output corroboration. We use this as a discipline even though December is not initially a scientific policy model.

### Pattern-oriented validation

We should test multiple patterns simultaneously rather than tune one headline outcome. For example, a food system should reproduce plausible seasonality, labor bottlenecks, storage buffering, and starvation response—not merely an average annual yield.

### Ensemble and ablation experiments

One beautiful run proves almost nothing. Each version must run many seeds, sweep uncertain parameters, and remove proposed mechanisms to demonstrate which outcomes depend on which mechanisms.

## Rejected shortcuts

- **LLM as environment simulator:** fluent but non-conservative, difficult to reproduce, and vulnerable to prompt drift.
- **A “chaos slider”:** makes drama authorial rather than emergent.
- **All agents awake every minute:** cost-heavy and socially noisy.
- **Infinite crafting via text:** breaks the material contract.
- **One shared memory database:** leaks private knowledge.
- **One model provider:** fragile and wastes heterogeneous token balances.
- **World state only in vector search:** approximate retrieval cannot be authoritative.
- **Unrestricted shell/code tools:** unnecessary security and integrity risk.
- **Trusting a README's license claim, or a repository that turns out to be a fork.** The audit pass found both errors in this wiki's own bibliography. Verify the LICENSE file and the upstream before any reuse decision.
- **Borrowing a mechanism that is invalid at our population size.** A model validated on thousands of agents may be meaningless at eighteen — see realism contract R7 in [`01`](01-scope-and-realism-contract.md).

