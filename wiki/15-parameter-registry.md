# 15 — First-Cut Parameter Registry

**Status:** provisional research notebook. Added by audit pass 1 and downgraded by pass 2 pending row-level reproducible provenance and transfer review.

Every prior draft said parameters would be sourced "during Phase 1." That deferral hid the fact that several design commitments were already numerically impossible. This document supplies first-cut anchors so the plan can be checked against reality *before* code is written, and so Phase 1 calibration starts from a bibliography rather than a blank page.

## How to read this

Each value currently carries an audit **evidence class**, not implementation approval:

| Class | Meaning |
|---|---|
| **V** | Auditor-reported verification — not reproducible provenance without a source ID and exact locator on the row |
| **D** | Derived — computed by the audit from verified inputs; arithmetic, not measurement |
| **S** | Secondhand — a paywalled primary quoted verbatim by a fetched peer-reviewed source |
| **C** | **Contested** — the literature genuinely disagrees; must be a range or scenario axis, never a point value |
| **N** | **Not verified** — could not be confirmed; do not use in code without checking |

No value here is calibrated or approved for December. These are research leads: they may bound plausibility or reveal nonsense, but most come from populations and environments unlike the fictional Founding Valley. Before a row enters code it must gain `source_id`, exact table/page/section locator, source population, transformation formula, intended subsystem, transfer justification, uncertainty representation, and reviewer status. A bold number plus “V” is not enough.

Interpretive prose in this notebook is hypothesis, not design law. Phase 1 admits only the smallest parameter subset needed for its registered patterns; genetics, warfare history, and other later-domain material remain out of the kernel until their phase and research question justify them.

**Read the design notes, not just the tables.** Several numbers below carry consequences that change how a subsystem must be built.

---

## A. Human energetics

| Parameter | Central | Range | Unit | Context | Class |
|---|---|---|---|---|---|
| PAL, sedentary/light | 1.55 | 1.40–1.69 | ×BMR | FAO/WHO/UNU 2004 Table 5.3 | V |
| PAL, moderately active | 1.85 | 1.70–1.99 | ×BMR | same | V |
| PAL, vigorous | 2.20 | 2.00–2.40 | ×BMR | same; >2.40 unsustainable long-term | V |
| PAL, non-mechanized agriculture — **FAO category** | 2.25 | 2.00–2.40 | ×BMR | FAO worked example | V |
| PAL, farmers — **actually measured** | M 1.90 / F 1.74 | M 1.36–2.40 / F 1.47–2.36 | ×BMR | Doubly-labelled-water review, 26 studies | V |
| PAL, Hadza foragers | M 2.26 / F 1.78 | ±0.48 / ±0.30 | ×BMR | DLW, n=30 | V |
| PAL, survival minimum | 1.27 | — | ×BMR | Totally inactive dependent person | V |
| BMR, Schofield M 18–30 | 15.057W + 692.2 | see 153 | kcal/day | W in kg; FAO 2004 retains Schofield | V |
| BMR, Schofield F 18–30 | 14.818W + 486.6 | see 119 | kcal/day | same | V |
| BMR, Henry M 18–30 | 16.0W + 545 | — | kcal/day | UK SACN 2011 adopted Henry | V |
| BMR, Henry F 18–30 | 13.1W + 558 | — | kcal/day | same | V |
| Henry vs Schofield | −3 to −4 | — | % BMR | Henry lower; 79% vs 69% within ±10% of measured | V |
| **TEE, man 60–70 kg, subsistence agriculture** | 3,200 | 2,900–3,900 | kcal/day | DLW measured; upper bound = peak harvest season | V |
| **TEE, woman 50–60 kg, subsistence agriculture** | 2,400 | 2,100–2,800 | kcal/day | DLW measured | V |
| Walking cost, level, **gross** | 0.81 | 0.72–0.91 | kcal·kg⁻¹·km⁻¹ | 3.4 J/kg/m; meta-analysis of 13 studies | V |
| Walking cost, level, **net** | 0.57 | 0.38–0.67 | kcal·kg⁻¹·km⁻¹ | 2.4 J/kg/m | V |
| Load carriage | `M = 1.5W + 2.0(W+L)(L/W)² + η(W+L)(1.5V² + 0.35VG)` | — | watts | Pandolf 1977; **G in percent**, V in m/s | V |
| Terrain factor η | 1.0 blacktop / 1.1 dirt / 1.2 light brush / 1.5 heavy brush / 2.1 sand | ±0.1–0.2 | — | USARIEM's own field data gave 1.2 for "1.1" surfaces | V |
| Minnesota: semi-starvation | 24 weeks @ ~1,570 | — | kcal/day | 36 men started, **32 analysed** | V |
| Minnesota: weight loss | −24 | −25 target | % body mass | 69.4 → 52.6 kg; BMI 21.9 → 16.4 | V |
| **Minnesota: strength decline** | −28 | to −37 | % | Grip dynamometer | V |
| **Minnesota: work capacity decline** | **−72** | to −94 | % | Harvard fitness test | V |
| Minnesota: VO₂max decline | >−40 | — | % | At 25% weight loss | V |
| Minnesota: BMR decline | −38 | 15–25 pts adaptive | % | 1,608 → 994 kcal/day | V |
| **No performance loss below** | 10 | — | % body-mass loss | Taylor 1957 | V |
| Lethal BMI, men / women | 13 / 11 | survival below 10 documented | kg/m² | Henry 1990; **~21 fatal cases — modal, not a wall** | S, C |
| Body-mass loss at death | 30 | 25–35 | % initial | Hunger-strike series | S |
| Starvation survival, water available | 62 | 46–73 | days | 10 IRA hunger strikers, healthy adult males | V |
| Starvation survival, broader series | 62.5 | 11–115 | days | 20 political strikers since 1920 | V |
| Survival without water, 32 °C shade, resting | 3 | 2–5 | days | Adolph's table | S |
| Survival without water, 21–27 °C | 10 | 9–12 | days | same | S |

### Design note A-1 — starvation is a behavioral parameter, not only a physiological one

The Minnesota figures are the most useful thing in this section, and the useful part is not the weight loss. **Work capacity fell 72% while body mass fell only 24%.** An undernourished resident is not a slightly slower worker — they are a person whose capacity to do anything demanding has collapsed nonlinearly, well before they look like they are dying.

The behavioral record is equally specific and equally implementable: **97% reported tiring easily**; two-thirds were downhearted with concentration difficulty; there was "no sign of a drive for activity"; food preoccupation dominated waking thought; sexual interest and sociability withdrew. Notably, **measured intellectual ability, memory, and logic did not decline** even though subjects believed they had — a distinction worth preserving, because it means a starving resident should still reason competently while wanting almost nothing except food.

This belongs in the appraisal prompt and in the behavioral test suite ([`09`](09-validation-and-experiments.md)). It is one of the few places where a well-documented human response can directly discipline LLM behavior rather than leaving "acts hungry" to the model's imagination.

