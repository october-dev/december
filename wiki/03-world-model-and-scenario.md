# 03 — World Model and Founding Valley Scenario

## Scenario: Founding Valley

A flood-fed tributary crosses a temperate valley with upland woodland, marsh, grassland, arable patches, clay, stone, fish, and migratory prey. Twelve adults from several households have established a new settlement after leaving an older community. They share a language and inherited customs.

The founding state is **declared, randomized, and varied—not unauthored** — see [`17`](17-initial-conditions-and-authorship.md), which is binding on this section. Earlier drafts described the founders as disagreeing "about property, leadership, risk, and relations with a neighboring mobile band," and described land claims as "ambiguous" and assembly procedure as "unsettled." Those were not neutral initial conditions; they were the plot, pre-installed. If the settlement later fractures over property and elects a leader to resolve it, we would have observed only what we planted. Generators do not remove authorship: their distributions, constraints, correlations, exclusions, and accepted seeds are all research decisions.

What the scenario may specify is **material and structural**:

- household composition, ages, kin links, and dependency ratios sampled from declared demographic ranges;
- per-household stores, tools, and skills, unequal because households differ in size and history;
- actual land claims with actual evidence and actual overlaps — ambiguity is then a *derived* property of the claim ledger, not an authored mood;
- distances from each dwelling to water, arable land, and fuel;
- a partly planted first crop, an unfinished irrigation ditch, and shelters of differing quality, each with real material state;
- values sampled per resident from the declared vocabulary in [`04`](04-agents-cognition-and-memory.md), with seed and distribution recorded.

The founding charter carries three inherited rules — violence is forbidden within the central hearth area, the communal grain store requires two key-holders, and disputes may be called before an assembly. These are legitimate as **inherited culture from the community the founders left**, with recorded provenance. They are not a designed constitutional crisis: either the charter specifies the assembly's procedure or there is no assembly. Deliberately underspecifying a rule so it can be fought over is authorship.

**A no-charter control arm is mandatory in every institutional ensemble.** If governance emerges only when a charter is seeded, then the charter is producing the institutions and the emergence claim is void.

"Neither utopian nor already doomed" is a design intent, and it becomes a specification only when measured: initial stores cover a stated number of days at current consumption, and the ensemble's one-year survival rate under scripted policies falls within a declared band.

## Authoritative state domains

### Geography and environment

Each cell or region tracks:

- coordinates, elevation, slope, surface type, traversability;
- soil texture, fertility pools, erosion, moisture, and cultivation state;
- surface water flow/volume and groundwater proxy;
- vegetation biomass by functional group and burnable fuel;
- wild food and prey stocks with regeneration/mobility;
- weather exposure, temperature proxy, precipitation, wind, and fire state;
- constructed features, paths, fields, claims, and occupancy.

Weather is generated from a seasonal stochastic process with autocorrelation and scenario-level climate parameters. We do not need a meteorological model; we do need wet/dry persistence, seasonal temperatures, correlated spatial effects, and extreme tails. Weather feeds hydrology, crops, vegetation, fire, travel, and health.

### People and bodies

Every person has:

- age/life stage, household/kin links, location and activity;
- energy reserve, hydration, temperature/exposure, fatigue, sleep debt;
- disease states, injuries, functional limitations, pregnancy/infant state where applicable;
- skills, practiced proficiency, known techniques, and teaching links;
- carried inventory, access rights, claims, debts, obligations, and offices;
- cognition tier and next activation conditions.

Sex/gender and reproduction require a later design note and review. The kernel only needs the minimal attributes required for demographic transitions and consensual household choices; it must not infer behavior from stereotypes.

### Things and resources

Resources are typed lots, not prose:

```text
lot = {
  kind, quantity, unit, quality, condition,
  location_or_container, custodian, claimants,
  produced_at, expires_at?, provenance_event
}
```

Initial kinds include potable/non-potable water, edible plants, grain, fish/meat, seed grain, wood by size, fiber, clay, stone, hides, fuel, tools, vessels, medicine proxies, and waste. Quality affects nutrition, durability, spoilage, and disease risk.

### Structures and projects

A structure is a spatial assembly of components with condition, capacity, access, function, and maintenance needs. A project holds:

- proposed design and purpose;
- site and access authorization;
- dependency DAG;
- bill of materials;
- labor tasks and skill/tool requirements;
- work completed and defects;
- owner/steward and future maintenance schedule.

There are no instant buildings.

### Relationships and groups

The social graph distinguishes:

- kin/household relationship;
- familiarity and frequency of contact;
- trust by domain, affection, fear, grievance, respect, perceived competence;
- obligations, gifts, debts, promises, testimony, and conflicts;
- groups, membership, roles, entry/exit rules, shared assets, and declared purpose.

Relationships are directional and evidence-based. “Trust” is not one universal score: a resident may trust someone’s farming judgment but not their honesty with stores.

### Institutions and public artifacts

