# December

**A world that keeps living.**

*A 13-minute introduction. The full specification is in [`wiki/`](wiki/); this is the version you read first.*

---

Eighteen people live in a valley. They farm, hunt, argue, build, make promises, break them, fall ill, have children, and die. Nobody is watching most of the time.

You come back after two days and something has happened. A dry season thinned the stream; the council rationed water; two households held grain back; a child's testimony changed a vote; the losing steward left with four followers and camped at the weir upstream. Three people were hurt in the confrontation. The people who nursed them caught what they had.

The point is not that this story is dramatic. The point is that **you can ask why, and get an answer made of evidence rather than narration.** Every clause in that paragraph resolves to a recorded event with a cause, a timestamp, an actor, and — where chance was involved — the exact random draw that produced it. You can walk backwards from the injury to the confrontation to the vote to the rainfall. You can ask what any resident knew at any moment, and be told only what they could actually have known.

That property, and not the story, is what December is for.

## 1. The problem with agent societies

Put several language models in a room, give them names and backstories, and they will produce something that reads like a society. They will negotiate, form alliances, betray each other, and write you a very good chronicle of it afterwards.

The trouble is that none of it is load-bearing. Language models are extraordinary at sounding like people and hopeless at being ledgers. Ask a model to narrate a world and grain appears from nowhere, a character is in two places on the same afternoon, a wall gets built in an evening, and a war starts because a war was the interesting thing to write next. Nothing is conserved, so nothing is at stake.

The deeper failure is epistemic. When such a society produces a war, you cannot tell whether it happened *because* the harvest failed or because "war" was simply a plausible next paragraph. The history is unfalsifiable. It cannot surprise you, because it could have gone any way at all, and you would have believed that too.

Everything below follows from taking that problem seriously.

## 2. One commitment: the simulator owns truth

December has a typed, deterministic kernel that owns all authoritative state — every gram of grain, every person's location, every claim on a field, every hour of the day. The kernel is not clever. It does arithmetic, checks preconditions, and refuses things.

Language models never touch it. A resident's model receives a private observation packet — what that person can see, remember, and has been told — and proposes an action in a fixed schema. The kernel validates the action against reality and either performs it, rejects it, or returns what would be possible instead. Prose describes the world. It never determines it.

This sounds like a limitation on the models. It is the opposite. **A choice only means something if it could have failed.** When a resident decides to give away food during a shortage, that decision is interesting precisely because the food is finite, the ledger is real, and the cost will arrive later whether or not anyone narrates it. Remove the constraint and the generosity is just a nice sentence.

The same commitment produces the causal graph. Because every change to the world is an event with recorded parents — this rainfall caused that soil moisture, this observation caused that decision, this rule authorised that transfer, this random draw produced that infection — you can reconstruct the reasoning for any outcome without asking a model to speculate about it afterwards. When the system says someone died of a wound infection following a fight over water, that is a query result, not an interpretation.

There is a read-only narrator, which we call the director. It writes summaries, ranks what mattered, and points a camera. It cannot change anything, and any claim in its summaries that isn't backed by a cited event is rejected before you see it. If it ever needed the power to make things happen in order to keep the world interesting, the project would have failed on its own terms.

## 3. What eighteen people can and cannot be

The settlement begins with twelve adults and six dependants. This number is not a gameplay choice; it is small enough that every person can be simulated with real interiority and large enough for households, factions, and disagreement.

It is also, honestly, below every published threshold for a viable isolated human population. Simulations of forager demography put the floor around forty people and near-certainty around a hundred and fifty. With twelve breeding adults, inbreeding accumulates at roughly four percent per generation — four times the rate conservation biologists consider tolerable — and by the third generation every child is more closely related than the offspring of first cousins.

And yet. Pitcairn Island was founded in 1790 by twenty-seven people and still exists. Tristan da Cunha was founded by about fifteen and still exists, carrying a thirty-six percent asthma rate two centuries later as the price. Rapa Nui fell to roughly a hundred and ten people in 1877 and recovered.

So the honest position is that eighteen people is **marginal rather than impossible** — and the interesting question is what makes the difference. The historical record answers it consistently: not headcount, but **connection**. The colonies that failed — Norse Greenland, the Polynesian settlements on Henderson and Pitcairn — died when their networks were severed, not when their numbers were low. Greenland's western settlement, six to eight hundred people, could be emptied in two centuries by about one departing household a year. No catastrophe required.