The cited performance threshold must not be turned into “hunger is free below 10% weight loss.” Hunger, attention, mood, and food-seeking can change before measurable strength/work-capacity loss, and the study population does not justify a universal threshold. Model immediate hunger/appraisal pressure separately from a delayed nonlinear impairment curve, and sweep the curve under explicit uncertainty.

---

## B. Subsistence production

| Parameter | Central | Range | Unit | Context | Class |
|---|---|---|---|---|---|
| **Wheat yield ratio** | 3.66 | 2.16–5.35 (p10–p90) | seed:seed | 8,403 English manor-years, 1211–1491 | V, D |
| Barley yield ratio | 3.60 | 2.12–5.19 | seed:seed | 7,439 manor-years | V, D |
| Oats yield ratio | 2.56 | 1.41–3.75 | seed:seed | 9,479 manor-years | V, D |
| Rye yield ratio | 3.92 | 2.03–6.00 | seed:seed | 1,247 manor-years | V, D |
| **Harvest retained as seed, wheat** | **27** | 19 (good yr) – 46 (bad yr) | % | = 1/ratio | D |
| Harvest retained as seed, oats | 39 | 27–71 | % | | D |
| **Contemporary break-even ratio** | 3.0 | — | seed:seed | Walter of Henley's medieval accounting target | V |
| Wheat yield, absolute | 554 | 327–810 | kg/ha gross | ratio × sowing rate | D |
| Emmer, hand-hoed, no manure | 2.08 | 0.78–3.11 | t/ha | Butser Ancient Farm, 15 consecutive seasons | V |
| Emmer, swidden, years 1→4 | 1.2 → 1.1 → 0.7 → 0 | — | t/ha | Butser slash-and-burn, mattock hoe | V |
| Millet, low-input smallholder | 500–1,500 | 150–3,000 | kg/ha | Modern African analogue | V |
| Yield CV, individual field-year | 0.36 | 0.36–0.41 | — | Across four cereals | D |
| Yield CV, regional annual mean | 0.14 | 0.11–0.15 | — | National annual means | D |
| Complete crop failure frequency | 7 | — | % of seasons | Butser: 1 in 15, killed by frost | V |
| **P(wheat ratio < 2.0)** | 7.0 | — | % of field-years | Half or more of harvest must be re-sown | D |
| Lag-1 autocorrelation of yields | 0.21 (wheat) | 0.21–0.66 | r | Bad years cluster, spring grains especially | D |
| Cross-crop correlation | 0.41 | 0.30–0.59 | r | **Diversification genuinely reduces risk** | D |
| **Total swidden labor** | 175 | 64–330 | person-days/ha | 17 SE Asian cases, core operations | V |
| Total swidden labor | 1,050 | 384–1,980 | person-hours/ha | at 6 h/person-day | D |
| — slashing and felling | 41 | 9–75 | person-days/ha | 18% of total | V |
| — burning and ground prep | 12 | 1–47 | person-days/ha | 7% | V |
| — planting | 23 | 8–55 | person-days/ha | 14% | V |
| — **weeding** | **49** | **0–153** | person-days/ha | **16% under long fallow → 38% under short** | V |
| — reaping, threshing, winnowing | 50 | 23–73 | person-days/ha | 27% | V |
| Labor productivity | 6.6 | 3.8–25.1 | kg grain/person-day | | V |
| **Saddle-quern grinding** | 0.69 | 0.57–0.90 | kg grain/hour | Coarse meal reaches 2.1; fine meal 0.63 | V |
| Grinding labor | 1.45 | 1.1–1.75 | hours per kg | Inverse of above | D |
| Rotary quern | 3.0 | — | kg grain/hour | 4.3× the saddle quern | V |
| Grinding energy cost | 206 | — | kcal/hour (PAR 3.5) | 30 women, indirect calorimetry | V |
| **Daily grinding time** | 3–5 | 1.7–8 | hours/day per woman | Ethnographic, 5–10 person household | V |
| Storage loss, cereals, 9-month season | 3 | 1–6 | % | Millet 1%, sorghum 2–4%, wheat 3–5% | V |
| Storage loss, insect-infested | 11 | 9.7–13.3 | % | Maize with Larger Grain Borer | V |
| Storage loss, first 3 months | ~0 | — | % | **Loss is convex in time, not linear** | V |
| **Whole post-harvest chain loss** | 13 | 9–18 | % field → consumption | Storage proper is only 1–5 points of this | V |
| Foraging return, men (incl. search) | 1,339 | 1,018–1,619 | kcal/hour | Aché, 611 man-foraging-days | V |
| Foraging return, women (incl. search) | 1,221 | 302–2,804 | kcal/hour | Aché, 61 woman-days | V |
| Between-forager spread | — | 446–2,124 | kcal/hour | 25 Aché men — a **4.8× individual spread** | V |
| Honey, on-encounter | >20,000 | — | kcal/hour | Aché | V |
| Horticulture vs foraging | 1.5–2× | — | multiplier | Return rate advantage | V |
| **Large-game hunting success** | 0.03 | 0.027–0.034 | P per hunter-day | Hadza, **large game only**; failure >97% | V |
| Hunting success, all prey incl. small game | 0.23 (!Kung) – 0.65 (Aché) | 0.23–0.76 | P per hunter-day | **Not the same quantity as above** | S |
| **Hunting daily-return CV** | **8.1** | — | SD/mean | Hadza: mean 4.89 kg, SD 39.7, n=2,072 | D |
| Meat package size | 12.8 | SD 14.0 | kg | Hiwi; CV ≈ 1.1 | V |
| Gathered package size | 4.3 | SD 4.1 | kg | Aché; CV ≈ 0.95 — much tighter | V |
| Shellfish collecting | 1,492 | ±173 SE | kcal/hour incl. search | Meriam reef flat | V |
| Spearfishing | 292 | ±135 SE | kcal/hour incl. search | Meriam; **8.6× search penalty** | V |
| Water, drinking + water in food | 2.75 | 2.5–3 | L/person/day | Sphere survival standard | V |
| **Water, total domestic** | 15 | 7.5–15 | L/person/day | Sphere minimum standard | V |
| Firewood, cooking only | 1.0 | 0.85–1.25 | kg/person/day | Three-stone fire, warm climate | V |
| Firewood, cooking + indoor warming | 1.8 | 0.5–4.0 | kg/person/day | Temperate winter | V |
| Firewood, cold climate pre-industrial | 4–10 | up to 10 | kg/person/day | Northern Europe | S |

### Design note B-1 — the seed-grain ratio is the most consequential number in the model

At a 3.66:1 return, **27% of every harvest must be withheld from hungry people to plant next year**, and in roughly one field-year in fourteen that figure exceeds 50%. Medieval accountants used a 3:1 return as the break-even line, which means a settlement is routinely operating within a factor of ~1.2 of not being able to re-sow.

