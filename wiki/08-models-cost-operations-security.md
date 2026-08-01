# 08 — Models, Cost, Operations, and Security

## Provider strategy

The user has balances across MiniMax, OpenRouter, and potentially other providers. The system should treat providers as interchangeable capacity behind tested model profiles.

Each approved model profile records:

- provider/model/version and endpoint mode;
- supported structured output/tool behavior;
- context/output limits;
- observed latency and failure rates;
- benchmark scores for December action schemas;
- token accounting and price snapshot date;
- allowed cognitive tiers and fallback order;
- data-retention/privacy notes;
- prompt template and conformance-suite version.

Each profile also records **prompt-cache TTL and pricing**, **structured-output capability**, and **measured refusal rate over the December action grammar**. All three turned out to be first-rank selection criteria; see [`16`](16-cost-model-and-model-selection.md).

MiniMax offers an OpenAI-compatible endpoint, and OpenRouter exposes many providers behind one API. A gateway should normalize calls while preserving provider-specific telemetry. **The gateway abstraction must not assume all “OpenAI-compatible” behavior is identical — and this is not a hypothetical caution.** MiniMax's compatibility layer silently ignores `presence_penalty`, `frequency_penalty`, and `logit_bias`, supports only `n=1`, and **does not support JSON-schema structured output at all**. Compatibility covers tool calling and streaming, not constrained decoding. Any design that assumes schema-guaranteed output from a cheap OpenAI-compatible endpoint is wrong; use the validity ladder in [`16`](16-cost-model-and-model-selection.md) §5.

## Model admission suite

Before a model can affect the canonical world it must pass:

1. schema compliance and repair behavior;
2. stable identity/values across context variations;
3. private-information canary tests, **including probes of the rejection/feasible-alternative channel**;
4. feasible action selection with adversarial distractors;
5. source-aware memory use and rumor distinction;
6. tool/command prompt-injection resistance;
7. negotiation, election, resource, and emergency scenarios;
8. verbosity/token limits;
9. retry/idempotency behavior **at the `decision_id` level**, including divergent output on retry;
10. drift comparison against the previous approved version;
11. **refusal-rate benchmark over the full action grammar**, including conflict, deception, theft, coercion, and household formation — a model that declines these imposes a silent behavioral bias on the world ([`16`](16-cost-model-and-model-selection.md) §6);
12. **character-break rate** — how often the model comments as an assistant, references being an AI, or narrates from outside the resident's perspective;
13. **behavioral-diversity check** — two residents with materially different values and histories must not produce interchangeable decisions across a scenario battery.

Admission is per model version and prompt bundle. Silent provider upgrades trigger quarantine until re-tested when detectable.

## Cost model

The budget equation is:

```text
daily_cost = Σcalls(model, tier) ×
             (input_tokens × input_price +
              output_tokens × output_price +
              cache/storage/embedding costs)
```

The main risk is input growth, not output. Agentopia's published experiment — 13,347 M input tokens, 352 M output, 567 K calls, **averaged across three worlds**, for 100 agents over 10 simulated years — implies an input:output ratio near 38:1. That demonstrates feasibility at research scale and shows why December cannot resend biographies and histories naively.

**[`16`](16-cost-model-and-model-selection.md) supersedes this section for anything budget-bearing.** It builds the estimate bottom-up from activation counts rather than by rescaling someone else's workload, and its conclusions change several assumptions made elsewhere in this wiki:

- A realistic canonical world costs roughly **$50–$1,300 per month**, depending overwhelmingly on the Tier C model and the simulated pace.
- **Tier C is ~10% of calls and ~89% of cost.** The decision-significance threshold, not population size, is the primary cost lever.
- **Sparse activation and prompt caching are in direct conflict.** Cache TTLs are measured in minutes while activation is deliberately scattered; a miss costs ~10× a hit on a workload that is >90% input. The activation scheduler must batch for cache locality.
- **The accelerated experiment programme is the larger budget risk**, plausibly an order of magnitude above canonical operation, and needs its own cap and approval.
- The earlier "$4.4k" illustration has been withdrawn. It priced another project's workload at a rate for a different, now-legacy model and told us nothing about December. Current provider labels and prices are recorded in [`16`](16-cost-model-and-model-selection.md) and must be rechecked at procurement time.

## Human-data boundary

The terrarium uses fictional residents. It must not ingest identifiable life histories, private messages, recordings, family data, or third-party nominations. A future human-modeling track requires a separate protocol: first-party informed consent, independent ethics review appropriate to the jurisdiction and institution, data minimization, access controls, retention and deletion rules, withdrawal handling, risk disclosure, and an explicit ban on claiming that a model is or continues the participant. Public GitHub issues are not an acceptable intake channel for human-subject data.

## Budget hierarchy

Budget is set at several levels:

- monthly hard cap across providers;
- daily canonical cap;
- shadow-world/experiment cap;
- per-model and per-agent rolling allowance;
- maximum tokens per decision type;
- emergency reserve for high-significance events and recovery.

OpenRouter keys can have explicit credit limits. Provider-side limits are a second line of defense; the local gateway enforces tighter limits first.

## Graceful degradation

When a threshold is reached:

1. stop shadow worlds and nonessential summaries;
2. reduce reflection frequency and use cached summaries;
3. route routine cognition to cheaper approved models;
4. shorten deliberation contexts using deterministic retrieval budgets;
5. promote more routines to Tier A;
6. slow canonical simulated time at cognition barriers;
7. only if necessary, pause at a clean snapshot.

Never allow a budget failure to invent decisions, discard physical events, duplicate actions, or fast-forward through unresolved high-stakes choices.

## Token-saving mechanisms

- Stable identity/profile blocks cached by hash.
- Delta observations rather than full state.
- Structured ledgers queried on demand.
- Memory consolidation with source links.
- Small contexts assembled per task.
- Conversation episodes summarized only after retaining raw transcript.
- Group meetings use shared public context plus private overlays.
- One model call may propose a bounded plan whose routine steps execute without recalls.
- Batch low-significance appraisals if isolation/private context remains intact.
- Response cache for deterministic replay and scenario tests.

## Always-running operations

### Process supervision

- Container or service manager restarts crashed processes.
- Single canonical leader protected by database lease/fencing token.
- Workers use idempotency keys and at-least-once delivery safely.
- Health endpoints distinguish process, database, scheduler progress, provider, and replay health.
- Deployments drain at a snapshot/cognition barrier.

### Backups

- Continuous database WAL or equivalent plus daily full backup.
- Content-addressed artifacts replicated with checksums.
- Configuration, prompts, model profiles, code commit, and container digest included in a world manifest.
- Monthly restore drill into an isolated world, **timed against realistic volumes rather than an empty database**.
- Retention policy keeps canonical history indefinitely unless the user explicitly changes it. Expect the canonical artifact to grow on the order of **100–300 GB per real year** at the unattended pace ([`14`](14-determinism-replay-and-state-integrity.md) §D8, [`16`](16-cost-model-and-model-selection.md) §7). Cold-tier archival of old events is permitted with hashes retained online; deletion is not.
- **The prompt/response cache is canonical, not a cache.** Replay cannot reproduce history without it, because no provider offers reproducible sampling. It is backed up, versioned, and restored with the event log.

### Change management

The canonical world is not a dev database. Every change follows:

1. ADR/config proposal;
2. tests and accelerated ensembles;
3. replay of a recent canonical snapshot in staging;
4. schema compatibility and migration rehearsal;
5. explicit release manifest;
6. snapshot and deploy;
7. post-deploy replay/hash check.

Behavior-changing patches are historical interventions even if called bug fixes. Record them visibly.

## Observability

Metrics:

- simulation lag, next-event queue, events/tick, projection lag;
- LLM calls/tokens/cost/latency/error/schema repair by agent and decision type;
- cognition activation reasons and fallback rates;
- memory retrieval size, source mix, contradiction/leak flags;
- command acceptance/rejection and repeated-loop counts;
- resource invariants and reconciliation deltas;
- snapshot/replay durations and hash mismatches;
- population, health, stores, ecology, groups, institutions, conflict;
- significance/quiet-period diagnostics.

Every model trace links to world/branch, resident, decision, command, and resulting event IDs. Secrets and sensitive rationale are redacted from default traces.

## Security model

### Threats

- prompt injection through resident speech, public artifacts, imported scenario text, or tool output;
- **prompt injection targeting the director**, corrupting the observer-facing account while leaving world state intact;
- **cross-site scripting** from resident-authored text rendered in the observer UI;
- **hidden-state leakage through rejection reasons and feasible-alternative packets**;
- generated command exploiting parser ambiguity or excessive quantities;
- unrestricted code/shell execution;
- SSRF/network exfiltration through model-authored URLs;
- leaked API keys in prompts/logs/client bundles;
- duplicate commands after retries;
- observer UI accidentally writing canonical state;
- malicious package/model/provider output;
- save corruption or unauthorized rule/office grants.

### Controls

- No arbitrary code execution for residents. Mindcraft’s code-generation feature remains disabled if used.
- Residents receive an allowlisted typed action API only.
- Strict schemas, quantity/unit bounds, entity visibility, and capability validation.
- No direct filesystem, network, database, or model-provider credentials in agent tools.
- Server-side secret manager/environment injection; secrets redacted before trace storage.
- Egress deny-by-default for runtime workers except gateway/internal services.
- Separate credentials and write permissions by module.
- Content is always untrusted data; resident text cannot modify system/action definitions. **This applies to the director and the observer UI as much as to residents** — delimited untrusted data in the summarizer's context, citation-enforced factuality checking on its output, and output escaping in the UI.
- Rejection reasons and feasible alternatives pass the same visibility filter as observation packets.
- Idempotency, expected versions, rate limits, and audit log.
- Dependency locking, vulnerability scanning, signed release manifests when practical.

## Observer interventions

Default canonical mode is read-only. Administrative actions—pause, resume, change pace, rotate key, fix corrupt projection—are operational and logged. World interventions such as adding food, weather, people, or rules require:

- creating a fork, or
- explicitly switching to “experimental/god mode,” ending the prior canonical integrity claim.

There is no hidden intervention button.

## Privacy and retention

The world is fictional, but prompts may contain provider-visible generated content. Do not include real personal data. Store API request/response bodies encrypted at rest if feasible, restrict developer-private rationale, and make provider retention terms part of model admission. Public sharing should omit secrets, raw hidden rationales, and any imported copyrighted scenario text.