Institutions are persistent rule bundles plus roles and assets. Public artifacts include enacted rules, proposals, vote records, office grants, judgments, boundary markers, tallies, calendars, and agreements. Literacy is unnecessary: records can represent witnessed oral commitments, tokens, marked clay, cords, or maintained memory, with durability and accessibility properties.

## Core physical processes

### Food and energy

The kernel models energy in consistent abstract units, with documented conversion to calories only when calibrated. Daily needs depend on age/life stage, condition, temperature, and exertion. Food lots carry energy/nutrient proxy, water content, contamination, and spoilage state.

Food pathways:

- gathering depletes renewable patches with diminishing returns;
- hunting/fishing success depends on stock, location, skill, tools, effort, and stochastic encounter/capture;
- crops pass through phenological stages conditioned on planting window, moisture, temperature, soil, labor, pests, and damage;
- processing changes edibility, storage life, and labor cost;
- storage capacity, pests, moisture, theft, and spoilage matter;
- seed consumption trades present survival against future yield.

### Water

Water exists in sources and containers. Collection takes time; treatment methods reduce hazards; irrigation diverts finite flow; upstream activity affects downstream access and quality. Wells and aqueducts are future expansions. This system is a natural source of both cooperation and conflict.

### Materials, tools, and maintenance

Extraction changes the environment. Tools have condition and task multipliers; broken tools become repairable components or waste. Buildings decay from exposure, use, pests, fire, and deferred maintenance. A settlement can grow itself into a maintenance trap.

### Health, injury, and disease

Health is not a hit-point bar. The first release uses:

- nutritional reserve and chronic undernutrition;
- dehydration and exposure;
- fatigue/sleep;
- task/accident injuries by body-function category;
- wounds, contamination, healing, impairment, and mortality risk;
- the five-mechanism disease model below.

#### Disease must be restructured for a population of eighteen

A single generic SEIR pathogen — the earlier design — is the wrong model at this scale. Critical community size for acute, directly transmitted, immunizing infections is in the hundreds of thousands; December's population is four orders of magnitude below it ([`15`](15-parameter-registry.md) §D). Such a pathogen will either fade out immediately and contribute nothing, or, if tuned until epidemics appear at a satisfying rate, encode a rate that cannot exist. The second outcome is risk **R-07** wearing epidemiological costume.

Five mechanisms with genuinely different persistence logic replace it:

| Mechanism | Persists because | Role |
|---|---|---|
| **Introduced acute epidemics** | It does not — it burns through and ends | Rare punctuated shocks, tied to actual contact events |
| **Environmentally transmitted** (water- and food-borne) | Environmental reservoir; population size is irrelevant | The settlement's standing, self-generated disease pressure |
| **Zoonoses with animal reservoirs** | Animal reservoir | Rodent-borne risk arising from the settlement's own grain stores |
| **Chronic and latent infection** | The host is the reservoir; latency reactivates | Background burden that survives at any population size |
| **Helminths and parasites** | Faecal-oral and environmental cycling | Emergent consequence of sedentism and sanitation |

The last four, not the first, are the *ongoing* health mechanics. This is a better design than a generic plague: it couples disease to the settlement's own decisions about water, waste, storage, and sedentism. The ethnographic contrast is striking — foragers and subsistence farmers in the *same* ecosystem differ more than tenfold in intestinal parasite prevalence, because one group is sedentary. **Helminth load, rodent zoonoses, and water-borne disease should be emergent outputs of December's sanitation and storage variables, not parametric inputs.** The settlement's success at storing grain is what brings the rats.

Two hard requirements on the epidemic mechanism:

1. **Expect strong finite-population variability.** Branching-process intuition predicts frequent early fade-out and, conditional on establishment, potentially large outbreaks. At n=18, intermediate final sizes remain possible; they are not automatically bugs. Validate the ensemble distribution against the configured contact and disease process rather than enforcing two outcome bins.
2. **Do not treat published R₀ values as inputs.** They come from dense modern populations and are functions of social organization; measles estimates alone span 3.7 to 203. Model contact structure explicitly and let the effective reproduction number emerge.

The design borrows the architecture and testing discipline of individual-based epidemic models, not their COVID-specific parameters. New pathogens enter through configured reservoirs, visitors, migration, or mutation scenarios — never from a drama generator.

Undernutrition and infection interact multiplicatively rather than additively — roughly half of child mortality in high-burden settings is attributable to undernutrition, and mild-to-moderate undernutrition carries most of that risk. This coupling is what ties the subsistence module to the health module, and it should be explicit rather than emergent-by-accident.

### Demography

Birth, maturation, aging, partnering/household reconfiguration, migration, and death are explicit events. Fertility is conditioned on eligible consensual household decisions, age/life stage, health, energy, social circumstances, and stochastic timing. Child survival and dependency create real labor and food tradeoffs. Numerical rates remain provisional until sourced and sensitivity-tested.

## Ecological feedbacks

