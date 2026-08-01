# 07 — Time, Emergence, and Observation

## Multi-resolution time

A fixed “one turn per agent” loop is both expensive and unrealistic. December uses a hybrid event system.

### Timescales

| Scale | Typical processes |
|---|---|
| Seconds/minutes | encounter, speech, combat exchange, accident response |
| Hours | travel, work task, meeting, cooking, care, sleep |
| Days | physiology, spoilage, infection progression, weather effects, project progress |
| Seasons | crops, prey movement, stores, institutional terms, migration |
| Years | aging, fertility, soil trends, knowledge transmission, generational politics |

The scheduler jumps to the next meaningful event. Daily boundaries settle physiological and ecological flows; high-resolution episodes temporarily expand time.

## Sparse activation

An agent wakes for cognition when:

- a body threshold crosses;
- an activity completes/fails/is interrupted;
- relevant observable state changes;
- a message or meeting arrives;
- a commitment approaches;
- a project needs a decision;
- conflict or danger is detected;
- a periodic reflection interval arrives;
- a novelty/significance detector fires.

Otherwise the kernel continues routine actions and world processes. This is central to cost control and believable quiet.

## Concurrency

Residents choose based on the same state snapshot for a decision window, but commands are resolved under explicit rules:

- independent actions can commit concurrently;
- contested resources use reservation plus priority/tie policy known to the world;
- simultaneous social/physical encounters enter a joint resolution episode;
- losing a race returns a new observation, not a silent alternative;
- scheduler ordering is deterministic and documented.

**No resident gains priority from model-provider response order.** The kernel never consumes network arrival order. A tick emits decision requests carrying deterministic `decision_id`s; an orchestrator resolves them outside the kernel; accepted resolutions are durably recorded; and a decision window is ingested in stable order. Live wall-clock deadlines and retry budgets may determine whether a response is recorded, because an always-running service needs real failure policy. That operational fact becomes part of canonical history. Replay consumes the recorded resolution and never repeats the timeout race.

For low-significance routine choices, a deterministic resident-specific fallback may resolve the request. If a consequential or identity-defining decision has no admitted response, the world pauses at that cognition barrier rather than silently replacing the resident with a generic survival policy. Provider latency can affect wall-clock pace; it cannot decide which of two already-resolved commands wins.

**Sparse activation conflicts with prompt caching, and the scheduler must mediate.** Cache entries expire on wall-clock TTLs measured in minutes, while sparse activation deliberately scatters calls. Because input is over 90% of tokens and a cache miss costs roughly 10× a hit, the activation scheduler should **batch residents whose cognition falls due within a short window** so prefixes are reused inside their TTL. Cache hit rate per resident is a primary operational metric; see [`16`](16-cost-model-and-model-selection.md) §4.

## Canonical pace and catch-up

The world runs continuously under a wall-clock controller, but simulated time is authoritative. The controller may:

- pause on integrity failure and on unresolved high-significance cognition after the admitted fallback ladder is exhausted;
- slow down when a high-density interaction requires cognition;
- speed through sleep/quiet intervals within a maximum ratio;
- use resident-specific deterministic routines only for low-significance activity when model budget/provider availability is exhausted;
- never skip unresolved scheduled events.

If the process is offline for two real hours, default behavior is resume from the same simulated instant rather than fabricate catch-up. A separately enabled catch-up mode can safely advance only deterministic/background processes until a cognition barrier.

## What emergence means here

An outcome counts as emergent when it:

1. was not directly selected by a developer-authored event or summary prompt;
2. arises from interactions among at least two mechanisms or agents;
3. varies across seeds or policies;
4. remains explainable through recorded local transitions;
5. survives a basic anti-cheating audit for hidden global information or narrative mutation.

Novel dialogue alone is not sufficient. A new institution, settlement split, trade convention, alliance, irrigation regime, or famine cascade can qualify.

## Avoiding both boredom and manufactured drama

We do not add a director that creates events. We improve the possibility space:

- heterogeneous but plausible goals/values and asymmetric information;
- shared, rival, and threshold resources;
- lumpy projects requiring coordination;
- seasons and delayed consequences;
- incomplete contracts and ambiguous norms;
- exit, voice, deception, forgiveness, sanctions, and institutional choice;
- external groups and rare conditional hazards;
- irreversible life events and knowledge loss.

