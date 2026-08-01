# ADR-003 — Embodiment is a replaceable adapter

- **Status:** Accepted for audit
- **Date:** 2026-08-01

## Context

Minecraft/Luanti and open RTS engines offer compelling visuals and actions, but their mechanics are designed for games. Choosing one first would force the social/material model into its abstractions and could make headless experiments and deterministic replay difficult.

## Decision

Build and validate the headless kernel with a simple grid view. Define a world-adapter contract. Compare a polished 2D view with Craftium/Luanti at Gate 6 using determinism, causal legibility, maintenance, construction, performance, licensing, and visual appeal.

## Consequences

- The first demos are visually modest.
- The canonical world remains portable and testable.
- A 3D adapter animates kernel truth and cannot grant resources or decide outcomes.

## Rejected alternatives

- Fork Mindcraft/Minecraft as the entire product.
- Fork an RTS economy as authoritative simulation.
- Commit to 3D before testing social/world mechanics.

