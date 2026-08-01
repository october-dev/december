# 16 — Bottom-Up Cost Model and Model Selection

**Status:** added by the 2026-08-01 audit pass. **All prices observed 2026-08-01 and will be stale within weeks — re-derive before committing a budget.**

## Why this document exists

Risk **R-04** ("token spend explodes") is rated High/High in [`11`](11-risks-decisions-open-questions.md), and the whole project is gated on "continuous operation within bounded cost." Yet the only number in any prior draft was an illustrative arithmetic exercise on someone else's published token totals. A project whose top operational risk has no bottom-up estimate cannot pass its own Gate 0.

This document builds the estimate from activation counts upward, prices it against the actual August 2026 market, and identifies which decisions dominate the bill.

## The Agentopia reference point, restated correctly

Prior drafts cited Agentopia's token volume without stating what it was. Verified against the paper (arXiv:2606.07513, Table 4):

- **13,347 M input tokens, 352 M output tokens, 567 K LLM calls** — these are **averages across three simulation worlds**, not a single run. Per-run input ranged 9,699–19,041 M.
- The run covered **100 agents over 10 simulated years** and took **~186 wall-clock hours**.
- The model was **Qwen3.5-397B with Gemini 3 Flash as a fallback for invalid outputs** — a detail that matters enormously and is discussed in §5 below.

Two derived figures are the useful ones:

| Derived quantity | Value | Why it matters |
|---|---|---|
| Calls per agent per simulated day | **1.55** | Sparse activation is achievable at scale |
| Input tokens per call | **23,540** | Contexts are large; input dominates |
| **Input : output ratio** | **38 : 1** | **Prompt caching is the primary cost lever, not output brevity** |
| Simulated days per wall-clock hour | 19.6 | Throughput is not the binding constraint |

The old draft's "$4.4k" substitution should be discarded. It priced someone else's workload at a rate for a different model and told us nothing about December.

## 1. Activation model

December's cognition is denser per agent than Agentopia's (an explicit appraise/deliberate/review cycle rather than a weekly loop) but runs on far fewer agents. Central case, per simulated day:

| Call class | Callers | Calls each | Total calls | Input each | Output each |
|---|---:|---:|---:|---:|---:|
| Tier B — appraisal, routine choice, short speech | 12 full residents | 12 | 144 | 4,500 | 300 |
| Tier B — lightweight residents | 6 dependants/elders | 1 | 6 | 3,000 | 200 |
| Tier C — consequential deliberation | 12 full residents | 1.5 | 18 | 12,000 | 900 |
| Director / observer summarization | — | — | 10 | 8,000 | 1,200 |
| **Total per simulated day** | | | **178** | **≈ 971 K** | **≈ 73 K** |

Input : output ≈ **13 : 1**.

**Cross-check against Agentopia.** December: 971 K input ÷ 18 residents ≈ **54 K input tokens per resident per simulated day**. Agentopia: 1.55 calls × 23.5 K ≈ **36 K**. This is a sanity check, not independent validation: both are speculative LLM-society workloads with different cognition loops. Until a four-resident prototype measures activation, context, repair, refusal, and cache-hit rates, use the wide envelope below plus a separate experiment reserve.

**Uncertainty is large and asymmetric.** Activation rate and context size each plausibly vary by 2× in either direction, so the honest envelope is **0.25× to 4×** the central case. All figures below should be read with that band.

## 2. Price landscape, August 2026

| Model | Input $/M | Output $/M | Notes |
|---|---:|---:|---|
| Zhipu GLM-4.7-Flash | 0.06 | 0.40 | |
| OpenAI gpt-5-nano | 0.05 | 0.40 | |
| Qwen3.5-Flash | 0.10 | 0.40 | |
| DeepSeek v4-flash | 0.14 | 0.28 | Cache hits at $0.0028 — a **50× read discount** |
| OpenAI GPT-5.6 Luna | 1.00 | 6.00 | Official GPT-5.6 family pricing; 30-minute minimum cache life |
| Google Gemini 2.5 Flash-Lite | 0.10 | 0.40 | |
| Google Gemini 3.5 Flash-Lite | 0.30 | 2.50 | |
| MiniMax M3 | 0.30 | 1.20 | ≤512 K tier; official page labels this **Permanent 50% off**, not a temporary promotion |
| MiniMax M2.7 | 0.30 | 1.20 | Not marked promotional |
| Anthropic Claude Haiku 4.5 | 1.00 | 5.00 | |
| Anthropic Claude Sonnet 5 | 3.00 | 15.00 | Introductory 2.00 / 10.00 through 2026-08-31 |