This reshapes the design. The neighbouring group is not primarily a source of raids and disease; it is the settlement's lifeline, and it has to exist early rather than late. Partner exchange, in-migration, and a seasonal regional gathering are load-bearing mechanics. A world where the neighbours only ever show up to fight would be a hazard generator wearing a costume.

Scale honesty cuts the other way too, and this is where most simulations quietly cheat. Consider disease. The number of people required to sustain an acute immunising infection like measles — the critical community size — is somewhere between two hundred fifty thousand and five hundred thousand. December has eighteen. Four orders of magnitude short.

So a conventional epidemic model, run at this scale, does one of two things: it fades out immediately and contributes nothing, or it gets tuned until epidemics appear at a satisfying rate. The second option is fabricated epidemiology wearing the costume of rigour, and it would be very easy to ship.

Instead the health model is rebuilt around what can actually persist in eighteen people: chronic and latent infections, where the host is the reservoir; environmentally transmitted disease, where the reservoir is the water; zoonoses, where the reservoir is an animal; and parasites, which accumulate with sedentism. Acute epidemics still happen, but only as rare introductions from outside contact, and they behave the way virgin-soil epidemics actually behave — either the infection fails to take hold at all, or it takes nearly everyone. There is no average epidemic at this scale, and any implementation producing one has a bug.

That correction made the design better, not smaller. The persistent disease pressure now comes from the settlement's own decisions about water, waste, and storage. Two populations living in the same ecosystem can differ tenfold in parasite load depending on whether they stay put. **The settlement's success at storing grain is what brings the rats.**

## 4. Why the seed grain matters more than the government

If you want to know where December expects its drama to come from, it isn't the constitution. It's a ratio.

In medieval European agriculture — the best-documented premodern cereal record, tens of thousands of manor-year observations — a field returned about three and a half to four grains for every grain sown. That means **roughly twenty-seven percent of every harvest has to be taken away from hungry people and put back in the ground.** Contemporary estate managers used a three-to-one return as their break-even line, which tells you how close to the edge the whole arrangement ran. In something like one field-year in fourteen, the yield is bad enough that half the harvest must be withheld.

Sit with what that does to a settlement in a bad autumn. Eating the seed corn is available, immediately rational, and catastrophic on a twelve-month delay. Nobody has to be villainous. The trap is arithmetic.

Hunting works the same way and produces the opposite social result. Measured return rates among Hadza hunters have a coefficient of variation above eight: a hunter targeting large game comes home with nothing on more than ninety-seven percent of days. The settlement eats meat because *someone* succeeds, never because anyone reliably does. That is not a colourful detail — it is the reason food sharing, reciprocity, and obligation networks exist at all. A simulation that hands hunters their average return has deleted the reason for society while appearing to model hunting correctly.

Grinding grain by hand runs around seven-tenths of a kilogram an hour, which for a household means three to five hours every single day, forever, falling almost entirely on women in every ethnographic case on record. If you model fields and harvests but not processing, you have silently handed the settlement several free person-hours a day and misrepresented who is doing the work.

The pattern in all three: **the institutions we hope to see emerge should be forced by material facts, not offered as a menu.** There is no democracy module. There is a bounded grammar for making rules, offices, and obligations, and there are pressures that make rule-making worth the trouble.

The clearest evidence that this works comes from Palmerston Island, settled in 1863 by four people — one man and three women, two of whom were cousins. It produced over a thousand descendants. It did that by organising itself into three exogamous branches with marriage inside a branch forbidden: an invented kinship rule, transmitted and enforced across generations, that solved a genetic problem the founders could perceive but not name.

That is precisely the shape December is built to produce. A material constraint — a shrinking pool of unrelated partners — generating a durable institution that nobody designed in advance. If a settlement independently arrives at an exogamy rule under demographic pressure, that will be a more convincing result than any election, because the pressure is measurable, the mechanism is legible, and the settlements that *fail* to invent it are visible in the same experiment.

## 5. What we refuse to claim

A project like this attracts overclaiming, so the limits are worth stating as plainly as the ambitions.

**This is not a model of real human societies.** It is a fictional valley with invented parameters, many borrowed from populations that have nothing to do with it. Nothing December produces is evidence about how people actually behave, and no result should ever be used to argue about real communities.

