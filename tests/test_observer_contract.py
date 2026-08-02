"""The browser projection must remain deterministic and read-only."""

from __future__ import annotations

import copy
import json

from december.kernel.rng import StreamRegistry
from december.kernel.store import EventStore
from december.kernel.world import Kernel
from december.observer.contract import CONTRACT_VERSION, write_replay_bundle


def _export(directory, log_path):
    with EventStore(log_path) as store:
        kernel = Kernel(store, StreamRegistry(b"observer-test"), "test")
        kernel.create_grain("granary", 100_000)
        kernel.create_resident("mara", "Mara", "Grower", 10_000, 12_000, "Inspecting grain")
        snapshot_world = copy.deepcopy(kernel.world)
        through_sequence = store.next_sequence - 1
        head_hash = store.head_hash
        kernel.advance_time(60)
        kernel.move_resident("mara", 11_000, 12_000)
        kernel.transfer("granary", "household", 5_000)
        events = [event for event in store.read_all() if event.sequence > through_sequence]
        return write_replay_bundle(
            directory,
            snapshot_world=snapshot_world,
            snapshot_through_sequence=through_sequence,
            snapshot_head_hash=head_hash,
            events=events,
            final_world=kernel.world,
            scenario_id="observer-test",
        )


def test_bundle_is_versioned_contiguous_and_hash_linked(tmp_path):
    output = tmp_path / "bundle"
    manifest = _export(output, tmp_path / "history.dec")
    snapshot = json.loads((output / "snapshot.json").read_text())
    events = [json.loads(line) for line in (output / "events.jsonl").read_text().splitlines()]

    assert manifest["contract_version"] == CONTRACT_VERSION
    assert snapshot["contract_version"] == CONTRACT_VERSION
    assert len(events) == manifest["event_count"] == 3
    assert events[0]["sequence"] == snapshot["through_sequence"] + 1
    assert events[0]["previous_event_hash"] == snapshot["head_event_hash"]
    assert [event["sequence"] for event in events] == list(
        range(events[0]["sequence"], events[-1]["sequence"] + 1)
    )
    assert events[-1]["event_hash"] == manifest["final_event_hash"]


def test_same_history_exports_byte_identical_bundle(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    _export(first, tmp_path / "first.dec")
    _export(second, tmp_path / "second.dec")

    for filename in ("manifest.json", "snapshot.json", "events.jsonl"):
        assert (first / filename).read_bytes() == (second / filename).read_bytes()


def test_resident_events_replay_exactly(tmp_path):
    path = tmp_path / "history.dec"
    with EventStore(path) as store:
        kernel = Kernel(store, StreamRegistry(b"resident-test"))
        kernel.create_resident("iven", "Iven", "Fisher", 1_000, 2_000, "Repairing nets")
        kernel.advance_time(300)
        kernel.move_resident("iven", 3_000, 4_000)
        kernel.set_activity("iven", "Inspecting the ford")
        live_hash = kernel.world.state_hash()

    with EventStore(path, writable=False) as store:
        replayed = Kernel.replay(store, StreamRegistry(b"irrelevant-during-replay"))

    assert replayed.world.state_hash() == live_hash
    assert replayed.world.residents["iven"].activity == "Inspecting the ford"