**Corrections:** M2.5 is legacy; M3 is the current flagship (1 M context) and M2.7 the mid-line workhorse. MiniMax's official page describes M3's displayed reduction as **permanent**, so the first audit was wrong to call it temporary and to advise budgeting at a higher "list" price. Prompts above 512 K cost twice the displayed standard tier.

**Re-verified 2026-08-01 (third check):** GPT-5.6 Luna's *standard* tier is **$0.20 input / $1.20 output** per million (short context), with long context at $0.40/$1.80, batch and flex at $0.10/$0.60, and fast mode at $0.40/$2.40. The second audit's assertion of "$1/$6" does not correspond to any tier on the official pricing page and has been withdrawn. The row is restored below:

| Model | Input $/M | Output $/M | Notes |
|---|---:|---:|---|
| OpenAI gpt-5.6-luna | 0.20 | 1.20 | Standard, short context; batch/flex 0.10/0.60 |

This is the second time a pricing figure has moved on re-check. Treat every price in this document as a snapshot requiring verification before it is committed to a budget, and prefer fetching the provider page over trusting any summary — including this one.

## 3. Cost per simulated day and per month

Two paces from [`01`](01-scope-and-realism-contract.md): attended (1 real hour = 1 simulated day → **730 simulated days/month**) and unattended (1 real hour = 3 simulated days → **2,190 simulated days/month**).

The following planning scenario assumes 65% of input is a stable cacheable prefix read at roughly 0.1×. That is **not provider-neutral**: cache semantics, routing affinity, TTL, writes, and OpenRouter provider selection vary. Gate 2 replaces it with measured hit/write rates.

| Model (single-tier) | $/sim-day uncached | $/sim-day cached | $/month @ 730 | $/month @ 2,190 |
|---|---:|---:|---:|---:|
| gpt-5-nano | 0.08 | 0.05 | **37** | **110** |
| GLM-4.7-Flash | 0.09 | 0.05 | **37** | **110** |
| DeepSeek v4-flash | 0.16 | 0.07 | **51** | **153** |
| MiniMax M3 (current ≤512 K tier) | 0.38 | 0.21 | 153 | 460 |
| Gemini 3.5 Flash-Lite | 0.47 | 0.27 | 197 | 591 |
| Claude Haiku 4.5 | 1.34 | 0.77 | 562 | 1,686 |
| Claude Sonnet 5 | 4.01 | 2.30 | 1,679 | **5,037** |

**The recommended mixed-tier configuration** — Tier B on a cheap model, Tier C on a strong one:

| Component | Model | $/sim-day |
|---|---|---:|
| Tier B (150 calls, 675 K in / 45 K out) | DeepSeek v4-flash | 0.05 |
| Tier C (18 calls, 216 K in / 16 K out) | Claude Sonnet 5 | 0.51 |
| Director (10 calls) | cheap tier | 0.01 |
| **Total** | | **≈ 0.57** |
| | @ 730 sim-days/month | **≈ $416** |
| | @ 2,190 sim-days/month | **≈ $1,248** |

## 4. What actually drives the bill

**Finding 1 — Tier C model choice dominates, not agent count.** In the mixed configuration, Tier C is **10% of calls and 89% of cost**. Doubling the resident population is cheaper than upgrading the Tier C model one tier. The **decision-significance threshold** in [`04`](04-agents-cognition-and-memory.md) is therefore the primary cost-control instrument in the entire system, and it deserves the engineering attention that would otherwise go to trimming prompts. It should be a live, tunable, monitored parameter with its own dashboard, not a constant buried in config.

**Finding 2 — sparse activation and prompt caching are in direct conflict, and nobody noticed.** This is the sharpest operational finding in this document.

Input is 93% of tokens, so caching the stable prefix (identity block, world rules, action schema, consolidated memory) is the difference between a $50/month world and a $500/month one. But cache entries expire on **wall-clock** TTLs:

| Provider | Cache TTL | Cache read | Cache write |
|---|---|---|---|
| DeepSeek | **hours to days** | ~0.02× | free |
| OpenAI (GPT-5.6+) | **30 min** | 0.1× | 1.25× |
| Google Gemini | 1 h explicit (storage-billed) | 0.1× | no premium |
| Anthropic | **5 min** default; 1 h option | 0.1× | 1.25× / 2× |
| MiniMax | **5 min** | ~0.2× | 1.25× |

