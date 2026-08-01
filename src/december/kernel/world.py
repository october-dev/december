"""A deliberately trivial world: grain in containers.

This is the walking skeleton. It has no ecology, no people, and no cognition.
Its only job is to exercise the parts of the architecture that cannot be
retrofitted later — integer state, the command pipeline, hash-chained events,
named RNG streams, conservation with a declared sink, and snapshot/replay.

Everything real comes after this proves out. Building weather and crops first
would be building on an unverified spine, and it is exactly where the
integer-versus-float decision bites hardest.
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
class World:
    """Authoritative state.

    `containers` holds live grain; `spoiled_total` is a declared sink. Together
    they must always sum to the total ever created, which is the conservation
    invariant the property tests assert.
    """

    containers: dict[str, int] = field(default_factory=dict)
    spoiled_total: int = 0
    created_total: int = 0
    sim_time: int = 0

    def total_live(self) -> int:
        return sum(self.containers.values())

    def check_conservation(self) -> None:
        """Assert that nothing has been created or destroyed off-ledger."""
        accounted = self.total_live() + self.spoiled_total
        if accounted != self.created_total:
            raise AssertionError(
                f"conservation violated: live {self.total_live()} + "
                f"spoiled {self.spoiled_total} = {accounted}, "
                f"but {self.created_total} was created"
            )

    def state_hash(self) -> bytes:
        """Canonical full-state hash, computed at snapshots.

        Containers are sorted by id so the digest cannot depend on dict
        insertion order — the kind of latent nondeterminism wiki/14 §D2 bans.
        """
        payload = {
            "containers": sorted(self.containers.items()),
            "spoiled_total": self.spoiled_total,
            "created_total": self.created_total,
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
        events.append(
            self._emit(
                "world.time_advanced.v1",
                {"sim_time": self.world.sim_time + 86_400},
            )
        )
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