**Simulated conflict rates carry no evidentiary weight.** The scholarly literature on violence in small-scale societies spans an order of magnitude, and much of that disagreement turns out to be definitional rather than empirical — the two most-cited papers on opposite sides do not even report the same quantity, and six of the same societies appear in both with opposite conclusions. December's conflict rate is a design choice inside a contested range. It cannot show that violence is natural, and it cannot show that peace is.

**We are not studying consciousness, and we are not studying whether a person could survive being copied.** Those questions motivate the work and are not tested by it. A resident who maintains a coherent identity across a model swap has demonstrated something about persistent synthetic agency. It has demonstrated nothing whatsoever about experience. The distance between those two claims is the whole distance, and we do not intend to blur it.

**A behavioural finding might be a fact about the model provider.** If residents rarely escalate a conflict, that could be the world working — or it could be the safety training of whichever model is playing them. So refusal rates are measured and reported alongside every behavioural result. A conflict statistic without its refusal denominator is uninterpretable.

**Reproducibility has a precise meaning.** Given the same code, configuration, and recorded model responses, a history replays to identical state. That works because every quantity in the world is an integer — grams, millilitres, seconds — so nothing depends on how a particular machine rounds a decimal. No language model provider offers reproducible sampling, so the recorded responses are part of the permanent record rather than a cache; a replay that cannot find one fails loudly instead of quietly inventing a different history.

## 6. How you would know if it worked

The hardest problem in a project like this is not building it. It is telling the difference between a world that produced something and a world that was arranged to produce it.

Three habits guard against that.

**The founding state is declared, randomised, and varied.** An earlier draft of the scenario described the founders as disagreeing about property, leadership, and risk, with land claims left conveniently ambiguous. That is not a starting condition; it is the plot, pre-installed. If the settlement later fractures over property and elects someone to sort it out, we would have observed only what we planted. So the initial world specifies quantities, locations, relationships, and capabilities — never dispositions toward a future conflict — and it is generated from a recorded seed so that experiments can vary it. Randomising does not make it unauthored: the distributions, the constraints, and the seeds we accept are all research decisions, and they are written down.

**Every claimed cascade is measured against a null model.** With eighteen people, births and deaths are single digits per decade, so variance rivals the mean and a meaningful fraction of worlds will simply die for no interesting reason. Unless a collapse is compared against the same demography with no social mechanisms at all, "the faction dispute destroyed the settlement" is indistinguishable from "a settlement of eighteen people collapsed, and there happened to be a faction dispute."

**Labels are defined before the runs, not after.** Words like *faction*, *war*, and *governance form* need structural definitions — readable off the institution registry, with persistence requirements — fixed in version control before the experiments that use them. A definition chosen after seeing the results is not a finding.

Beyond that, the criteria are ordinary: histories should differ across seeds; removing a mechanism should measurably change outcomes; residents with different values and histories should make measurably different decisions rather than becoming one personality wearing twelve names; and a week of unattended running should require no human repair.

And there is one clean failure condition. **If the world needs a storyteller to stay interesting, it has failed.** Quiet seasons are allowed. A world that is only compelling when someone is secretly arranging events is a very expensive way to write fiction.

## Where it stands

The design is complete and has been through two independent adversarial audits, the second of which corrected the first on several points, including some it had gotten confidently wrong.

Implementation has started at the foundation rather than the scenery. What exists today is the part that cannot be retrofitted: integer-valued world state, a tamper-evident chain of events, reproducible random streams, an append-only history, and a replay path that reconstructs the world exactly. It runs on a deliberately trivial world — grain moving between containers — because the point of a foundation is to be tested before anything is built on it.

There is no ecology yet, no people, no cognition. Nothing is alive.

The nearest milestone is a headless world with weather, water, crops, and demography, running thousands of times with no language models involved at all, to find out which settlements survive and why before any resident is asked to make a single decision.

---

*Details, sources, and the reasoning behind every choice above are in [`wiki/`](wiki/). The audits are in [`AUDIT-FINDINGS.md`](AUDIT-FINDINGS.md) and [`AUDIT-FINDINGS-PASS-2.md`](AUDIT-FINDINGS-PASS-2.md), including the parts where they disagree.*