Meanwhile [`07`](07-time-emergence-and-observation.md) makes activation deliberately sparse and irregular. At the attended pace, a resident activated ~13 times per simulated day is activated ~13 times per *real hour* — roughly one call every 4.6 real minutes, which straddles a 5-minute TTL. **Every cache miss costs 10× the token price**, so an architecture optimized for fewer calls can easily cost more than one optimized for cache locality.

Required responses:

1. **Cache-aware activation scheduling.** When several residents are due for cognition within a short window, batch them so each resident's prefix is reused inside its TTL rather than scattering calls across the hour.
2. **Treat cache TTL as a model-selection criterion of the first rank.** DeepSeek's multi-hour cache and OpenAI's 30-minute window are worth more to December than a modest per-token price advantage. This belongs in the model profile record in [`08`](08-models-cost-operations-security.md).
3. **Measure cache hit rate per resident per tier as a primary operational metric,** alongside cost. A falling hit rate is the leading indicator of a cost incident.
4. **Structure prompts prefix-stable.** Identity and rules first, volatile observations last. A single early-token change invalidates the whole prefix.

**Finding 3 — batch APIs are largely unavailable to a live world.** Anthropic, OpenAI, Google, and Alibaba all offer ~50% batch discounts, but with turnarounds up to 24 hours. That is unusable for canonical cognition. It **is** usable, and should be used, for: shadow-world experiments, kernel ensembles, offline Tier D analysis, memory consolidation jobs, and model-admission suites. Those are exactly the workloads [`09`](09-validation-and-experiments.md) says will run in the thousands, so the saving is real — just not on the canonical path.

**Finding 4 — the accelerated experiments, not the canonical world, are the budget risk.** [`09`](09-validation-and-experiments.md) calls for "dozens/hundreds of multi-season runs with bounded LLM use." A single 100-simulated-day run at the central rate costs ~$57 in the mixed configuration; 200 such runs is ~$11,400 — an order of magnitude above a year of canonical operation. **The experiment budget needs its own hard cap and its own approval, and should default to the cheapest tier plus batch pricing.** The existing budget hierarchy lists a "shadow-world/experiment cap" but does not flag that it is the larger number.

## 5. Structured output: constrained decoding is uneven, so local validity is mandatory

[`04`](04-agents-cognition-and-memory.md) requires every model output to validate against a versioned schema, and [`08`](08-models-cost-operations-security.md)'s admission suite makes schema compliance the first gate. Strict schema-constrained decoding is uneven across providers. That does not make lower-cost models unusable: tool calls plus local validation, repair, and escalation can satisfy the transport contract. Strict JSON is also not semantic validity—a perfectly shaped command may still be irrational or infeasible.

| Provider | Strict JSON-Schema guarantee | Notes |
|---|---|---|
| OpenAI | **Yes** | `additionalProperties: false` required; all fields required; recursion supported |
| Anthropic | **Yes** | No recursive schemas; no numeric/length constraints |
| Google Gemini | **Yes** (structural) | Supports recursion and numeric bounds |
| DeepSeek | **No** — best-effort JSON mode only | Docs warn output may be empty |
| Qwen | **No** — best-effort JSON mode only | |
| **MiniMax** | **No** — undocumented, open feature requests | Tool calling works; `response_format` unsupported |

This constrains rather than eliminates MiniMax for routine cognition. **“OpenAI-compatible” does not imply `response_format` compatibility.** MiniMax’s current OpenAI-compatible documentation lists tools but not structured-response formatting, so conformance must be measured through tool-call framing and local validation before admission.

Note that Agentopia hit exactly this wall and solved it the same way we should: **Qwen for volume, Gemini Flash as a fallback for invalid outputs.** That is independent confirmation of the design.

**Required architecture — the validity ladder.** Every Tier B/C call resolves through:

1. **Constrained decoding** where the provider supports it.
2. Otherwise **tool-call framing with a strict schema**, which is better supported than `response_format` on most OpenAI-compatible endpoints.
3. **Local validation** against the versioned schema — always, regardless of provider claims.
4. **One repair attempt** on the same model with the validation error appended.
5. **Escalation to a schema-guaranteed model** (Gemini Flash-Lite or gpt-5-nano) for the repair, not a retry on the same model. This is the Agentopia pattern and it is cheap: it only fires on failures.
6. **Deterministic Tier A fallback**, recorded as a `DecisionResolved` event with `resolution: fallback` per [`14`](14-determinism-replay-and-state-integrity.md).

Track **schema-failure rate per model per decision type** as an admission criterion and an ongoing metric. A model whose failure rate rises after a silent provider update is quarantined.

## 6. Model refusal is an unhandled failure mode with emergence consequences

