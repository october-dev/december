"""Generate December's first kernel-driven observer replay.

This is scripted input to the real kernel, not agent cognition. It proves the
full truth path: typed command -> canonical event -> replay bundle -> viewer.
"""

from __future__ import annotations

import argparse
import copy
import tempfile
from pathlib import Path

from december.kernel.rng import StreamRegistry
from december.kernel.store import EventStore
from december.kernel.world import Kernel
from december.observer.contract import write_replay_bundle

SCENARIO_ID = "founding-valley-day-one"


def tile(value: int) -> int:
    return value * 1_000


def build(output: Path) -> dict:
    with tempfile.TemporaryDirectory(prefix="december-day-one-") as temporary:
        log_path = Path(temporary) / "canonical.dec"
        with EventStore(log_path) as store:
            kernel = Kernel(store, StreamRegistry(b"december-founding-valley-v1"), "0.0.2")
            kernel.create_grain("granary", 286_000)
            kernel.create_grain("raised_seed_store", 74_000)
            kernel.create_water("cistern", 120_000)
            kernel.create_resident(
                "iven", "Iven", "Fisher · House Reed", tile(17), tile(9),
                "Checking the fishing nets", energy_kilojoules=6_400,
                hydration_millilitres=2_100,
            )
            kernel.create_resident(
                "mara", "Mara", "Grower · House Alder", tile(23), tile(14),
                "Inspecting the lower barley plot", energy_kilojoules=6_800,
                hydration_millilitres=2_400,
            )
            kernel.create_resident(
                "sera", "Sera", "Storekeeper · House Flint", tile(29), tile(8),
                "Checking the seed-grain ledger", energy_kilojoules=7_200,
                hydration_millilitres=2_600,
            )
            kernel.create_resident(
                "toma", "Toma", "Carpenter · House Birch", tile(9), tile(20),
                "Selecting timber for the footbridge", energy_kilojoules=5_900,
                hydration_millilitres=1_900,
            )
            kernel.advance_time(16 * 86_400 + 5 * 3_600 + 40 * 60)

            snapshot_world = copy.deepcopy(kernel.world)
            snapshot_through_sequence = store.next_sequence - 1
            snapshot_head_hash = store.head_hash

            kernel.advance_time(2 * 60)
            kernel.set_activity("iven", "Walking to inspect the eastern ford")
            kernel.move_resident("iven", tile(19), tile(13))
            kernel.metabolize("iven", 11 * 60, 1_200_000)
            kernel.advance_time(9 * 60)
            kernel.move_resident("mara", tile(28), tile(14))
            kernel.set_activity("mara", "Checking barley heads for blight")
            kernel.metabolize("mara", 9 * 60, 1_100_000)
            kernel.advance_time(7 * 60)
            kernel.set_activity("sera", "Moving seed grain into dry storage")
            kernel.transfer("granary", "raised_seed_store", 12_400)
            kernel.move_resident("sera", tile(34), tile(9))
            kernel.metabolize("sera", 18 * 60, 1_000_000)
            kernel.advance_time(15 * 60)
            kernel.move_resident("toma", tile(13), tile(24))
            kernel.set_activity("toma", "Hauling timber to the bridge site")
            kernel.metabolize("toma", 33 * 60, 1_500_000)
            kernel.advance_time(12 * 60)
            kernel.move_resident("iven", tile(18), tile(18))
            kernel.set_activity("iven", "Measuring the ford against yesterday’s notch")
            kernel.drink("iven", "cistern", 450)
            kernel.advance_time(11 * 60)
            kernel.move_resident("mara", tile(27), tile(21))
            kernel.move_resident("sera", tile(37), tile(13))
            kernel.eat("mara", "granary", 180)
            kernel.eat("sera", "granary", 160)
            kernel.drink("sera", "cistern", 350)
            kernel.advance_time(14 * 60)
            kernel.move_resident("toma", tile(17), tile(25))
            kernel.eat("toma", "granary", 240)
            kernel.drink("toma", "cistern", 600)

            all_events = list(store.read_all())
            replay_events = [event for event in all_events if event.sequence > snapshot_through_sequence]
            return write_replay_bundle(
                output,
                snapshot_world=snapshot_world,
                snapshot_through_sequence=snapshot_through_sequence,
                snapshot_head_hash=snapshot_head_hash,
                events=replay_events,
                final_world=kernel.world,
                scenario_id=SCENARIO_ID,
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/founding-valley-day-one"))
    args = parser.parse_args()
    manifest = build(args.output)
    print(
        f"wrote {manifest['event_count']} events through sequence "
        f"{manifest['last_event_sequence']} to {args.output}"
    )


if __name__ == "__main__":
    main()