The observer UI turns quiet causality into legible interest with comparisons, trends, unresolved commitments, and causal explanations. It does not need explosions.

## Observer experience

### Home / “Since you left”

- simulated time elapsed and runtime health;
- 3–7 consequential changes ranked by a transparent significance score;
- population, stores, health, ecological pressure, conflict, and project deltas;
- new/changed institutions and officeholders;
- current high-risk causal chains (“seed grain below planting requirement”);
- links to evidence and replay.

### Live map

Shows terrain, weather, residents/activities, structures, crop/resource state, claims, and uncertainty appropriate to observer mode. Layers can display water, soil, fire, disease contacts, work, property, and social groups.

### Person page

Biography, body/needs, accessible inventory, skills, relationships, offices, current goals, commitments, personal timeline, directly observed knowledge, beliefs with confidence, and model/cost telemetry. Private thoughts are a developer-only toggle and clearly labeled as model output, not ground truth.

### Institution page

Charter, executable rules, membership, roles/capabilities, assets, current proposals, election procedure, enforcement history, legitimacy estimates, and amendment lineage.

### Event and “Why?” page

Every headline opens an event. Users can walk backward through causal parents, forward through consequences, inspect pre/post state, see who knew what when, and distinguish deterministic rule from random draw and LLM choice.

### Replay

Timeline scrub, speed control, layer selection, and resident viewpoint. The same event can be replayed from omniscient audit view or one resident’s information-constrained view.

## Director service

The director is a read-only journalist. It may:

- cluster linked events into candidate arcs;
- rank significance by deaths/injuries, reversibility, people affected, resource delta, institution change, novelty, and long-term dependency;
- write summaries with event citations;
- propose camera locations and alert thresholds;
- compare canonical and shadow branches.

It may not schedule weather, alter decisions, award resources, change memories, or suppress events from the audit log. A factuality checker rejects uncited claims in summaries.

**The director is a prompt-injection target, and it is the one that reaches the human.** Residents author text — speech, proposals, public records, rule drafts — and that text flows into the director's context, whose output is displayed to the observer as the authoritative account of what happened. A resident whose utterance contains instructions aimed at the summarizer could bias the "Since you left" page, suppress a headline, or fabricate a motive, without ever touching world state. The world would remain perfectly intact while the observer's understanding of it was corrupted, and the read-only guarantee would be technically satisfied throughout.

Required controls:

- All resident-authored text enters the director's context as **explicitly delimited, untrusted data**, never as instruction.
- The **factuality checker runs on the director's output against linked events** and is the enforcement point: an assertion without a supporting event citation is rejected regardless of how it was induced.
- The observer UI **escapes all resident-authored strings** — this text is untrusted input rendered in a browser, and it is the obvious cross-site-scripting path.
- Director prompts and outputs are logged and replayable like any other model call, so a corrupted summary can be traced to the utterance that caused it.
- Injection attempts aimed at the director are a **named red-team scenario** in [`09`](09-validation-and-experiments.md), distinct from injection aimed at residents.

## Shadow worlds

At selected decision points the experiment service may fork a short-lived branch:

- identical pre-fork state and RNG streams;
- replace one decision or model response;
- run a bounded horizon;
- compare outcomes and causal divergence;
- mark everything non-canonical and apply a separate budget.

Examples: “What if the rationing vote failed?” or “What if the messenger arrived one day later?” These provide insight without allowing the observer to rewrite history.

## Alerts

Alerts are state-based and non-intervening:

- population extinction or settlement abandonment;
- active fire/epidemic/organized conflict;
- projected potable water or calories below thresholds;
- event-log/hash/replay mismatch;
- stuck scheduler, provider outage, cost anomaly, repeated invalid output;
- no meaningful state mutation for a suspicious wall-clock interval;
- hidden-state leak or authorization violation.

Notifications should avoid sensational labels. “Organized conflict detected” links to evidence; it does not declare a “war” until the configured structural criteria are met.

## Measuring interestingness safely

Interestingness is an observer metric, never an agent reward. Track:

- causal depth and number of domains in an event cascade;
- institutional novelty and persistence;
- project novelty and utility;
- distributional change and reversals;
- unresolved tensions and branching possibilities;
- surprise relative to an ensemble forecast;
- narrative compression ratio: meaningful events per summary sentence.

We explicitly do **not** optimize model prompts or world parameters against engagement, violence, death, or catastrophe counts.