Not addressed anywhere in the prior plan. December asks models to act as residents who may raid, steal, deceive, threaten, withhold food from rivals, and make reproductive decisions. Commercial models sometimes decline such requests, break character to comment as an assistant, or soften an action.

This is worse than a nuisance — **it is a systematic bias that silently invalidates emergence claims.** If a provider's safety layer makes agents reluctant to escalate conflict, December will report that "peaceful institutions emerged from material conditions" when the true cause was reinforcement learning at the provider. The [`09`](09-validation-and-experiments.md) emergence audit asks whether any prompt contained the outcome label beforehand; it must also ask whether the *model* declined the alternative.

Required:

1. **A refusal-rate benchmark in the model admission suite** ([`08`](08-models-cost-operations-security.md)), covering the full action grammar including conflict, deception, theft, and household formation, framed as the analytical simulation content it is.
2. **Refusals are a first-class failure class**, logged distinctly from schema failures and timeouts, and surfaced as an operational metric.
3. **Per-model refusal profiles are part of the model profile record**, because a model swap that changes refusal behavior is a behavioral intervention on the world and must be recorded as such under the change-management rules in [`08`](08-models-cost-operations-security.md).
4. **Refusal rates are reported alongside any conflict-frequency finding.** A conflict statistic without its refusal denominator is uninterpretable.
5. Prefer models with **steerable, documented behavior over the December action grammar** even at a price premium, and prefer open-weight models where refusal behavior can be measured stably over time.

## 7. Storage and retention costs

[`14`](14-determinism-replay-and-state-integrity.md) estimates 40–150 GB per real year of event log at the unattended pace under the batched-event policy, plus 1–5 MB per simulated day of prompt/response cache — which is canonical and must be backed up. At 2,190 simulated days/month that cache alone is roughly **26–130 GB/year**.

Total canonical artifact growth: **order 100–300 GB per real year**, replicated. This is affordable on local disk and cheap in object storage, but it is not zero, and the monthly restore drill in [`08`](08-models-cost-operations-security.md) must be timed against these volumes rather than against an empty database.

## 7a. The actual budget: $2,000 MiniMax + $1,000 OpenRouter

The owner holds **$2,000 in MiniMax credits and $1,000 in OpenRouter credits**. This is now the real constraint, and it answers open question 1 in [`11`](11-risks-decisions-open-questions.md) for the pre-revenue phase.

**The structure of these credits matters more than the total**, because the two pools are not interchangeable.

| | MiniMax $2,000 | OpenRouter $1,000 |
|---|---|---|
| Spendable on | MiniMax models only | ~any routed model |
| Strict JSON-schema decoding | **No** — undocumented, open feature requests | **Yes**, via Gemini / OpenAI models |
| Prompt-cache TTL | **5 minutes** — the shortest of any provider | Varies by routed model |
| Cache read | $0.06/M vs $0.30/M input — a **5× saving** | Varies |
| Batch discount | **None** | **None** |
| Model diversity | One family | Many families |

Three consequences follow directly.

**The pools are complementary by necessity, not merely by price.** MiniMax cannot guarantee schema-valid output, so if it carries Tier B volume, the validity ladder in §5 is load-bearing from the first day of Phase 2 and its **escalation target must live on OpenRouter**. Conversely, OpenRouter is the only pool that can supply schema guarantees, Tier C reasoning, and the multi-family model assignment that mitigates behavioural homogeneity (**R-31**). Spending OpenRouter credits on bulk Tier B traffic would waste their only unique properties.

**Neither pool offers a batch discount.** §4 Finding 3 recommended batch pricing for the ensemble programme; that 50% saving is **unavailable on these credits**. Ensembles either pay full rate here or run against a direct provider account that has a batch API.

**MiniMax's 5-minute TTL sits exactly where the token volume is.** Cache-aware activation batching (§4 Finding 2) therefore becomes more important under this budget, not less — a hit is 5× cheaper than a miss on the dominant cost line.

### What the credits buy

Recommended allocation — MiniMax carries volume, OpenRouter carries correctness and judgment:

| Component | Pool / model | $/sim-day |
|---|---|---:|
| Tier B, 150 calls (675 K in / 45 K out) | MiniMax M3 | 0.15 cached – 0.26 uncached |
| Director, 10 calls | MiniMax M3 | 0.04 |
| **MiniMax subtotal** | | **0.19 – 0.30** |
| Tier C, 18 calls (216 K in / 16 K out) | OpenRouter → Gemini 3.5 Flash-Lite | 0.11 |
| Schema repair escalation | OpenRouter → gpt-5-nano | fires only on failure |
| **Combined** | | **≈ 0.30 – 0.41** |

