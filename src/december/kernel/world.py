"""A deliberately small world: grain containers and scripted residents.

This is the walking skeleton. It has no ecology, no people, and no cognition.
Its only job is to exercise the parts of the architecture that cannot be
retrofitted later — integer state, the command pipeline, hash-chained events,
named RNG streams, conservation with a declared sink, and snapshot/replay.

The residents in this module are bodies, not minds. Their typed movement and
activity events exist so the observer can consume honest kernel output before
cognition is introduced. Everything ecological and cognitive comes later.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from ..domain.units import Grams, apply_rate, quantize
from .canonical import encode
from .events import Event
from .rng import StreamRegistry
from .store import EventStore


class PreconditionFailed(ValueError):
    """A command was rejected because the world does not permit it.

    Rejections carry only information the actor could already observe. Leaking
    a hidden quantity through a rejection reason would violate the epistemic
    contract R3 — the failure mode recorded as F-14 in the first audit.
    """


@dataclass(slots=True)
class Resident:
    """The minimum authoritative body state needed by the first observer."""

    resident_id: str
    name: str
    role: str
    x_millimetres: int
    y_millimetres: int
    activity: str
    energy_kilojoules: int
    hydration_millilitres: int
    health_ppm: int
    alive: bool


@dataclass(slots=True)
class World:
    """Authoritative state.

    `containers` holds live grain; `spoiled_total` is a declared sink. Together
    they must always sum to the total ever created, which is the conservation
    invariant the property tests assert.
    """

    containers: dict[str, int] = field(default_factory=dict)
    water_containers: dict[str, int] = field(default_factory=dict)
    residents: dict[str, Resident] = field(default_factory=dict)
    spoiled_total: int = 0
    consumed_total: int = 0
    created_total: int = 0
    water_consumed_total: int = 0
    water_created_total: int = 0
    sim_time: int = 0

    def total_live(self) -> int:
        return sum(self.containers.values())

    def check_conservation(self) -> None:
        """Assert that nothing has been created or destroyed off-ledger."""
        accounted = self.total_live() + self.spoiled_total + self.consumed_total
        if accounted != self.created_total:
            raise AssertionError(
                f"conservation violated: live {self.total_live()} + "
                f"spoiled {self.spoiled_total} + consumed {self.consumed_total} = {accounted}, "
                f"but {self.created_total} was created"
            )
        water_live = sum(self.water_containers.values())
        water_accounted = water_live + self.water_consumed_total
        if water_accounted != self.water_created_total:
            raise AssertionError(
                f"water conservation violated: live {water_live} + consumed "
                f"{self.water_consumed_total} = {water_accounted}, but "
                f"{self.water_created_total} was created"
            )

    def state_hash(self) -> bytes:
        """Canonical full-state hash, computed at snapshots.

        Containers are sorted by id so the digest cannot depend on dict
        insertion order — the kind of latent nondeterminism wiki/14 §D2 bans.
        """
        payload = {
            "containers": sorted(self.containers.items()),
            "water_containers": sorted(self.water_containers.items()),
            "residents": [
                {
                    "resident_id": resident.resident_id,
                    "name": resident.name,
                    "role": resident.role,
                    "x_millimetres": resident.x_millimetres,
                    "y_millimetres": resident.y_millimetres,
                    "activity": resident.activity,
                    "energy_kilojoules": resident.energy_kilojoules,
                    "hydration_millilitres": resident.hydration_millilitres,
                    "health_ppm": resident.health_ppm,
                    "alive": resident.alive,
                }
                for _, resident in sorted(self.residents.items())
            ],
            "spoiled_total": self.spoiled_total,
            "consumed_total": self.consumed_total,
            "created_total": self.created_total,
            "water_consumed_total": self.water_consumed_total,
            "water_created_total": self.water_created_total,
            "sim_time": self.sim_time,
        }
        return hashlib.blake2b(encode(payload), digest_size=32).digest()


class Kernel:
    """The command pipeline.

    Commands are validated against authoritative state, then produce events.
    Nothing mutates state except `_apply`, which is also what replay calls — so
    a replayed history and a live one cannot diverge through separate code
    paths.
    """

    def __init__(self, store: EventStore, rng: StreamRegistry, code_version: str = "dev") -> None:
        self._store = store
        self._rng = rng
        self._code_version = code_version
        self.world = World()

    # -- transitions ----------------------------------------------------

    def _apply(self, event: Event) -> None:
        """The single mutation point. Used by both live commands and replay."""
        p = event.payload
        match event.event_type:
            case "grain.created.v1":
                self.world.containers[p["container"]] = (
                    self.world.containers.get(p["container"], 0) + p["grams"]
                )
                self.world.created_total += p["grams"]
            case "grain.transferred.v1":
                self.world.containers[p["from"]] -= p["grams"]
                self.world.containers[p["to"]] = (
                    self.world.containers.get(p["to"], 0) + p["grams"]
                )
            case "grain.spoiled.v1":
                self.world.containers[p["container"]] -= p["grams"]
                self.world.spoiled_total += p["grams"]
            case "water.created.v1":
                self.world.water_containers[p["container"]] = (
                    self.world.water_containers.get(p["container"], 0) + p["millilitres"]
                )
                self.world.water_created_total += p["millilitres"]
            case "resident.created.v1":
                resident_id = p["resident_id"]
                self.world.residents[resident_id] = Resident(
                    resident_id=resident_id,
                    name=p["name"],
                    role=p["role"],
                    x_millimetres=p["x_millimetres"],
                    y_millimetres=p["y_millimetres"],
                    activity=p["activity"],
                    energy_kilojoules=p["energy_kilojoules"],
                    hydration_millilitres=p["hydration_millilitres"],
                    health_ppm=p["health_ppm"],
                    alive=p["alive"],
                )
            case "resident.moved.v1":
                resident = self.world.residents[p["resident_id"]]
                resident.x_millimetres = p["x_millimetres"]
                resident.y_millimetres = p["y_millimetres"]
            case "resident.activity_changed.v1":
                self.world.residents[p["resident_id"]].activity = p["activity"]
            case "resident.metabolized.v1":
                resident = self.world.residents[p["resident_id"]]
                resident.energy_kilojoules -= p["energy_spent_kilojoules"]
                resident.hydration_millilitres -= p["water_spent_millilitres"]
                resident.health_ppm -= p["health_lost_ppm"]
            case "grain.consumed.v1":
                resident = self.world.residents[p["resident_id"]]
                self.world.containers[p["container"]] -= p["grams"]
                self.world.consumed_total += p["grams"]
                resident.energy_kilojoules += p["energy_absorbed_kilojoules"]
            case "water.consumed.v1":
                resident = self.world.residents[p["resident_id"]]
                self.world.water_containers[p["container"]] -= p["millilitres"]
                self.world.water_consumed_total += p["millilitres"]
                resident.hydration_millilitres += p["water_absorbed_millilitres"]
            case "resident.died.v1":
                resident = self.world.residents[p["resident_id"]]
                resident.alive = False
                resident.activity = "Dead"
            case "world.time_advanced.v1":
                self.world.sim_time = p["sim_time"]
            case _:
                raise ValueError(f"unknown event type {event.event_type}")
        self.world.check_conservation()

    def _emit(self, event_type: str, payload: dict, **kw) -> Event:
        ev = Event(
            event_type=event_type,
            sim_time=self.world.sim_time,
            sequence=-1,  # assigned by the store
            payload=payload,
            code_version=self._code_version,
            **kw,
        )
        sealed = self._store.append(ev)
        self._apply(sealed)
        return sealed

    # -- commands -------------------------------------------------------

    def create_grain(self, container: str, grams: int) -> Event:
        """Source process. The only way grain enters the world."""
        if grams <= 0:
            raise PreconditionFailed("grams must be positive")
        return self._emit(
            "grain.created.v1",
            {"container": container, "grams": grams},
            entity_ids=(container,),
        )

    def transfer(self, src: str, dst: str, grams: int) -> Event:
        if grams <= 0:
            raise PreconditionFailed("grams must be positive")
        if src == dst:
            raise PreconditionFailed("source and destination are the same")
        available = self.world.containers.get(src, 0)
        if available < grams:
            # Observable to anyone who can see the container, so it is safe to
            # say the transfer is short without naming the hidden remainder.
            raise PreconditionFailed(f"container {src} does not hold {grams} g")
        return self._emit(
            "grain.transferred.v1",
            {"from": src, "to": dst, "grams": grams},
            entity_ids=(src, dst),
        )

    def create_resident(
        self,
        resident_id: str,
        name: str,
        role: str,
        x_millimetres: int,
        y_millimetres: int,
        activity: str,
        *,
        energy_kilojoules: int = 8_000,
        hydration_millilitres: int = 3_000,
        health_ppm: int = 1_000_000,
    ) -> Event:
        """Create a body. This does not create a cognitive agent."""
        if not resident_id or not name or not role or not activity:
            raise PreconditionFailed("resident fields must be non-empty")
        if resident_id in self.world.residents:
            raise PreconditionFailed("resident already exists")
        if x_millimetres < 0 or y_millimetres < 0:
            raise PreconditionFailed("resident position must be non-negative")
        if energy_kilojoules < 0 or hydration_millilitres < 0:
            raise PreconditionFailed("resident reserves must be non-negative")
        if not 0 < health_ppm <= 1_000_000:
            raise PreconditionFailed("resident health must be in (0, 1_000_000]")
        return self._emit(
            "resident.created.v1",
            {
                "resident_id": resident_id,
                "name": name,
                "role": role,
                "x_millimetres": x_millimetres,
                "y_millimetres": y_millimetres,
                "activity": activity,
                "energy_kilojoules": energy_kilojoules,
                "hydration_millilitres": hydration_millilitres,
                "health_ppm": health_ppm,
                "alive": True,
            },
            actor_ids=(resident_id,),
            entity_ids=(resident_id,),
        )

    def move_resident(self, resident_id: str, x_millimetres: int, y_millimetres: int) -> Event:
        """Record an accepted body movement to a position in the world."""
        resident = self.world.residents.get(resident_id)
        if resident is None:
            raise PreconditionFailed("resident does not exist")
        if not resident.alive:
            raise PreconditionFailed("resident is dead")
        if x_millimetres < 0 or y_millimetres < 0:
            raise PreconditionFailed("resident position must be non-negative")
        return self._emit(
            "resident.moved.v1",
            {
                "resident_id": resident_id,
                "x_millimetres": x_millimetres,
                "y_millimetres": y_millimetres,
            },
            actor_ids=(resident_id,),
            entity_ids=(resident_id,),
        )

    def set_activity(self, resident_id: str, activity: str) -> Event:
        """Record a typed, externally chosen activity for the scripted body."""
        if resident_id not in self.world.residents:
            raise PreconditionFailed("resident does not exist")
        if not self.world.residents[resident_id].alive:
            raise PreconditionFailed("resident is dead")
        if not activity:
            raise PreconditionFailed("activity must be non-empty")
        return self._emit(
            "resident.activity_changed.v1",
            {"resident_id": resident_id, "activity": activity},
            actor_ids=(resident_id,),
            entity_ids=(resident_id,),
        )

    def create_water(self, container: str, millilitres: int) -> Event:
        """Source process. The only way water enters the current world."""
        if millilitres <= 0:
            raise PreconditionFailed("millilitres must be positive")
        return self._emit(
            "water.created.v1",
            {"container": container, "millilitres": millilitres},
            entity_ids=(container,),
        )

    def metabolize(self, resident_id: str, seconds: int, activity_level_ppm: int = 1_000_000) -> list[Event]:
        """Consume bodily reserves and apply deprivation damage.

        Baseline rates are provisional Phase 1 parameters: 100 kJ and 100 ml
        per simulated hour. The activity multiplier is integer ppm.
        """
        resident = self.world.residents.get(resident_id)
        if resident is None:
            raise PreconditionFailed("resident does not exist")
        if not resident.alive:
            raise PreconditionFailed("resident is dead")
        if seconds <= 0 or activity_level_ppm <= 0:
            raise PreconditionFailed("metabolism duration and activity must be positive")
        energy_per_hour = apply_rate(100, activity_level_ppm)
        water_per_hour = apply_rate(100, activity_level_ppm)
        energy_required = max(1, (seconds * energy_per_hour + 3_599) // 3_600)
        water_required = max(1, (seconds * water_per_hour + 3_599) // 3_600)
        energy_spent = min(resident.energy_kilojoules, energy_required)
        water_spent = min(resident.hydration_millilitres, water_required)
        energy_deficit = energy_required - energy_spent
        water_deficit = water_required - water_spent
        health_lost = min(
            resident.health_ppm,
            energy_deficit * 250 + water_deficit * 500,
        )
        events = [
            self._emit(
                "resident.metabolized.v1",
                {
                    "resident_id": resident_id,
                    "duration_seconds": seconds,
                    "activity_level_ppm": activity_level_ppm,
                    "energy_spent_kilojoules": energy_spent,
                    "water_spent_millilitres": water_spent,
                    "health_lost_ppm": health_lost,
                },
                actor_ids=(resident_id,),
                entity_ids=(resident_id,),
            )
        ]
        if self.world.residents[resident_id].health_ppm == 0:
            events.append(
                self._emit(
                    "resident.died.v1",
                    {"resident_id": resident_id, "cause": "deprivation"},
                    entity_ids=(resident_id,),
                )
            )
        return events

    def eat(self, resident_id: str, container: str, grams: int) -> Event:
        resident = self.world.residents.get(resident_id)
        if resident is None or not resident.alive:
            raise PreconditionFailed("resident cannot eat")
        if grams <= 0 or self.world.containers.get(container, 0) < grams:
            raise PreconditionFailed("food is unavailable")
        absorbed = min(grams * 15, 12_000 - resident.energy_kilojoules)
        return self._emit(
            "grain.consumed.v1",
            {
                "resident_id": resident_id,
                "container": container,
                "grams": grams,
                "energy_absorbed_kilojoules": max(0, absorbed),
            },
            actor_ids=(resident_id,),
            entity_ids=(resident_id, container),
        )

    def drink(self, resident_id: str, container: str, millilitres: int) -> Event:
        resident = self.world.residents.get(resident_id)
        if resident is None or not resident.alive:
            raise PreconditionFailed("resident cannot drink")
        if millilitres <= 0 or self.world.water_containers.get(container, 0) < millilitres:
            raise PreconditionFailed("water is unavailable")
        absorbed = min(millilitres, 4_000 - resident.hydration_millilitres)
        return self._emit(
            "water.consumed.v1",
            {
                "resident_id": resident_id,
                "container": container,
                "millilitres": millilitres,
                "water_absorbed_millilitres": max(0, absorbed),
            },
            actor_ids=(resident_id,),
            entity_ids=(resident_id, container),
        )

    def advance_time(self, seconds: int) -> Event:
        """Advance simulated time without consulting the wall clock."""
        if seconds <= 0:
            raise PreconditionFailed("seconds must be positive")
        return self._emit(
            "world.time_advanced.v1",
            {"sim_time": self.world.sim_time + seconds},
        )

    def advance_day(self, spoil_rate_ppm: int) -> list[Event]:
        """Advance one day, applying stochastic spoilage to each container.

        Spoilage is the declared sink. Each container draws from its own named
        stream, so adding a container — or adding a cosmetic draw elsewhere —
        cannot perturb any other container's outcome.
        """
        day = self.world.sim_time // 86_400
        events: list[Event] = []
        for container in sorted(self.world.containers):  # sorted: never iterate unordered
            amount = self.world.containers[container]
            if amount <= 0:
                continue
            stream = self._rng.stream("economy", container, "spoilage")
            # Integer arithmetic throughout: the jitter is a ppm draw, not a float.
            jitter = stream.ppm(day)
            effective_rate = apply_rate(spoil_rate_ppm, 500_000 + jitter // 2)
            lost = apply_rate(amount, effective_rate)
            if lost <= 0:
                continue
            events.append(
                self._emit(
                    "grain.spoiled.v1",
                    {"container": container, "grams": lost},
                    entity_ids=(container,),
                    rng_draws=(
                        {
                            "subsystem": "economy",
                            "purpose": "spoilage",
                            "entity": container,
                            "counter": day,
                            "value": jitter,
                        },
                    ),
                )
            )
        events.append(self.advance_time(86_400))
        return events

    # -- replay ---------------------------------------------------------

    @classmethod
    def replay(cls, store: EventStore, rng: StreamRegistry) -> "Kernel":
        """Rebuild state from recorded events.

        This is *recorded-history reconstruction* in the wiki/14 §D1 sense: the
        events carry the authoritative outcomes, so nothing is recomputed and no
        RNG draw is repeated. It must succeed on any machine.
        """
        k = cls(store, rng)
        for ev in store.read_all():
            k._apply(ev)
        return k
