# ADR-008 — Cheap-model-first cognition with a validity escalation ladder

- **Status:** Proposed; confirm at Gate 2
- **Date:** 2026-08-01 (added by audit pass)

## Context

The bottom-up cost model in [`16`](../16-cost-model-and-model-selection.md) produced three findings that together constrain model selection more tightly than the original plan assumed.

First, **Tier C dominates spend**: in the modelled configuration it is roughly 10% of calls and 89% of cost. Doubling the resident population is cheaper than upgrading the Tier C model one tier.

Second, strict JSON-Schema-constrained decoding is uneven. DeepSeek and Qwen offer best-effort JSON; MiniMax documents tool calling but not `response_format`. These models may still carry routine cognition through tool-call framing, local validation, repair, and escalation. Provider syntax guarantees never replace semantic and feasibility checks.

Third, **prompt-cache TTL matters more than headline token price**. Input is over 90% of tokens and a cache miss costs roughly 10× a hit, so DeepSeek's multi-hour automatic cache is worth more than a small per-token advantage over a provider with a five-minute TTL.

Notably, Agentopia hit exactly this wall and resolved it the same way: Qwen for volume, Gemini Flash as a fallback for invalid outputs.

## Decision

Route cognition **cheap-first**, and resolve validity through an escalation ladder rather than by paying for a premium model everywhere:

1. Constrained decoding where the provider supports it.
2. Otherwise tool-call framing with a strict schema, which is better supported than `response_format` on OpenAI-compatible endpoints.
3. Local validation against the versioned schema — always, regardless of provider claims.
4. One repair attempt on the same model with the validation error appended.
5. **Escalation to a schema-guaranteed model** for the repair, not a retry on the same one. This fires only on failure, so it is cheap.
6. Deterministic Tier A fallback, recorded as a `DecisionResolved` event with `resolution: fallback`.

Model profiles gain three first-rank selection criteria: **strict-schema capability, prompt-cache TTL and pricing, and measured refusal rate over the December action grammar.**

The decision-significance threshold that gates Tier C is treated as the primary cost-control instrument, with live tuning, a dashboard, and an alert.

## Amendment — the actual credit position ($2,000 MiniMax + $1,000 OpenRouter)

The owner's prepaid balances make this ADR concrete and reinforce it. MiniMax cannot guarantee schema-valid output and OpenRouter can, so the two pools map onto the ladder almost exactly: **MiniMax carries Tier B volume; OpenRouter carries Tier C judgment and the schema-guaranteed repair escalation.** The escalation target is therefore not a design preference but a structural requirement of the budget.

Two further consequences ([`16`](../16-cost-model-and-model-selection.md) §7a): MiniMax's five-minute cache TTL sits precisely where the token volume is, making cache-aware activation batching a budget mechanism rather than an optimisation; and OpenRouter is the only pool able to assign different residents to different model families, which is the strongest available mitigation for behavioural homogeneity (**R-31**).

## Consequences

- Schema-failure rate per model per decision type becomes an admission criterion and an ongoing metric; a rise after a silent provider update triggers quarantine.
- Budgets use the official current price plus contingency. MiniMax currently labels M3’s displayed 50% reduction permanent; the earlier audit incorrectly called it temporary. The >512 K tier remains twice as expensive.
- The activation scheduler must batch for cache locality, which partially conflicts with sparse activation and is an explicit design tension rather than an oversight.
- Assigning different residents to different models is both a diversity mitigation and a provider-drift hedge, and becomes attractive rather than merely tolerable.

## Rejected alternatives

- **One strong model for everything.** Clean, and roughly an order of magnitude more expensive; Sonnet-tier throughout reaches ~$5,000/month at the unattended pace.
- **One cheap model for everything.** Concentrates schema-repair, semantic-validity, and behavioral-homogeneity risk.
- **Assuming "OpenAI-compatible" implies structured-output-compatible.** This is the specific error the audit found, and it would have surfaced as a mysterious Tier B failure rate deep into Phase 2.