**Horizon: roughly 8,000 simulated days — about 22 simulated years — with both pools exhausting at approximately the same time.** The MiniMax pool alone yields ~6,700–10,500 sim-days; matching that with $1,000 of OpenRouter requires Tier C to stay near **$0.125/sim-day**, which Gemini 3.5 Flash-Lite ($0.105) hits almost exactly.

That balance is fragile in one direction. Tier C alternatives at $1,000:

| Tier C model | $/sim-day | Sim-days from $1,000 | Outcome |
|---|---:|---:|---|
| gpt-5-nano | 0.02 | ~58,000 | OpenRouter never binds; weakest deliberation |
| **Gemini 3.5 Flash-Lite** | **0.11** | **~9,500** | **Balanced — both pools end together** |
| Claude Haiku 4.5 | 0.30 | ~3,400 | OpenRouter dies first, ~$1,200 MiniMax stranded |
| Claude Sonnet 5 | 0.89 | ~1,100 | OpenRouter dies at 3 sim-years, ~$1,750 stranded |

Choosing a Sonnet-class Tier C spends the OpenRouter pool seven times faster than the MiniMax pool and strands most of the larger credit. This is §4 Finding 1 restated in cash: **the Tier C model is the budget.**

### What 22 simulated years is, and is not

At the two documented paces: **~11 real months** attended (24 sim-days/real-day), or **~3.7 real months** unattended (72 sim-days/real-day).

Demographically it is **exactly one generational transition**. Founders age 22 years; children born at t=0 reach the ethnographic age at first birth (~19.7) just before the credits run out. That is enough to watch the kinship constraint in [`15`](15-parameter-registry.md) §C arrive and force a response — the exogamy-institution question in [`05`](05-society-economy-governance-conflict.md) becomes live and testable. It is **not** enough for deep multigenerational history, inherited institutions across several generations, or the long ecological trends in [`03`](03-world-model-and-scenario.md).

### The allocation conflict the owner must resolve

§4 Finding 4 warned that the experiment programme, not the canonical world, is the larger budget line. Under these credits that is now concrete:

- A canonical world to one generational transition: **~8,000 sim-days — the entire pool.**
- The ensemble programme in [`09`](09-validation-and-experiments.md) ("dozens/hundreds of multi-season runs"): 200 runs × 100 sim-days = **20,000 sim-days — 2.5× the entire pool**, with no batch discount available.

**These credits cannot fund both.** The choice is a research-programme decision, not an accounting one, and it belongs with the claims ladder in [`18`](18-lab-charter-and-research-program.md): a registered cohort study with controls is the scientific artifact, while a long canonical exhibit is the demonstration. Pass 2's separation of exhibit from cohort (**P2-F12**) is what makes the trade-off visible.

Recommended split, pending the owner's decision:

1. **Reserve ~$500 of OpenRouter** for model admission, refusal benchmarking, homogeneity testing, and schema-failure measurement across families. These are prerequisites to trusting anything else and they are cheap.
2. **Spend MiniMax on Phase 2–3 development traffic**, where volume is high, stakes are low, and schema failures are informative rather than costly.
3. **Do not start a long canonical run until Gate 3**, when measured activation counts replace §1's estimates. Starting early burns the pool on a world whose cost model is still an estimate.

Phase 1 requires **no LLM spend at all** — the headless kernel has no cognition — so the credits remain untouched through the longest build phase and are not at risk from the schedule.

### Uncertainty

§1's activation model carries ±2× on both activation rate and context size, so the honest envelope on the 8,000-day figure is roughly **2,000–32,000 simulated days**. Every number here is planning arithmetic over an unmeasured workload; Gate 2 replaces it with measurement. Track spend per simulated day from the first cognition call.

## 8. Recommended budget posture

1. **Set the monthly cap before Phase 1**, as [`11`](11-risks-decisions-open-questions.md) already requires. This document supplies a scenario—not a forecast: roughly **$50–$1,300/month** under current assumptions, with wider contingency until the four-resident prototype measures real behavior.
2. **Budget at the official current price plus contingency**, and model known context-tier step changes.
3. **Separate and cap the experiment budget**, which is likely the larger number.
4. **Instrument cost per simulated day as a first-class metric** with an alert on trend, not just on absolute spend. Input-token growth per simulated day is the early warning that context assembly is regressing.
5. **Re-derive this entire document at Gate 1** with measured activation counts and context sizes replacing the estimates in §1. Everything here is an estimate whose purpose is to make the risk tractable, not to be right.
