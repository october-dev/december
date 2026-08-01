# ADR-001 — The authoritative world is a causal kernel, not an LLM

- **Status:** Accepted for audit
- **Date:** 2026-08-01

## Context

Language models are excellent at interpretation, language, negotiation, and proposing plans. They are unreliable stock ledgers, clocks, physics engines, permission systems, and reproducible stochastic processes. Asking one model to narrate the environment would make famine, war, construction, and extinction impossible to verify.

## Decision

A typed deterministic/stochastic kernel owns all authoritative state and resolves commands. LLMs receive private observations and propose schema-valid actions. A read-only director summarizes events but has no mutation path.

## Consequences

- More up-front simulation engineering.
- Less immediate cinematic variety.
- Strong conservation, replay, partial observability, causal explanation, provider swapping, and testing.
- Creative physical actions require a bounded project compiler.

## Rejected alternatives

- One LLM/Game Master narrates all consequences.
- Agents negotiate shared truth in conversation.
- Renderer/game engine owns one truth while database owns another.

