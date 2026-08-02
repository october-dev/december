# Open-source adoption: what December should borrow

**Status:** living adoption register, last reviewed 2026-08-02
**Rule:** reuse implementations and interface ideas; never outsource canonical truth.

December does not need to invent every renderer, model gateway, memory index, experiment runner, or observability screen. It does need to own the causal rules that distinguish it from an animated group chat. Every donor is therefore classified as **adopt**, **port selectively**, **study**, or **reject as authority**.

License compatibility must be checked against the exact version, package subtree, assets, and transitive dependencies before code enters the canonical repository. A repository-level license is not automatically an asset license.

## Current decisions

| Donor | Useful parts | Decision now | Boundary |
|---|---|---|---|
| [AI Town](https://github.com/a16z-infra/ai-town) | PixiJS tile renderer, camera, sprite animation, selection UI, map/sprite editors, debug paths, movement utilities | **Adopt/port selectively.** The first renderer spike is based on upstream commit `7b24233`. | Do not adopt Convex as canonical state, wall-clock scheduling, the autonomous chat loop, or conversation memory as identity. Preserve MIT attribution and audit asset licenses separately. |
| [Concordia](https://github.com/google-deepmind/concordia) | Experiment composition, agent components, scenarios, measurements, grounded action/outcome separation | **Study and port patterns.** | Its language-mediated Game Master must not decide December physics or silently narrate outcomes. Typed commands still pass through December's kernel. |
| [Mesa](https://github.com/mesa/mesa) | Classical agent-based models, schedulers, spatial models, batch runs, data collection, calibration examples | **Benchmark and use around the kernel if valuable.** | Do not replace the working event/hash/RNG spine merely for framework conformity. Use Mesa first for comparison models and ensemble tooling. |
| [Generative Agents](https://github.com/joonspk-research/generative_agents) | Observation-memory-reflection-planning decomposition and the Smallville reference implementation | **Study; reimplement the minimum.** | Do not import its global knowledge assumptions, free-form action consequences, wall-clock coupling, or prompt-era dependencies. |
| [AgentSociety](https://github.com/tsinghua-fib-lab/AgentSociety) | Need/behavior coupling, typed action blocks, interviews, interventions, experiment metrics, model monitoring | **Study APIs and evaluation tools.** | Its urban-scale stack and commercial subtree are unnecessary for the first valley. Review licensing per package before reuse. |
| [OASIS](https://github.com/camel-ai/oasis) | Activation probability, large-population scheduling, PettingZoo-style environment/action interface, token accounting | **Study later for institutions and communication networks.** | It models social platforms rather than embodied material survival. Its scale is not December's present bottleneck. |
| [LiteLLM](https://github.com/BerriAI/litellm) | One API across MiniMax, OpenRouter and other providers; retries, routing, spend tracking | **Candidate for the Phase 2 model gateway.** | Keep it outside the kernel. Persist exact prompts/responses and enforce December's own hard budget ledger even if gateway budgets exist. Recheck current licensing before pinning. |
| [Langfuse](https://github.com/langfuse/langfuse) and [OpenTelemetry](https://github.com/open-telemetry) | LLM traces, latency, token/cost metrics, prompt/evaluation inspection | **Optional operations layer after cognition exists.** | Telemetry is not canonical history and must not receive private resident state without an explicit data policy. |

## AI Town extraction map

Take or adapt now:

- `PixiStaticMap`, `PixiViewport`, `Character`, sprite sheets, and the tile map;
- click selection, name labels, pan/zoom, observer-side interpolation, and replay speed controls;
- the included level/sprite editors after their asset provenance is reviewed;
- pathfinding and collision utilities only after they are converted into deterministic kernel-side movement validation or a disposable planning helper whose result the kernel checks;
- historical interpolation and debug-path ideas for replay inspection.

Study before porting:

- memory scoring by relevance, importance, and recency;
- reflection/conversation summaries as fallible private memories;
- reactive historical views and multiplayer observer patterns.

Do not adopt as December's core:

- Convex tables or transactions as the authoritative event model;
- JavaScript wall-clock time as simulated time;
- LLM prose directly changing location, inventory, relationships, or institutions;
- continuous agent-to-agent chatting as the main scheduler;
- embeddings as the memory source of truth;
- one generic `doSomething` loop in place of typed action schemas.

## Implemented proof: Kernel-driven Day One

The first end-to-end path now exists:

```text
scripted typed commands
        ↓
December Python kernel
        ↓
canonical binary event log + state hashes
        ↓
december.observer.v1
snapshot.json + events.jsonl + manifest.json
        ↓
read-only AI Town-derived PixiJS viewer
```

The observer contract is deterministic: exporting identical history twice produces byte-identical files. A snapshot declares its sequence fence and event-chain head; the JSONL stream must begin at the next sequence and continue that hash. The browser validates the contract version and event count before presenting it.

This proves the truth path, not agency. Four resident bodies, grain stocks, time, movement, and activities are canonical. Their Day One commands are scripted. There is still no ecology, private perception, memory, model call, deliberation, or autonomous action selection.

## Adoption sequence

1. Keep the current AI Town-derived renderer while December's world contract changes rapidly.
2. Port or replace only the exact renderer modules we use into a clean first-party frontend repository, retaining notices and asset credits.
3. Benchmark Mesa against the custom runtime for ecology ensembles; do not decide by familiarity.
4. Build December's typed cognition boundary before selecting LiteLLM or another gateway.
5. Evaluate Concordia, AgentSociety, and Generative Agents using one identical four-resident scenario. Borrow components only when they improve a declared R0 measurement.
6. Add Langfuse/OpenTelemetry only when real model calls create something worth tracing.

The recurring test is simple: **does this donor help December produce or inspect causal history, or does it merely make agents talk more?** The former is leverage. The latter is usually theatre.