This can make a famine cascade materially real rather than decorative. Eating seed grain is a possible immediate-survival tradeoff with delayed cost. It may become a private, household, or institutional issue; calling it the settlement’s “first governance dispute” would script the outcome that the emergence protocol is meant to observe. The ratio remains provisional until crop, sowing system, climate, and storage assumptions match the selected scenario.

The distribution matters as much as the mean, and it is well characterized: manor-year ratios are close to lognormal (wheat μ=1.232, σ=0.370), bad years cluster (lag-1 autocorrelation up to 0.66 for spring grains, with three-year runs of bad harvests occurring repeatedly in the medieval record), and **cross-crop correlations of 0.30–0.59 mean planting two crops genuinely reduces risk** rather than merely appearing to. That gives residents a real, learnable, non-obvious strategy.

Critically: **the variance that matters is field-level (CV 0.36), not regional (CV 0.14).** A household lives on its own field.

### Design note B-2 — hunting variance can create strong risk-pooling pressure

The Hadza coefficient of variation on daily hunting returns is **8.1**. A hunter fails on more than 97% of days when large game is the target; the settlement eats meat because *someone* succeeds, not because anyone reliably does.

A model that gives hunters only their mean return per outing erases a major risk-pooling pressure. High variance can support sharing, reciprocity, prestige, and obligations, but it is not “the reason society exists,” and one population’s large-game rate is not a universal December parameter. **Model an appropriate distribution rather than only a mean** after prey set, technology, habitat, and comparison population are chosen.

Note also the prey-breadth decision, which moves success probability by an order of magnitude: 0.03/day for large game only versus 0.23–0.65/day when small game is included. Decide December's prey set *first*, then pick the matching rate. Do not average across these populations — they are answering different questions.

The cited datasets suggest different return distributions for gathered food and some hunting strategies. Treat the resulting sharing/obligation hypothesis as something the simulation can test, not as a universal social law.

### Design note B-3 — grinding is a hidden labor sink comparable to farming

Saddle-quern grinding can consume several household labor-hours per day under grain-heavy diets. The comparative record often shows gendered allocation, but December must not hard-code that allocation into a fictional society. Model the task burden, skill, fatigue, household negotiation, and norms; let labor allocation arise from declared initial culture and resident choices.

If December models fields and harvests but not processing, it will silently hand the settlement several free person-hours per day and misrepresent who is doing the work. Grain must be processed before it is food.

### Design note B-4 — weeding is where the Boserup mechanism lives

Total labor per hectare stays roughly flat as fallow shortens (~175 person-days), but its *composition* inverts: clearing falls and **weeding rises from 16% to 38% of all labor**, while yields decline. Labor productivity collapses even though labor input does not rise.

This is the intensification trap, empirically confirmed, and it is exactly the kind of slow structural pressure that makes a settlement's success into its later problem. It should fall out of the fallow-length state variable rather than being scripted.

---

## C. Demography

| Parameter | Central | Range | Unit | Context | Class |
|---|---|---|---|---|---|
| Life expectancy at birth | 31 | 21–37 | years | Hunter-gatherers, 5 populations | V |
| e0, forager-horticulturalists | 33 | 21–42 | years | | V |
| e0, pre-industrial Sweden 1751–59 | 34 | — | years | **Inside the forager range** | V |
| **Modal adult age at death** | 72 | 68–78 | years | Conditional on reaching adulthood | V |
| Infant mortality, first year | 23 | 21–27 | % of births | | V, D |
| **Survival to age 15 (l15)** | 0.57 | 0.44–0.73 | proportion | Foragers; forager-horticulturalists 0.64 | V |
| Survival to 45 (l45) | 0.36 | 0.26–0.43 | proportion | | V |
| Life expectancy at 45 | 20.7 | 12–24 | further years | **Survivors of childhood often reach old age** | V |
| Adult hazard, ages 15–40 | 0.01–0.02 | flat | annual q | Slope indistinguishable from zero | V |
| Mortality-rate doubling time, 40+ | 8–10 | 7–10 | years | Gompertz phase | V |
| Cause of death: illness / violence / degenerative | 70 / 20 / 9 | — | % | Whole cross-cultural sample | V |
| Early Neolithic e0 (Vedrovice, LBK) | 27.6 | — | years | Skeletal; ageing bias suspected | V |
| **TFR, foragers** | 5.6 | <4–8 | births/woman | 12 populations | V |
| **TFR, horticulturalists** | 5.4 | — | births/woman | **Not significantly different from foragers (p=0.8)** | V |
| **TFR, intensive agriculturalists** | 6.6 | ±0.3 SE | births/woman | The only significant subsistence break | V |
| Interbirth interval, foragers | 3.3 | 2.3–5.4 | years | | V |
| Interbirth interval, sedentary horticulturalists | 30.7 | SD 10.6 | months | Tsimane | V |
| Age at first birth | 19.7 | 15.3–22.8 | years | Forager mean | V |
| Age at last birth | 39.0 | 26–42 | years | Forager mean | V |
| Weaning age | 24–48 | 12–72 | months | Foragers | V |
| **Sedentism → fertility (Agta, within-population)** | 7.7 vs 6.6 | +16.7% | TFR | Settled vs mobile | V |
| Sedentism → child mortality | +63 | 0.93 vs 0.57 | deaths/mother | **Same study — a quantity/quality trade** | V |
| Neolithic Demographic Transition | +2 | contested | births/woman | Driven by 3–4 month earlier weaning | V, C |
| Steady-state agrarian growth | 0.1–0.2 | — | %/year | Pre-industrial equilibrium | V |
| Mean experienced band size | 28.2 | — | adults | 32 societies, n=5,067 | V |
| Adult primary kin per band | 1.8 | 0.45–5.27 | persons | **Only 7% of co-resident adults** | V |
| Household size, foragers | ~5 | 2.9–7.7 | persons | | V |
| Naroll floor-area constant | 10 | 9–10 | m²/person | 18 societies; author called it "very rough" | V |
| Late Natufian community | 59 | largest under 50 | persons | 0.2 ha | V |
| PPNA community | 332 | 18–735 | persons | 1.0 ha | V |
| Çatalhöyük peak (revised 2024) | 600–800 | vs 3,500–8,000 older | persons | Revised down ~5× | V |

### C-1. The founding population sits below every modelled threshold

This is a **structural finding**. Read it together with **C-4**, which supplies the historical counterweight: real colonies of this size have occasionally survived, so the correct conclusion is *marginal*, not *impossible* — and what separates the survivors is network connection rather than headcount.

**Every threshold estimated by every method sits above 18.**

