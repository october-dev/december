# Four Bodies Need Food

**Status:** implemented walking skeleton; parameters provisional

This milestone adds the first material pressure that can eventually constrain
resident choice. Bodies have energy, hydration, health, and life status. Grain
and water are conserved stocks. Eating and drinking move matter into declared
consumption sinks while replenishing bounded reserves. Metabolism drains those
reserves, deprivation damages health, and zero health produces an irreversible
death event.

It is intentionally a body loop without a mind. The Founding Valley replay
still supplies scripted typed commands. This isolates physical correctness from
LLM behavior and lets the observer, replay, and conservation machinery mature
before model calls can disguise defects.

## Canonical body state

Each resident currently stores:

- `energy_kilojoules`, bounded by a provisional 12,000 kJ reserve;
- `hydration_millilitres`, bounded by a provisional 4,000 ml reserve;
- `health_ppm`, from 1 to 1,000,000 while alive;
- `alive`, with death irreversible in the current schema;
- position and current activity from the preceding observer milestone.

The world ledger now stores live, spoiled, and consumed grain plus live and
consumed water. The kernel checks both conservation equations after every
event. A failure aborts immediately.

## Implemented commands and events

| Command | Canonical event | Effect |
|---|---|---|
| `create_water` | `water.created.v1` | Adds water through an explicit source process. |
| `metabolize` | `resident.metabolized.v1` | Drains energy and hydration; records any health loss. |
| `eat` | `grain.consumed.v1` | Removes grain, records the sink, replenishes bounded energy. |
| `drink` | `water.consumed.v1` | Removes water, records the sink, replenishes bounded hydration. |
| deprivation at zero health | `resident.died.v1` | Marks the body dead and prevents further activities. |

The event records outcomes, not formulas to recompute during replay. Recorded
history therefore reconstructs without consulting parameters or randomness.

## Provisional parameters

The walking skeleton uses 100 kJ and 100 ml per simulated hour at activity
multiplier 1.0. Activity multipliers use integer parts-per-million. Food yields
15 kJ per gram. Deprivation damage is deliberately simple and is not a human
physiology claim.

These values exist to exercise event flow and invariants. They must be replaced
through literature review, dimensional checks, sensitivity sweeps, and Gate 1
calibration before a canonical long-running world begins.

## Tests and observer evidence

The suite asserts:

- grain remains `live + spoiled + consumed = created`;
- water remains `live + consumed = created`;
- reserves and transitions stay integer-valued;
- eating and drinking cannot consume unavailable stocks;
- the same metabolism history replays to the same state hash;
- deprivation can produce death;
- dead residents cannot begin another activity;
- identical observer exports remain byte-identical and hash-contiguous.

`december.observer.v2` adds body fields, water containers, and expanded ledgers.
The viewer reconstructs each resident's current reserves from the snapshot and
ordered events, and displays energy, hydration, health, food, water, population,
and body events without a write path back to the kernel.

## What this does not yet provide

- automatic needs-driven action selection;
- digestion, sleep recovery, temperature, illness, injury, age, or pregnancy;
- renewable water, crops, weather, seasons, or ecology;
- food types, nutrition, cooking, waste, or contamination;
- validated human metabolic or mortality dynamics;
- perception, memory, deliberation, relationships, or language models.

The next engineering milestone is a deterministic ecology and scripted policy
runner: bodies should notice only permitted local facts, choose from typed
policies without an LLM, and survive or fail across many seeds. The following
research milestone is **Four Minds in a Hut**, where bounded model decisions are
introduced without changing physical authority.
