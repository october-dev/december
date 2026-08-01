# 13 — Sources and Research Notes

**Research snapshot:** 2026-08-01. Every URL below was fetched and checked during the audit pass on that date unless marked otherwise. Repository activity, prices, APIs, and licenses change; verify again at implementation.

Sources below informed architecture and mechanism selection. **Inclusion is not endorsement**, and is not evidence that a model is valid for December.

## How to read the license column

The licensing question in [`11`](11-risks-decisions-open-questions.md) — "permissive-only code reuse versus GPL-compatible project" — can now be answered from evidence. See [Licensing consequences](#licensing-consequences) at the end of this page.

## Long-horizon generative societies

- [Agentopia repository](https://github.com/Neph0s/Agentopia) — long-horizon multi-agent simulation; Plan→Contact→Activity→Review, self-managed memory, append-only JSONL records, checkpoint resume. **License caveat: the README states MIT but the repository contains no LICENSE file**, so GitHub reports it as unlicensed. Treat as legally unlicensed for reuse purposes. Also note the repository is three commits deep, all dated 2026-06-05; the headline experiment is a paper claim, not something reproducible from the four files present.
- [Agentopia paper](https://arxiv.org/abs/2606.07513) — "Agentopia: Long-Term Life Simulation and Learning in Agent Societies," Xintao Wang et al., 2026-06-05. **Source of the token figures used in [`16`](16-cost-model-and-model-selection.md)**: Table 4 reports 13,347 M input tokens, 352 M output tokens, and 567 K LLM calls, as **averages across three simulated worlds** (per-run input ranged 9,699–19,041 M), for 100 agents over 10 simulated years in ~186 wall-clock hours. The models used were Qwen3.5-397B with Gemini 3 Flash as a fallback for invalid outputs. Very recent; treat replication maturity cautiously.
- [Generative Agents paper](https://arxiv.org/abs/2304.03442) — Park et al. Foundational memory-stream, reflection, planning, and believability evaluation. 25 agents.
- [Concordia repository](https://github.com/google-deepmind/concordia) — Apache-2.0, actively maintained. Configurable generative social simulation with a Game Master entity and modular components.
- [AI Town repository](https://github.com/a16z-infra/ai-town) — MIT, maintained. Convex/React/PixiJS browser town; product and UI reference only.
- [MiroFish repository](https://github.com/666ghj/MiroFish) — **AGPL-3.0**, very active. Self-described as a "swarm intelligence engine" for prediction rather than a social-simulation framework; the seed-material → parallel simulation → report-generation workflow is as described. **The AGPL obligation is materially stronger than any other repository on this page and extends to network use** — do not vendor code from it without a deliberate licensing decision.
- [Project Sid repository](https://github.com/altera-al/project-sid) — **contains no code.** It is a technical-report PDF, README, image, and video, with no license and no pushes since 2024-11-04. The PIANO architecture is described only in the [paper](https://arxiv.org/abs/2411.00114). Useful as a claim landscape; it is not an implementation reference.
- [AI Agents Alone Are Not (Yet) Sufficient for Social Simulation](https://arxiv.org/abs/2603.00113) — Yiming Li & Dacheng Tao. Argues role-play plausibility is not behavioral validity and proposes an environment-involved formulation. Direct support for December's kernel-owns-truth stance.
- [MemFail](https://arxiv.org/abs/2605.26667) — "MemFail: Stress-Testing Failure Modes of LLM Memory Systems," Garg et al., 2026-05-26. **Correction to earlier drafts:** its taxonomy is *summary failure, storage failure, retrieval failure, and reasoning failure*, evaluated over five adversarial datasets. Earlier drafts of this wiki attributed to it a different list ("fabricated recall, over-compression, source confusion, self-reinforcing summaries") which is our paraphrase, not the paper's. [`04`](04-agents-cognition-and-memory.md) has been corrected to use the paper's actual categories.

## Personal identity, agent continuity, and consciousness boundaries

- [Stanford Encyclopedia of Philosophy: Personal Identity](https://plato.stanford.edu/entries/identity-personal/) — distinguishes characterization, persistence, psychological-continuity, bodily/animalist, and fission problems. Essential warning that copying psychological state does not settle numerical identity.
- [Agent Identity Evals](https://arxiv.org/abs/2507.17257) — a statistical framework for measuring long-horizon agent identity, perturbation recovery, persistence, and consistency. Relevant to Track A in [`18`](18-lab-charter-and-research-program.md); identity scores remain operational measures, not consciousness tests.
- [Time, Identity and Consciousness in Language Model Agents](https://ojs.aaai.org/index.php/AAAI-SS/article/view/42561) — conservative persistence measures from instrumented scaffold traces and a distinction between apparent and architecturally grounded identity.
- [Consciousness in Artificial Intelligence: Insights from the Science of Consciousness](https://arxiv.org/abs/2308.08708) — derives computational indicator properties from several consciousness theories. Indicators are theory-dependent evidence, not a proof of consciousness.
- [Principles for Responsible AI Consciousness Research](https://arxiv.org/abs/2501.07290) — argues for organizational policies, responsible objectives, ethics, and careful public communication under uncertainty. This supports ADR-009’s claims ladder and human-subject boundary.
- [Whole Brain Emulation: A Roadmap](https://ora.ox.ac.uk/objects/uuid%3Aa6880196-34c7-47a0-80f1-74d32ab98788) — illustrates how much neuroanatomical acquisition, emulation, validation, and philosophical work separates a behavioral persona from whole-brain emulation. December is not a WBE project.

## Embodied worlds and construction

- [Mindcraft repository](https://github.com/mindcraft-bots/mindcraft) — MIT, active. Minecraft/Mineflayer LLM agents; providers include OpenRouter. **The repository moved**: the widely cited `kolbytn/mindcraft` now redirects here. Code execution via `allow_insecure_coding` must remain disabled — see [ADR-005](adr/005-no-arbitrary-agent-code.md). A separate community fork, `mindcraft-ce/mindcraft-ce`, is more recently active but is not canonical.
- [Mineflayer repository](https://github.com/PrismarineJS/mineflayer) — MIT, very active. The Minecraft bot API underlying Mindcraft.
- [Craftium repository](https://github.com/mikelma/craftium) — **LGPL-2.1-or-later for code plus CC BY-SA 3.0 for media**, inherited from Luanti. Not MIT — earlier drafts implied a permissive license and were wrong. Gymnasium and PettingZoo APIs, with explicit client/server synchronization for slow agents such as LLMs. Published at **ICML 2025** ([paper](https://arxiv.org/abs/2407.03969)), so it is no longer merely an early experiment — but development has slowed, with no pushes since 2026-02-17.
- [Luanti repository](https://github.com/luanti-org/luanti) — **LGPL-2.1-or-later** code, CC BY-SA 3.0 media with several exceptions. Formerly Minetest. Very active.
- [MineLand paper](https://arxiv.org/abs/2403.19267) — multi-agent Minecraft simulator with limited senses and physical needs.
- [VillagerAgent paper](https://arxiv.org/abs/2406.05720) — DAG-based task decomposition and coordination; **Findings of ACL 2024**.
- [APT paper](https://arxiv.org/abs/2411.17255) — text-to-blueprint architectural planning. arXiv preprint, no venue listed.

## Governance and social dilemmas

- [GovSim repository](https://github.com/giorgiopiatti/GovSim) and [paper](https://arxiv.org/abs/2404.16698) — **this is the correct citation.** "Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents," Piatti et al., NeurIPS 2024. MIT. Effectively a frozen research artifact (no pushes since 2025-01-19).
- [GovSimElect / AgentElect](https://github.com/rfaulkner/GovSimElect) — **correction to earlier drafts, which cited this as though it were an upstream project.** It is a five-star personal *fork* of GovSim that renames itself "AgentElect" in its own README, comparing elected-leader, fixed-leader, and leaderless governance over the GovSim fishery scenario. Cite it as a fork if the election variant is what is wanted; cite GovSim above for the underlying work.
- [Agent Ballot Box](https://github.com/Anna4142/agent-ballot-box) — MIT. **Weak citation, retained only for completeness:** zero stars, single author, no activity since 2025-06-22, and it is a GovSim-style commons framework (fisheries, pasture, pollution) in which voting is one component rather than the focus. Earlier drafts described it as "LLM voting experiments," which oversells it.
- [Melting Pot repository](https://github.com/google-deepmind/meltingpot) and [Melting Pot 2.0 paper](https://arxiv.org/abs/2211.13746) — Apache-2.0, active. **The "over 50 substrates / over 256 scenarios" figures come from the repository README and full report, not the paper abstract** — cite the repository for them. The README's own dilemma list is "cooperation, competition, deception, reciprocation, trust, stubbornness"; coalition-formation substrates exist but "coalitions" was our paraphrase.
- [Open Policy Agent documentation](https://www.openpolicyagent.org/docs) — Apache-2.0, CNCF graduated. Policy-as-code reference for infrastructure authorization; not a model of social law.

## Archaeology, subsistence, and demography

- [MoralAgentSim](https://moralagentsim.github.io/) and [paper](https://arxiv.org/abs/2509.17703) — "Why Are We Moral? An LLM-based Agent Simulation Approach to Study Moral Evolution," Zhou et al., **ACL 2026 Main (oral)**. The "MoRE" architecture in a prehistoric hunter-gatherer environment with hunting, gathering, sharing, communication, reproduction, and conflict. The closest published analogue to December's cognition-in-a-subsistence-world premise; assess independently.
- [AgModel at CoMSES](https://www.comses.net/codebases/581b8bfa-064f-4af8-9dc3-be939202e9c7/releases/1.0.0/) — Isaac Ullah, v1.0.0, 2024-12-06. **GPL-2.0.** Forager–farmer transition with demography, environment, subsistence, labor, stores, births, and deaths. Parameter and mechanism reference.
- [Agent-Based Modeling for Archaeology](https://santafeinstitute.github.io/ABMA/) — Romanowska, Wren & Crabtree, SFI Press. **CC BY-SA 4.0.** Ten chapters with NetLogo code covering subsistence, population, fission–fusion, commons, and games.
- [Simulating Forager Mobility](https://www.cherscience.org/simulating-forager-mobility-project) — NetLogo models for residential mobility, waterhole tethering, and logistical mobility.
- [Artificial Anasazi model](https://ccl.northwestern.edu/netlogo/models/ArtificialAnasazi) — **both cautions confirmed verbatim on the page**: "This model is unverified. It has not yet been tested and polished as thoroughly as our other models," and "environmental variability alone can not explain the population collapse around 1350." Use as a cautionary case, never as historical ground truth.
- [Lewis et al. 2014, high mobility and demand sharing](https://pmc.ncbi.nlm.nih.gov/articles/PMC4284614/) — *Nature Communications* 5:5789. Hunting, movement, sharing, reproduction, aging, and enforced cooperation in egalitarian hunter-gatherers.

Demographic and energetic anchors are consolidated in [`15`](15-parameter-registry.md), which flags which values were verified in this pass and which still require URL confirmation.

## Disease, ecology, and hazards

The disease literature was researched in depth during this audit because it materially changed the design. Full treatment and design consequences are in [`15`](15-parameter-registry.md) §D.

- [Bartlett 1957](https://rss.onlinelibrary.wiley.com/doi/10.2307/2342553) and [Bartlett 1960](https://rss.onlinelibrary.wiley.com/doi/abs/10.2307/2343186) — origin of critical community size; measles CCS 250,000–300,000.
- [Black 1966](https://pubmed.ncbi.nlm.nih.gov/5965486/) — island study; CCS 300,000–500,000, with transmission breaks in every community below 500,000.
- [Keeling & Grenfell 1997](https://www.science.org/doi/10.1126/science.275.5296.65) — shows realistic infectious-period distributions reproduce the observed CCS, giving the empirical result a mechanistic basis.
- [Black 1975, Infectious Diseases in Primitive Societies](https://www.science.org/doi/10.1126/science.163483) — serosurveys of isolated Amazonian groups; chronic and latent infections are endemic, acute infections die out after introduction.
- [Wolfe, Dunavan & Diamond 2007](https://www.nature.com/articles/nature05775) — five-stage animal-to-human pathogen model; crowd diseases require "at least several hundred thousand people."
- [Amazonian contact epidemics, 1875–2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC4564847/) — 117 epidemics across 59 societies; median mortality 18%, range <1–97%, median affected population 180. **The closest empirical analogue to December's scale.**
- [Faroe Islands 1846](https://hekint.org/2021/08/18/peter-panum-and-the-geography-of-disease/) — Panum's virgin-soil measles study; 77.5% attack rate, 2.8% CFR, lifelong immunity demonstrated over 65 years.
- [Tristan da Cunha respiratory epidemics](https://pmc.ncbi.nlm.nih.gov/articles/PMC2130889/) — a ~300-person community; every epidemic ship-initiated, and a three-week passage was enough for the virus to die out en route.
- [Stochastic fade-out in branching processes](https://pmc.ncbi.nlm.nih.gov/articles/PMC2872325/) — branching-process basis for early fade-out probability. It is intuition for ensemble behavior, not proof that an 18-person outbreak must fall into exactly two final-size bins.
- [Delamater et al. 2019, complexity of R₀](https://wwwnc.cdc.gov/eid/article/25/1/17-1901_article) — R₀ is a function of social organization, not a pathogen constant; measles estimates span 3.7–203.3.
- [Caulfield et al. 2004](https://pubmed.ncbi.nlm.nih.gov/15213048/) — undernutrition attributable fractions for child mortality, 44.8% (measles) to 60.7% (diarrhea). The quantitative basis for coupling December's subsistence and health modules.
- [Covasim](https://covasim.org/) and [methods paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC8341708/) — MIT. **The repository has moved to `starsimhub/covasim`.** Adapt architecture and testing discipline, never COVID parameters.
- [OpenABM-Covid19 paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC8328312/) — individual contact networks and extensive test categories.
- [ForeFire documentation](https://forefire.readthedocs.io/en/latest/) — **GPL-3.0**. Wildfire fuel/landscape/spread concepts; far more detailed than v1 needs.

## Agent-based-model engineering and validation

- [Mesa documentation](https://mesa.readthedocs.io/stable/) — Apache-2.0. **Current stable is 3.5.1 (2026-03-15), with a 4.0 line in alpha.** Correction to earlier drafts: discrete-event and hybrid step+event scheduling are now **stable, not experimental** — `model.schedule_event()`, `model.schedule_recurring()`, `run_for`, `run_until`. The `mesa.experimental.devs` simulators (`Simulator`, `ABMSimulator`, `DEVSimulator`) are **deprecated since 3.5.0 and removed in the 4.0 line**, so any design targeting them is already stale. Note also that `mesa.space` is maintenance-only and SolaraViz carries breaking-change risk across minor releases — both argue for the narrow `SimulationRuntime` interface in [`02`](02-research-landscape.md).
- [ODD protocol resource](https://www.ufz.de/index.php?en=40429) and [ODD 2020 update](https://www.jasss.org/23/2/7.html) — Grimm et al., JASSS 23(2):7, DOI 10.18564/jasss.4259.
- USGS overview of the ODD second update — indexed at `usgs.gov/publications/odd-protocol-describing-agent-based-and-other-simulation-models-a-second-update` but **fetch-blocked during this audit**; the [pubs.usgs.gov record 70209554](https://pubs.usgs.gov/publication/70209554) also returns 403. Use the JASSS version above as the citable source.
- [Azure event-sourcing pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) — general event-store, replay, and projection tradeoffs. **Insufficient on its own**: it does not cover the commit-ordering hazard that [`14`](14-determinism-replay-and-state-integrity.md) §D7 addresses.

## Determinism, state integrity, and replay

Added by this audit pass; these underpin [`14`](14-determinism-replay-and-state-integrity.md).

- [glibc, Errors in Math Functions](https://sourceware.org/glibc/manual/latest/html_node/Errors-in-Math-Functions.html) — glibc explicitly does not aim for correctly rounded transcendentals. The single clearest reason portable bit-identity is unavailable by default.
- [CORE-MATH project](https://core-math.gitlabpages.inria.fr/) and [LLVM libc math](https://libc.llvm.org/math/) — correctly-rounded implementations, partially upstreamed into glibc 2.42/2.43.
- [NumPy random compatibility policy](https://numpy.org/doc/stable/reference/random/compatibility.html) and [NEP 19](https://numpy.org/neps/nep-0019-rng-policy.html) — streams are guaranteed only for the same build, environment, and machine; distribution methods may change in minor releases.
- [NumPy SIMD build options](https://numpy.org/doc/stable/reference/simd/build-options.html) and [global state](https://numpy.org/doc/stable/reference/global_state.html) — runtime CPU dispatch and how to pin it.
- [Gaffer on Games, floating point determinism](https://gafferongames.com/post/floating_point_determinism/) and [deterministic lockstep](https://gafferongames.com/post/deterministic_lockstep/) — the practitioner literature on cross-platform determinism and turn buffering.
- [1500 Archers on a 28.8](https://www.gamedeveloper.com/programming/1500-archers-on-a-28-8-network-programming-in-age-of-empires-and-beyond) — the original decision-barrier pattern, twenty-five years before December needed it.
- [Ordering in the Postgres outbox](https://event-driven.io/en/ordering_in_postgres_outbox/) — Oskar Dudycz's write-up of the sequence-gap race that silently loses events.
- [postgresql-event-sourcing](https://github.com/eugene-khyst/postgresql-event-sourcing) — a snapshot-fencing reference. December does not treat `xid8` ordering as commit ordering and does not require this mechanism in Phase 1.
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) and [information functions](https://www.postgresql.org/docs/current/functions-info.html).
- [Postgres LISTEN/NOTIFY does not scale](https://www.recall.ai/blog/postgres-listen-notify-does-not-scale) — the global commit lock, with measurements; and a [counterpoint with its own measurements](https://www.dbos.dev/blog/postgres-listen-notify-scalability).
- [Homomorphic hashing (Meta)](https://engineering.fb.com/2019/03/01/security/homomorphic-hashing/) and [Lewi et al., LtHash](https://eprint.iacr.org/2019/227.pdf) — incremental set hashing.
- [Solana SIMD-0215, accounts lattice hash](https://github.com/solana-foundation/solana-improvement-documents/blob/main/proposals/0215-accounts-lattice-hash.md) — LtHash applied to a very large mutable entity set, per block. Evidence the approach scales far past December's needs.
- [EIP-7864, unified binary state tree](https://eips.ethereum.org/EIPS/eip-7864) — why to prefer binary hash trees over verkle.
- [FoundationDB simulation testing](https://apple.github.io/foundationdb/testing.html) and [TigerBeetle VOPR](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/internals/vopr.md) — deterministic simulation of nondeterministic systems.
- [Random123 / Philox](https://www.thesalmons.org/john/random123/papers/random123sc11.pdf) and [JAX PRNG design](https://docs.jax.dev/en/latest/jep/263-prng.html) — counter-based and splittable RNG.
- [Python PYTHONHASHSEED](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED) and [What's New in Python 3.14](https://docs.python.org/3/whatsnew/3.14.html) — hash randomization, and free-threading support (PEP 779) as of 3.14.

## Open-source strategy and economy references

- [0 A.D.](https://play0ad.com/game-info/project-overview/) — **GPL code, CC BY-SA 3.0 art.** Latest is Release 28 "Boiorix" (2026-02-18); the project dropped "Alpha" branding at R28. Reference only; rejected as an authoritative base.
- [Widelands](https://github.com/widelands/widelands) and [unit documentation](https://www.widelands.org/documentation/autogen_toc_lua_tribes_units/) — **GPL-2.0**, actively maintained (v1.3.1, 2026-02-22). Worker/ware/building economy and moddable Lua unit definitions.
- [Unknown Horizons](https://unknown-horizons.org/about/) — **dormant, not maintained.** Correction to earlier drafts: the last release is `2019-dev` (2019-01-13); the classic game is Python/FIFE with no LICENSE file in the repository, and the Godot rewrite ([godot-port](https://github.com/unknown-horizons/godot-port), GPL-2.0) has no playable content and no release. "Python/Godot" conflates two separate codebases.
- [Freeciv](https://github.com/freeciv/freeciv) — **GPL-2.0**, very active (3.2.5, 2026-07-10). Ruleset and client/server architecture reference only.

## Model routing, telemetry, and provider facts

- [LiteLLM repository](https://github.com/BerriAI/litellm) — **MIT with a proprietary `enterprise/` carve-out** (GitHub reports NOASSERTION). Very active. Now describes itself as a Rust core with a Python SDK.
- [Langfuse](https://langfuse.com/docs/observability/overview) — **MIT Expat with proprietary `ee/` carve-outs.** Open-core; cite the LICENSE file, not the docs page, for any licensing claim.
- [MiniMax pay-as-you-go pricing](https://platform.minimax.io/docs/guides/pricing-paygo) — **M3 is the current flagship (1 M context); M2.5 is legacy.** The page labels the $0.30/$1.20 ≤512 K rate “Permanent 50% off”; the >512 K tier is $0.60/$2.40. Audit pass 1 incorrectly described the reduction as temporary.
- [MiniMax OpenAI-compatible API](https://platform.minimax.io/docs/api-reference/text-openai-api) — tool calling and streaming work; `presence_penalty`, `frequency_penalty`, and `logit_bias` are silently ignored; `n` supports only 1. **JSON-schema structured output is not supported** and is the subject of open feature requests. MiniMax also offers an [Anthropic-compatible endpoint with explicit prompt caching](https://platform.minimax.io/docs/api-reference/anthropic-api-compatible-cache) (5-minute TTL).
- [OpenRouter provisioning API keys](https://openrouter.ai/docs/features/provisioning-api-keys) — **corrected URL**; the previously cited path 404s. Per-key credit limits with optional daily reset are confirmed.
- [OpenAI GPT-5.6 announcement and pricing](https://openai.com/index/gpt-5-6/) — as of 2026-08-01: Sol $5/$30, Terra $2.50/$15, Luna $1/$6 per million input/output tokens. Audit pass 1 incorrectly assigned Luna $0.20/$1.20. Also see [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching), [batch API](https://developers.openai.com/api/docs/guides/batch), and [structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs).
- [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing), [batch API](https://ai.google.dev/gemini-api/docs/batch-api), [structured output](https://ai.google.dev/gemini-api/docs/structured-output).
- [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing), [KV cache](https://api-docs.deepseek.com/guides/kv_cache), [JSON mode](https://api-docs.deepseek.com/guides/json_mode) — automatic multi-hour disk caching at roughly 0.02× read cost is the strongest caching economics available, and best-effort JSON only.
- [OpenAI reproducible outputs cookbook](https://cookbook.openai.com/examples/reproducible_outputs_with_the_seed_parameter) — `seed` is explicitly best-effort. **No provider guarantees deterministic sampling**; Anthropic's newest models remove `temperature` and `top_p` entirely. This is why [`14`](14-determinism-replay-and-state-integrity.md) makes the response cache canonical.

## Licensing consequences

Evidence now supports a concrete answer to the open licensing question in [`11`](11-risks-decisions-open-questions.md):

| If December is… | Then these are usable | And these are not |
|---|---|---|
| **Permissive-first project** | Mesa (Apache-2.0), Melting Pot (Apache-2.0), Concordia (Apache-2.0), GovSim (MIT), Mineflayer/Mindcraft (MIT), Covasim (MIT), OPA (Apache-2.0), permitted open-core portions after file-level review | LGPL/GPL/AGPL code requires deliberate integration and distribution/network-use analysis; it is not categorically unusable |
| **Reciprocal-license-compatible project** | May incorporate more LGPL/GPL components while satisfying their terms | AGPL and mixed-media licenses still require specific review, especially for a network service |

Three practical notes:

1. **The 3D adapter decision at Gate 6 is also a licensing decision.** Craftium and Luanti are LGPL-2.1-or-later with CC BY-SA media. Dynamic linking and process separation keep LGPL obligations manageable, and December's adapter contract in [`06`](06-architecture-and-data.md) already implies process separation — but this must be a deliberate, recorded choice rather than a discovery made at integration time.
2. **Reading a GPL model for mechanism inspiration is not reuse.** AgModel and the archaeology ABMs are parameter and mechanism references; that use is unaffected by their license. Only copied code creates an obligation. Record which is which in the parameter registry.
3. **Do not treat this table as legal advice.** MiroFish’s AGPL is especially relevant to network deployment, but LGPL linking, GPL distribution, assets, open-core carve-outs, and combined works all need project-specific review.

## Source-quality rules for implementation

1. Prefer primary papers, official documentation, official repositories, and maintained model registries.
2. Record version, commit, date, and license for any code or parameter reuse.
3. Do not transfer a parameter outside its population, environment, or domain without stating the justification.
4. Triangulate important numerical values across multiple sources, or carry a broad uncertainty range.
5. Separate mechanism inspiration from empirical calibration.
6. Mark unverified models and very recent papers explicitly.
7. Preserve a bibliography entry beside every parameter family in the registry.
8. **Verify that a cited repository is the upstream project and not a fork**, and that a claimed license is backed by a LICENSE file rather than a README sentence. This audit found errors of both kinds.