| Method | Threshold | Finding |
|---|---|---|
| Demographic ABM (White 2017, ~5,000 runs/condition, 400-year horizon) | **40–140** by marriage rules; **150** for near-certainty | "Very small populations (i.e., less than 40 people) were not viable over a 400-year period" |
| Marriage-rule sensitivity | ×2.25–3.25 | Eight marriage divisions raise the requirement to 100–140; a simple incest taboo costs only ~10 persons |
| Closed-system Monte Carlo (Marin & Beluffi 2018) | 98 for certainty | **50 people went extinct in 50 ± 15% of runs** when inbreeding was forbidden |
| Endogamous-population simulation (MacCluer & Dyke 1976) | <300 monogamous; 50–100 with polygyny | | 
| Voyage microsimulation (Moore 2001) | 150–180 | "Populations varying in initial size from 4 to 60 persons invariably went extinct" at low fertility |
| Genetic (Frankham et al. 2014) | Ne ≥ 100 | "Ne ≤ 100 indicates … serious genetic threats after 5 or more generations" |

**The genetics are unambiguous at this size.** Twelve breeding adults give Ne ≤ 12 — realistically 8–10 once family-size variance is included — so inbreeding accumulates at **ΔF = 4.2% per generation**, four times the tolerance the 50/500 rule was built around:

| Generation | F at Ne=12 | Comparison |
|---|---|---|
| 2 | 0.082 | Already above first-cousin offspring (0.0625) |
| 3 | 0.120 | Approaching double-first-cousin |
| 5 | 0.192 | Beyond uncle–niece |
| 10 | 0.347 | 65% of original heterozygosity remains |

The *founding event* is mild — it retains 95.8% of heterozygosity. **Sustained small size, not the bottleneck, is what does the damage.**

**The single best empirical anchor is the Raute of Nepal**: a genuinely isolated population of **150 people** — more than eight times December's settlement — with an explicit three-clan exogamy system deliberately optimized against inbreeding. Result: mean spousal relatedness r = 0.124 and **F_ROH = 0.226**, meaning 22.6% of the genome is autozygous, approaching full-sibling level. Their own analysis concludes that "owing to overall limited genetic variation, high expected offspring inbreeding is observed regardless of the simulated mating system." The gradient against better-connected groups is stark:

| Population | Mating-network size | Mean spousal relatedness |
|---|---|---|
| Mbendjele BaYaka | >30,000 regional | 0.0053 |
| Palanan Agta | ~1,000 local / ~10,000 regional | 0.0175 |
| **Raute** | **150, isolated** | **0.1240** |

### C-2. What actually makes a small settlement viable: network membership

The correction the second pass forced, and it improves the design rather than constraining it:

> **A forager band of 28 adults sustains a mostly-unrelated composition only because it continuously exchanges members with a wider network. The viable unit is the network, not the settlement.**

The evidence is direct. Across 32 foraging societies, co-resident adult primary kin number only **1.8 per band — 7% of adults** — and about a quarter of band members share no known genealogical or marriage tie with any given person at all. Among 80 Agta marriages in a ~270-adult network, **78 had no known shared ancestry**. Studying two Pumé groups of ~11 adult males and ~11 adult females each — almost exactly December's scale — researchers concluded plainly that "in small populations, looking outside of one's local group is necessary to find a mate."

**A methodological caveat that sharpens this.** Figures drawn from ethnographic band size — the "magic 25," Dunbar's 150 — are **not closed-population numbers**. Those bands were never isolated; they maintained systematic mate exchange with adjacent bands, which is the entire reason a 28-adult band can be composed mostly of non-relatives. Citing band size as evidence that a small group is self-sufficient inverts the finding. The relevant quantity is always the *network*, never the camp.

**Required network size: ~150–500 people, with ~175 the smallest well-supported value.** This is where four independent estimates overlap: White's ABM (150), Wobst's mating-network simulation (79–332 raw, re-expressed as 175–475 under spatial assumptions), Birdsell's dialectal tribe (500 central tendency, but explicitly "commonly including groups of less than 200"), and the empirical forager hierarchy whose periodic-aggregation tier sits at ~165 and regional tier at ~839.

**Required in-migration: roughly 1–3 exogamous marriages per generation**, i.e. on the order of 15–30% of unions bringing in an outsider — comfortably within the ethnographic range.

**But gene flow only rescues a population that is already big enough.** The clearest demonstration comes from population viability analysis: at 12 breeding females with a realistic inbreeding load, one migrant per generation lowered 50-year extinction probability only **from 100% to 97%**, and three to four migrants gave no further improvement. At 48 breeding females, two migrants dropped it to 5%. There is a floor below which connection does not help.

### C-3. Founder effects, and why "purging" does not rescue December

A natural objection to §C-1 is that small populations *purge* their deleterious recessives — selection exposes them in homozygotes and removes them, so the inbreeding cost should be self-limiting. This is exactly the argument made against Frankham's revised thresholds. **The evidence says purging is real but weak, acts only on the extreme lethal tail, and at n≈18 is dwarfed by drift.**

| Finding | Evidence | Class |
|---|---|---|
| Hutterite founder recessive lethals: 57% lost by 1950 — but at a rate "almost the same as for neutral variants" | Loss was **drift, not selection** | V |
| Direct human test of mating practices | "Purging by non-random mating has low efficiency and different mating practices do not lead to different mutational loads" | V |
| Actively consanguineous cohort | Homozygous-knockout deficit only **13.7%** (95% CI 8–20) — ~86% still occur | V |
| Greenlandic Inuit, Ne <300 for 15,000+ years | **≥20% MORE recessive load**, not less | V |
| Additive load | Demography-proof; the two effects exactly cancel | V |
| Counter-evidence | Modest purging signal in recessive disease genes; *ancestral* Ne predicts persistence better than current Ne | V, C |

The Lord Howe Island stick insect, rebuilt from two mating pairs, is the cleanest illustration of the limit: stop codons were depleted, but "moderate- and low-impact mutations escape this process and may even fix." Purging removes the lethals and leaves everything else.

**One result deserves to drive December's design directly.** Extinction time for a population crashed to K=25–50 depends on its *ancestral* effective size, not its current one: **474 generations if the ancestral K was 1,000, but only 70 generations if the ancestral K was 15,000.** A group that has always been small carries a purged, survivable load; a group that has *recently become* small carries the full reservoir of a large population and is far more fragile. December's founders left an established community — they are the second case.

