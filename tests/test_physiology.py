"""Phase 1 body-loop invariants: reserves, consumption, and death."""

from __future__ import annotations

import pytest

from december.kernel.rng import StreamRegistry
from december.kernel.store import EventStore
from december.kernel.world import Kernel, PreconditionFailed


def test_eating_and_drinking_conserve_materials(tmp_path):
    with EventStore(tmp_path / "body.dec") as store:
        kernel = Kernel(store, StreamRegistry(b"body"))
        kernel.create_grain("granary", 10_000)
        kernel.create_water("cistern", 20_000)
        kernel.create_resident(
            "mara", "Mara", "Grower", 0, 0, "Resting",
            energy_kilojoules=5_000, hydration_millilitres=2_000,
        )
        kernel.eat("mara", "granary", 200)
        kernel.drink("mara", "cistern", 500)

        resident = kernel.world.residents["mara"]
        assert resident.energy_kilojoules == 8_000
        assert resident.hydration_millilitres == 2_500
        assert kernel.world.total_live() + kernel.world.consumed_total == 10_000
        assert sum(kernel.world.water_containers.values()) + kernel.world.water_consumed_total == 20_000


def test_metabolism_is_integer_and_replayable(tmp_path):
    path = tmp_path / "body.dec"
    with EventStore(path) as store:
        kernel = Kernel(store, StreamRegistry(b"body"))
        kernel.create_resident("iven", "Iven", "Fisher", 0, 0, "Walking")
        kernel.metabolize("iven", 3_600, 1_500_000)
        assert kernel.world.residents["iven"].energy_kilojoules == 7_850
        assert kernel.world.residents["iven"].hydration_millilitres == 2_850
        live_hash = kernel.world.state_hash()

    with EventStore(path, writable=False) as store:
        replayed = Kernel.replay(store, StreamRegistry(b"unused"))
    assert replayed.world.state_hash() == live_hash


def test_deprivation_can_kill_and_dead_resident_cannot_act(tmp_path):
    with EventStore(tmp_path / "body.dec") as store:
        kernel = Kernel(store, StreamRegistry(b"body"))
        kernel.create_resident(
            "toma", "Toma", "Carpenter", 0, 0, "Stranded",
            energy_kilojoules=0, hydration_millilitres=0, health_ppm=100_000,
        )
        events = kernel.metabolize("toma", 86_400)
        assert [event.event_type for event in events] == [
            "resident.metabolized.v1", "resident.died.v1"
        ]
        assert not kernel.world.residents["toma"].alive
        with pytest.raises(PreconditionFailed, match="dead"):
            kernel.set_activity("toma", "Working")
        with pytest.raises(PreconditionFailed, match="dead"):
            kernel.move_resident("toma", 1_000, 1_000)