- Harvesting above regrowth depletes wild patches.
- Cultivation draws down soil fertility unless fallow, flood deposition, or modeled amendment restores it.
- Tree/fuel removal changes travel, construction supply, erosion, and fire behavior.
- Prey populations respond to habitat, reproduction, hunting, and weather.
- Waste and crowding raise environmental disease risk.
- Irrigation improves crops but takes labor, alters water distribution, and can fail catastrophically.

No subsystem needs maximal scientific detail. Each needs enough state and feedback to prevent dominant exploits and create meaningful tradeoffs.

## Causal catastrophe pathways

Catastrophes are emergent cascades. These pathways are hypotheses to test, not scripts.

### Drought and famine

```text
low precipitation → low stream flow/soil moisture
→ crop stress + gathering decline + irrigation dispute
→ drawdown of stores/seed grain
→ rationing, concealment, theft, trade or migration
→ undernutrition + lower labor capacity + disease susceptibility
→ failed harvest / political crisis / mortality
```

### Fire

```text
dry fuel + ignition + wind
→ cell-to-cell spread
→ structure/crop/store damage + smoke/exposure
→ displacement + loss of tools/records
→ emergency cooperation or blame
→ rebuilding burden, migration, or settlement abandonment
```

### Epidemic

```text
introduction via visitor/contact/reservoir
→ exposure across actual contact graph
→ presymptomatic/visible illness
→ care, avoidance, isolation, ritual, or denial decisions
→ labor shortage + concentrated caregiving contact
→ recovery, impairment, death, institutional response
```

### Ecological overshoot

```text
successful settlement growth
→ higher extraction and shortened fallow
→ declining prey/soil/wood near settlement
→ longer trips + higher labor demand
→ weaker maintenance/childcare/defense
→ shock sensitivity, dispersal, or collapse
```

### Political fission and local war

```text
distributional conflict + identity/kin clustering
→ failed adjudication / disputed office
→ factional withholding and rival claims
→ exit or occupation of key resource
→ negotiation, sanctions, raid, or mobilization
→ encounter-level violence + injury/death
→ vengeance, settlement split, treaty, domination, or depopulation
```

### Knowledge bottleneck

```text
specialization around one expert
→ expert death/migration/injury
→ unavailable repair/crop/storage technique
→ cascading project failures and lost productivity
→ apprenticeship reform, outside exchange, or decline
```

### Compound extinction

Extinction should almost never have one cause. A terminal settlement might follow drought, factional departure, epidemic, and a harsh winter. The causal graph assigns contributing conditions rather than declaring a single melodramatic cause.

## Hazards and “random things”

Candidate v1 hazards:

- dry/wet spells and temperature anomalies;
- lightning and accidental ignition;
- crop pest/disease pressure;
- injury during travel, hunting, felling, construction, or fighting;
- pathogen introduction and transmission;
- prey migration and hunting variance;
- birth complications and background mortality (abstractly represented);
- landslip/flood only if terrain/hydrology supports it.

Rare-event rates must be tested across thousands of accelerated non-LLM runs. If extinctions happen constantly, the world is a catastrophe machine; if they never happen under severe stress, it is padded.

## Boundary world

The valley is not a sealed jar. The external world is represented in layers:

1. **Climate/resource boundary:** weather regimes and migratory stocks.
2. **Aggregate groups:** neighboring populations with demographics, stores, territory, needs, disposition, and travel schedules.
3. **Materialized contacts:** named people created from aggregate state when interacting locally.
4. **No deus ex machina:** outsiders cannot appear with arbitrary goods or armies; aggregate ledgers conserve them.

This provides trade, exogamy, migration, disease, diplomacy, and war without simulating a continent.

**Exogamy is the boundary world's most important function, not its most colorful one.** Twelve founding adults sit below every modelled viability threshold ([`01`](01-scope-and-realism-contract.md), [`15`](15-parameter-registry.md) §C). Partner exchange, in-migration, and fostering are what make multigenerational history possible at all. The aggregate neighbor is therefore required from **Phase 3**, ahead of the conflict and disease mechanics it also enables, and the migration-and-exchange path must be validated before the raiding path is built. A boundary world introduced only as a source of threat would make the neighbors into a hazard generator — precisely the design failure [`07`](07-time-emergence-and-observation.md) forbids.

**One neighbor of similar size is not sufficient.** Two settlements of eighteen give a combined pool of ~36 — roughly a quarter of the minimum viable mating network of 150–500. The boundary world therefore needs a third layer between "the neighboring band" and "the abstract climate boundary": a **periodic regional aggregation**, a seasonal gathering that residents travel to and return from.

This is ethnographically standard — the forager settlement hierarchy has an aggregation tier at roughly 165 people — and it is efficient design, because a single mechanic supplies partners, news, trade, disease introduction, diplomacy, and reputation at once. It also gives December a natural rhythm: a recurring event the settlement must decide whether to attend, prepare for, and send people to, with real opportunity costs during the season it falls in.

The archaeological record is explicit that such networks carried **marriage partners along the same routes as goods**, and that when the network contracted, the dependent colonies died. Modelling aggregation as optional-but-costly, and letting residents under-invest in it, creates one of the most defensible slow-burn failure modes available to this project.