**Founding load, derived from verified rates** (this arithmetic is the audit's, not a cited figure):

| Quantity | Value | Basis |
|---|---|---|
| Recessive lethals per haploid genome | 0.29 (95% CrI 0.10–0.84) | Hutterite founder analysis |
| **Distinct recessive lethal alleles entering an 18-founder pool** | **~10** | 36 haploid genomes × 0.29 |
| Recessive LoF lethal equivalents per individual | 1.6 | Two independent studies converge |
| **F by generation 10 at Ne ≈ 12–15, no immigration** | **0.30–0.35** | ΔF = 1/(2Ne) |

That projected F is roughly **twice** the mean autozygosity of UK Biobank's "extreme inbreeding" individuals (FROH 0.172, prevalence ~1 in 3,650), for whom the measured dose-response is:

| Trait | Effect at FROH ≈ 0.17 |
|---|---|
| Peak expiratory flow | **−0.651 SD** |
| Fluid intelligence | −0.570 SD |
| Height | −0.404 SD |
| Educational attainment | −0.260 SD |
| Fertility | **RR ≈ 1.54 reduced** |

This is the best direct human dose-response available, and it points at the right *mechanism* for December: the cost lands on capacity and fecundity, not on dramatic death.

**Founder contribution is severely unequal, which makes effective size far smaller than founder count.** This is the most directly useful modelling finding in this subsection:

| Population | Nominal founders | Effective concentration | Class |
|---|---|---|---|
| Old Order Amish | 554 in the 14-generation pedigree | **128 account for >95% of the gene pool; 16 account for 50%** | V |
| Québec | ~8,500 French settlers, 1608–1760 | **15% of founders explain 90% of genetic contribution** | V |
| Ashkenazi | — | Effective founders **≈350** (250–420), 25–32 generations ago | V |
| Hutterites | 64 founders, 1,623-member pedigree | Mean F = **0.034** | V |

December should not assume its twelve founders contribute equally. Differential reproductive success concentrates ancestry fast, so realized Ne will run **below** the 8–10 already assumed in §C-1.

**The Hutterite fertility finding is directly implementable.** Inbreeding significantly lengthened **interbirth intervals** (p=0.024) and **time to conception** (p=0.010), but produced **no increase in fetal loss and no reduction in completed family size** — reproductive compensation absorbed the cost. So December's inbreeding penalty should appear as *slower* reproduction under a longer shadow, not as dramatic infant death. That is both better sourced and more interesting than a mortality multiplier.

**The best real-world anchor at December's exact scale is Tristan da Cunha**: 15 settlers in 1816 (7 women, 8 men), 28 founders in total. The community survived to the present — but carries a **36% asthma prevalence** today, alongside documented founder-effect retinitis pigmentosa. That is the honest picture of an 18-person founding at 200 years: persistence is possible, and it is not free.

For scale, human long-term effective population size sits at **~13,500** (ancestral non-African) with an out-of-Africa minimum around **1,200** at 40–20 kya. Even humanity's tightest documented bottleneck was roughly seventy times December's settlement.

### C-4. The historical counterweight — small colonies that *did* survive

Intellectual honesty requires reporting evidence that cuts against §C-1. The simulation and conservation-genetics literature says populations under 40 are non-viable. **Actual history contains small founding groups that persisted anyway**, and the audit's earlier flat statement that "18 people cannot persist" was too strong.

| Case | Founding party | Outcome | Class |
|---|---|---|---|
| **Pitcairn, 1790** | **27** — 9 mutineers, 6 Polynesian men, 11 Polynesian women, 1 infant | **Persisted 230+ years.** Peak 233 (1937); ~35 today. Violent early years left two adult males | V |
| **Tristan da Cunha, 1816** | **~28** founders; 15 settlers (7 women, 8 men) | **Persisted.** Carries 36% asthma prevalence and founder-effect retinitis pigmentosa | V |
| **Palmerston Island, 1863** | **4 effective founders** — one man and three Polynesian wives, two of them cousins | **Persisted.** 23 children, 134 grandchildren, >1,000 descendants by 1973 | V |
| **Pingelap, ~1775** | **~20 typhoon survivors** | **Persisted** (~250 today) with ~10% achromatopsia and ~30% carriers | V |
| **Rapa Nui, 1877** | Fell to **~110** (1892 census: 101 people, **12 adult men**) | **Recovered.** A documented real-world floor from which a population rebuilt | V |
| Roanoke, 1587 | 117 | Vanished | V |
| Saint Croix Island, 1604 | 79 → 44 | **44% mortality in one winter** (scurvy); abandoned | V |
| Jamestown "Starving Time," 1609–10 | 214 → 60 | 72% mortality; colony voted to abandon, reprieved by a relief fleet | V |
| Norse Greenland | 300–500 landing; peak ~2,000 | **Extinct by ~1450** (latest ¹⁴C: AD 1430 ± 15) | V |
| Henderson & Pitcairn (Polynesian) | — | Abandoned after ~600 years of continuous occupation | V |

**The corrected claim:** an 18-person founding is **marginal, not impossible.** It sits below every modelled threshold, and the historical cases that survived did so while (a) retaining outside contact and periodic in-migration, and (b) carrying a permanent genetic cost — Tristan da Cunha's 36% asthma rate is what an unrescued founder effect looks like two centuries on.

#### Four historical mechanisms December should model

These are the specific failure and survival modes the record actually documents. Each is more interesting than "the population was too small."

**1. Founding sex ratio drives violence, and violence erases lineages.** Pitcairn landed with **15 men and 12 women** — a male surplus that the record ties directly to the killings. Within ten years, **seven of nine mutineers and every one of the six Polynesian men were dead**; in 1800 the colony held **one adult man, nine women, and nineteen children**. The genetic signature is unambiguous two centuries later: of 223 Norfolk Island male descendants, **zero carry a Polynesian Y chromosome**, while 40.4% of maternal lineages are Polynesian. One founding group's entire male line was annihilated by social conflict that began as a partner shortage.

That is a complete causal cascade — initial sex ratio → competition → homicide → permanent loss of half the founding ancestry — running on exactly the mechanisms December already models. It is the single best argument that this scale produces interesting history rather than merely fragile history.

Note also the recovery: Pitcairn went from 27 to 193 in 66 years at **3.0%/year growth, with infant mortality of only 5.5% and marital fertility above Hutterite levels**. Small populations are not merely fragile; they are volatile in both directions.

**2. Correlated risk can remove a whole cohort in a day.** In 1885 Tristan da Cunha lost **fifteen men — roughly 79% of its adult males — in a single boat**, sent together to trade with a passing ship. The settlement never recovered its former size. December's activity scheduler should therefore treat *co-location of a demographic cohort* as a modelled hazard: a hunting party, a raid, a trading voyage, or a construction accident that puts most able adults in one place at one time is a single point of failure, and at n=18 it is an extinction-class event.

**3. A cause can be cured and the collapse still arrive.** St Kilda lost **45–69% of newborns per decade to neonatal tetanus for roughly 150 years**, arising from a local umbilical-care practice rather than from isolation or inbreeding. The practice stopped and infant deaths reached zero by the 1920s — and the island was evacuated in 1930 anyway, because the age-structure hole left by five generations of lost children could not be refilled once the young adults emigrated. **Demographic damage persists long after its cause is removed.** A simulation that lets a settlement bounce back immediately once a hazard is fixed will miss this entirely; the lag is the story.

**4. Exchange networks carried partners, not just goods.** The prehistoric Polynesian colonies on Pitcairn and Henderson traded basalt, volcanic glass, pearl shell, and red feathers along a network centred on Mangareva — and the archaeological account is explicit that **marriage partners were exchanged along the same routes.** When Mangareva withdrew from the network in the 16th century, the satellites lost material supply and gene flow together, and both colonies died after five centuries of successful occupation. This is precisely §C-2's finding, observed rather than modelled.

**5. Isolated communities invent institutions to manage their own genetics — and this is December's thesis in miniature.** Palmerston Island was founded in 1863 by **four effective people**: one man and three Polynesian wives, two of whom were cousins. It produced over a thousand descendants. It did so by organising itself into **three exogamous branches with intra-branch marriage prohibited** — an invented kinship rule that structured mating away from the closest available unions.

Tristan da Cunha shows the same behaviour without the formal rule: a measured **heterozygote excess**, with a "pattern of homozygote deficiency suggestive of avoidance of close matings."

This is precisely the emergence December exists to produce — a material constraint (a shrinking pool of unrelated partners) generating a durable institution (an exogamy rule) that residents create, transmit, and enforce. It should therefore be **available to agents, not imposed by the kernel**. The kernel supplies the kinship graph and the consequences; whether residents notice the problem, propose a rule, get it adopted, and keep it enforced across generations is exactly the kind of question the project is built to answer. If a December settlement independently invents an exogamy institution under demographic pressure, that is a stronger result than any governance outcome currently listed in the success criteria.

**A precision point on where the fitness cost lands.** Couples who are cousins show *no* net fertility reduction — reproductive compensation absorbs it, and the Hutterite pattern (longer interbirth intervals, longer time to conception, no fetal-loss increase, no change in completed family size) is the mechanism. But individuals who are *themselves* inbred do show reduced fertility. **The cost therefore lands one generation downstream of the consanguineous union**, not on the couple that made it. That lag is both well-evidenced and dramatically more interesting to simulate than an immediate penalty, because it means the consequences of a marriage rule surface only after the people who set it are gone.

**The recurring killer is network severance, not headcount.** This is the single most useful pattern in the historical record and it converges exactly on §C-2:

- Henderson Island and Polynesian Pitcairn sustained themselves for centuries and then died as **dependent nodes whose supply network failed** — both were satellites of Mangareva, and when Mangareva's network collapsed they could not stand alone.
- Norse Greenland is structurally the same failure: regular Norwegian shipping ceased after the 1370s, and the ivory trade that had given Greenland a near-monopoly in western Europe collapsed when North Atlantic commerce shifted to bulk dried fish. Researchers call it a "rigidity trap."
- Lynnerup's arithmetic on the Western Settlement is the sharpest version: at 600–800 people, **8–13 net emigrants per year — roughly one household — empties it in 200 years with no catastrophe at all.** A settlement near the viability floor does not need a disaster; it needs only a slow leak.

**A caution against overstating the genetics.** The Norse Greenland "degeneration" hypothesis — small stature, inbred skulls — originated in 1920s racial anthropology, and modern reanalysis rejects it: the notorious "inbred monstrosity" skull was re-diagnosed as acromegaly, the claimed 6.5% stature decline "cannot be proven" because different regression equations were used across sites, and the definitive biological-anthropological study explicitly lists **degeneration among the causes that can be *rejected***. What the skeletal record does show is modest: life expectancy at 20 fell ~1.5–3 years between early and late sites, concentrated in young adult females — and, tellingly, a possible **decline in the sex ratio**, since in a population this small "a chance series of death events may lead to extinction."

That last point is the real lesson. **Small populations die from mate-availability failures and chance sex-ratio skews long before they die from inbreeding depression** — which is precisely why §C-3's requirement for an explicit mate-availability model is the load-bearing one, not the inbreeding coefficient.

### C-5. Consequences for the plan — revised

1. **The neighboring aggregate group is mandatory at Phase 3**, and the *exchange and migration* path must be validated before the raiding path is built. A boundary world introduced only as a threat would make the neighbors a hazard generator, which [`07`](07-time-emergence-and-observation.md) forbids.
2. **One neighbor of similar size is not sufficient.** Two settlements of 18 give a combined pool of ~36 — roughly a quarter of the minimum viable network. The scenario needs either a substantially larger neighbor, several neighbors, or an **episodic regional aggregation** connecting the valley to a wider pool. The last option is ethnographically standard (the periodic-aggregation tier of ~165) and is the recommended design: a seasonal gathering that residents travel to, which supplies partners, news, trade, disease, and diplomacy in one mechanic.
3. **Marriage rules are the dominant lever on viability** — tightening them raises the required population 2.25–3.25×, far more than any other factor. December's kinship model is therefore not flavor; it is the parameter that most determines whether the world persists. It needs its own sensitivity sweep.
4. **A mate-availability model is mandatory.** A demographic simulation without explicit partner matching will badly *understate* extinction risk — the audit's own quick Monte Carlo using verified vital rates but no marriage rules returned only ~1% extinction over 200 years, which is wrong for exactly this reason. Do not build vital rates without pairing.
5. **Fertility must not encode the wrong story.** Foragers and horticulturalists have statistically indistinguishable TFR (5.6 vs 5.4, p=0.8); only *intensive* agriculture adds ~1 birth. But sedentism within a population raises fertility ~17% while raising child mortality ~63% — a quantity/quality trade, not a free gain. December's settlement is sedentary and pre-plough, so the horticulturalist band (TFR 6.0–6.5, IBI 30–34 months) is the right default.
6. **Null-model comparison remains mandatory** ([`09`](09-validation-and-experiments.md)).

---

## D. Disease

**This section invalidated part of the original design and is unchanged from the first pass.** Full sourcing in [`13`](13-sources.md).

### D-1. Critical community size

| Parameter | Central | Range | Unit | Context | Class |
|---|---|---|---|---|---|
| CCS, measles (Bartlett) | 275,000 | 250,000–300,000 | persons | US/UK cities, pre-vaccine | V |
| CCS, measles (Black, islands) | 400,000 | 300,000–500,000 | persons | Transmission broke in every community below 500,000 | V |
| CCS, pertussis | ~390,000 | 387,000–1,460,000 | persons | | V |
| Crowd-disease population floor | "several hundred thousand" | — | persons | Wolfe, Dunavan & Diamond 2007 | V |

**December's population is four orders of magnitude below the measles CCS.** No acute, directly transmitted, immunizing infection can be endemic in eighteen people. This is arithmetic over a seventy-year literature, mechanistically confirmed. An 18-person group produces roughly one birth every 1.5–3 years while measles needs new susceptibles on a two-week timescale.

### D-2. The five-mechanism health model

A single generic SEIR pathogen will either fade out immediately and contribute nothing, or — if tuned until epidemics appear at a satisfying frequency — encode a rate that cannot exist. That would be risk **R-07** in epidemiological costume.

| Mechanism | Persists because | Role in December |
|---|---|---|
| **Introduced acute epidemics** | It does not — burns through and ends | Rare punctuated shocks tied to contact events |
| **Environmentally transmitted** | Environmental reservoir; CCS does not apply | The persistent, self-generated disease pressure |
| **Zoonoses with animal reservoirs** | Animal reservoir | Rodent-borne risk from the settlement's own grain stores |
| **Chronic and latent infection** | The host is the reservoir | Background burden at any population size |
| **Helminths and parasites** | Faecal-oral and environmental cycling | Emergent consequence of sedentism and sanitation |

### D-3. Parameters and the finite-population outbreak requirement

| Parameter | Central | Range | Unit | Context | Class |
|---|---|---|---|---|---|
| Contact-epidemic mortality | 18 (median) | <1–97 | % of group | 117 epidemics, 59 Amazonian societies | V |
| Median affected population | 180 | — | persons | **Closest scale analogue to December** | V |
| Inter-epidemic period | 7 | rises with time since contact | years | | V |
| Epidemic causes | measles 37, influenza 25, malaria 13 | — | % of epidemics | | V |
| Measles attack rate, virgin soil | 77.5 | — | % | Faroe Islands 1846 | V |
| Measles CFR, adequate care | 2.8 | — | % of cases | Faroe Islands 1846 | V |
| Measles mortality, care collapse | 22 | 20–25 | % of population | Fiji 1875 — same pathogen, 10× the deaths | V |
| TB lifetime reactivation | 10 | 5–15 | % of latent | Elevated by malnutrition | V |
| Helminth prevalence, foragers vs farmers | 6 vs 76 | — | % Ascaris | **Same ecosystem; sedentism is the variable** | V |
| Child deaths attributable to undernutrition | 52.5 | 44.8–60.7 | % | | V |

**R₀ is not a pathogen constant** — measles estimates span 3.7–203.3 because R₀ is a function of social organization. Published values are upper bounds, not inputs; model contact structure and let the effective reproduction number emerge.

**Introduced acute outbreaks at n=18 should often show strong fade-out-versus-large-outbreak behavior across ensembles.** Under a simple early branching-process approximation with one index case, extinction probability is approximately `1/R₀`; the final-size values below are large-population approximations, not exact invariants for eighteen heterogeneous people:

| R₀ | Final attack rate | P(fade-out) |
|---|---|---|
| 1.5 | 58% | 67% |
| 2.0 | 80% | 50% |
| 3.0 | 94% | 33% |
| 5.0 | 99% | 20% |
| 12.0 | ~100% | 8% |

Many introductions should fizzle and some should affect much of the group; intermediate outbreaks remain possible in a finite, structured contact network. Validate the full stochastic distribution rather than only its mean, and do not mark an intermediate outcome as a bug solely because it differs from this approximation.

---

## E. Violence — the range spans an order of magnitude and the dispute is substantially definitional

**This is the section where December must be most careful, because the temptation to pick a number is strongest and the literature least supports doing so.**

| Source | Statistic | Value | Sample | Class |
|---|---|---|---|---|
| Keeley 1996 | % of all deaths from war | 7–40 | 9 archaeological cases | V, C |
| **Bowles 2009** | Fraction of adult mortality due to war (δ) | **mean 0.14, median 0.12** | 15 archaeological + 8 ethnographic | V, C |
| Bowles 2009, range | δ | 0.00–0.46 | Gobero 0.00 → Jebel Sahaba 0.46 | V |
| Pinker 2011 | % deaths, prehistoric sites | mean 15, range 0–60 | 21 cases compiled from Keeley + Bowles | V, C |
| Pinker 2011 | Annual war deaths | 524 per 100,000 | Non-state societies | V, C |
| Gat 2006/2015 | Violent death rate | ~25% of adult males, ~15% of adults | HGs + pre-state horticulturalists | V, C |
| **Fry & Söderberg 2013** | **Lethal aggression events** | **148 events; median 4/society; range 0–69** | 21 mobile forager band societies | V |
| Fry & Söderberg 2013 | Events classified intergroup | 33.8% overall; **15.2% excluding Tiwi** | | V |
| Ferguson 2013 | Pinker's list after audit | **21 cases → 14** | Duplicates, single deaths, misreadings removed | V |
| Jurmain, via Ferguson | Jebel Sahaba recount | **9.8%** vs Bowles's 46% | 4 of 41 complete skeletons | V |
| Meijer 2024 | Prehistoric HG lethal violence | notes ~2–3% of deaths, declines to endorse | Global archaeological review | V |

### E-1. Why the numbers cannot simply be averaged

**The two flagship papers do not report the same statistic.** Bowles reports war deaths as a fraction of all deaths. Fry & Söderberg report *counts of lethal events classified by motive* and **never compute a mortality rate at all**. They are routinely presented as opposing estimates of one quantity. They are not.

**Six of Bowles's eight ethnographic societies also appear in Fry & Söderberg's twenty-one** — the same societies, opposite conclusions. That difference is definitional, not empirical. Bowles defines war as any coalitional lethal action across group boundaries, explicitly including revenge killings; Fry & Söderberg follow Kelly in requiring *social substitutability* (any member of the offending group being a legitimate target), which reclassifies much of the same behavior as feud or homicide.

**The denominators differ too**: Keeley counts all individuals, Bowles counts adults only, Gat's 25% is of adult males, and frequently cited trauma figures (57.3% of Australian crania; 10.91% Neolithic cranial trauma) count *injuries*, mostly healed, not deaths. Four different quantities, routinely juxtaposed.

**Both headline results are leveraged on outliers.** A single society, the Tiwi, supplies 69 of Fry & Söderberg's 148 events and 38 of their 50 intergroup events; removing it halves the mean and cuts the range from 0–69 to 0–15. On the other side, Ferguson's audit removed 7 of Pinker's 21 cases as duplicated sites, single deaths, or misread evidence.

**Sample composition is a deliberate choice on both sides.** Bowles knowingly included sedentary hunter-gatherers and seasonal forager-horticulturalists (3 of his 8); Fry & Söderberg deliberately excluded them. Fry's earlier work found 62% of mobile forager band societies non-warring while *all* complex and equestrian forager societies had war. Most of the famous archaeological massacre sites — Crow Creek, Talheim, Schöneck-Kilianstädten, Asparn/Schletz, Potočani — are **farming societies**, not foragers, and bear on a different question than the one they are cited for.

**Jebel Sahaba is the cautionary tale.** The single most-cited site has been reported at 46%, 40.7%, and 9.8% of deaths, and a 2021 microscopic reanalysis of all 61 individuals found *more* total violence than previously documented while concluding the evidence "dismisses the hypothesis that Jebel Sahaba reflects a single warfare event," supporting recurrent raiding instead. The same site supports opposite headlines depending on whether you count trauma or count events.

### E-2. What December must do

**Treat conflict frequency as an output, not a direct input knob.** Sweep mechanisms that could produce it—resource pressure, mobility, group boundaries, threat sensitivity, dominance motives, institutional effectiveness, retaliation, logistics, and provider refusal—and compare the resulting outputs with broad contested reference ranges. Concretely:

1. **Pick and publish a definition before running anything.** December must state whether it counts coalitional cross-boundary killing (Bowles) or requires social substitutability (Kelly/Fry), and it must count events *and* mortality fractions separately, with explicit denominators. Most of the published disagreement is exactly this choice, so making it silently would be inheriting a position without argument.
2. **Sweep mechanisms, and report outcome distributions.** The literature spans roughly 2% to 25% of deaths depending on definition, denominator, and society type. December must not choose a target rate and tune until it appears.
3. **Claim nothing about human nature.** The prohibition in [`09`](09-validation-and-experiments.md) is reinforced: because the empirical range is an order of magnitude wide and partly definitional, December's simulated conflict rate carries **no evidentiary weight in either direction**. It cannot show that violence is natural, and it cannot show that peace is.
4. **What December *can* honestly demonstrate** is the structural finding both sides accept: that sedentism, population density, storable and defensible resources, and social segmentation are associated with more organized violence. That is common ground across Kelly, Fry, Ferguson, Meijer, and Gat, and it is a mechanism December actually models. Showing conflict emerging from *those* pressures is a defensible result; showing it at a particular rate is not.
5. Risks **R-11** (conflict as entertainment) and **R-07** (catastrophe machine) both bite here, and the refusal-rate requirement in [`16`](16-cost-model-and-model-selection.md) §6 applies to every conflict statistic.

The most honest summary available comes from Ferguson, a partisan of the low side, in two consecutive sentences: anyone believing violence began with colonialism, the state, or agriculture is proven wrong — and equally, anyone believing all human societies were plagued by war is proven wrong. Recent reviews (Meijer 2024, Glowacki 2023) conclude the debate is at an impasse that the archaeological record probably cannot resolve, and that **the true finding is the variance itself**.

---

## F. Movement

| Parameter | Central | Range | Unit | Context | Class |
|---|---|---|---|---|---|
| **Tobler's hiking function** | `W = 6·exp(−3.5·|S + 0.05|)` | — | km/h | **S = rise/run**, not percent or degrees | V |
| Tobler, flat ground | 5.04 | — | km/h | | D |
| Tobler, maximum | 6.00 | at S = −0.05 | km/h | Slight downhill is fastest | D |
| Tobler, off-path multiplier | ×0.6 | — | — | Tobler's own text | V |
| Tobler vs measured | −34 | — | % (predicts too fast) | 200 GPS-tracked walkers | V |
| Tobler percentile | ~5th | — | percentile | Against 29,928 Strava users — it is a *slow* walker | V |
| Naismith's rule | 1 h/5 km + 1 h/600 m ascent | — | — | **Sample size: n=1**, a club trip report | V, C |
| Langmuir gentle descent (5–12°) | −10 | — | min/300 m | Subtract | V |
| Langmuir steep descent (>12°) | +10 | — | min/300 m | Add; **creates a discontinuity at 12°** | V |
| **Sustainable load, non-specialist** | 25 | 20–30 | % body mass | Multi-day walking | V |
| Fighting / approach-march load | 30 / 45 | — | % body mass | Military doctrine | V |
| "Free ride" below 20% body mass | — | — | — | **82% of 45 studies fail to replicate it** | V, C |
| Professional porter load | 85 | 80–200 | % body mass | Lifelong specialists; −20% metabolic cost | V |
| **Loaded travel, sustainable** | 26 | 20–32 | km/day | Roads, daylight | V |
| Forced march, 24 / 48 / 72 h | 56 / 96 / 128 | — | km cumulative | **Note the sublinearity** | V |
| Hadza daily distance | M 11.4–12.9 / F 5.8–7.6 | — | km/day | GPS, two studies | V |
| Hadza foraging trip | M 8.3 / F 5.5 | — | km | | S |
| **Max comfortable daily round trip** | 25 | 20–30 | km | Hunters, many habitats | S |
| Foraging radius before camp move | 6 | 1.5–10 | km | **Function of camp-move cost** | S |
| Load speed penalty | −28 | — | % (1.25 → 0.9 m/s) | !Kung women carrying ~30% body mass | V |
| Walking speed, dense forest | 1.67 | — | km/h | | V |

### Design note F-1 — the depletion halo is a documented, directly implementable mechanic

The !Kung record gives December its ecology-and-labor coupling almost for free. A camp exhausts mongongo nuts within **1.5 km in week 1, 3 km in week 2, and 5 km in week 3**; measured daily round trips rose from 9–14 km in June to 19 km by August. Foraging radius before a camp move is not a constant but a function of move cost — a two-hour camp breakdown makes it worth exhausting resources within ~6 km, while a half-hour breakdown makes moving worthwhile at 1.5 km.

Combined with Tobler's terrain-sensitive travel times, this produces the continuously rising subsistence cost that [`03`](03-world-model-and-scenario.md) wants from its ecology — not a stepwise "resource depleted" flag, but a slowly tightening squeeze that residents can perceive, argue about, and respond to by moving, intensifying, or fighting. It should be an explicit Gate 1 pattern target.

Two implementation cautions: **Tobler's S is rise/run** — published archaeology has got this wrong by a factor of 100 — and Tobler predicts roughly a 5th-percentile walker, ~34% faster than GPS-measured off-road speeds, so it is a *slow* baseline rather than a median one. The forced-march sublinearity (56 km on day 1, only 40 more by day 2, only 32 more by day 3) is the most useful single fact for modelling multi-day journeys.

---

## Gaps this registry does not close

1. **No crop phenology parameters** — stage durations, temperature and moisture thresholds, damage functions. Needed at Phase 1.
2. **No hydrology parameters** — infiltration, runoff, baseflow recession, irrigation efficiency.
3. **No construction labor figures** — person-days per structure type, the direct input to the project compiler in [`05`](05-society-economy-governance-conflict.md). The swidden labor breakdown in §B is the closest available analogue.
4. **No stone-tool forest clearance rate** — sought and not found; use the swidden slashing-and-felling column (9–75 person-days/ha) as the stand-in.
5. **No tool wear or maintenance rates.**
6. **No skill acquisition curves** — the "diminishing returns" in [`04`](04-agents-cognition-and-memory.md) remains unparameterized.
7. **Fire spread parameters** deferred to Phase 5, entirely open.
8. **Pre-modern road-network travel rates** (Roman/medieval) — not obtainable in this pass.

Items marked **N** or **S** above are the ones to verify first. Every gap that ships uncalibrated becomes a registry row with `source: NONE — DESIGNED`, disclosed in the known-limit report required at canonical launch.
