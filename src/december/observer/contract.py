"""Versioned, read-only contract between the kernel and visual observers.

The kernel's binary event log remains canonical. This module exports a JSON
projection that browsers can read without gaining authority to mutate the
world. It intentionally contains no wall-clock generation timestamp: exporting
the same history twice must produce byte-identical artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from december.kernel.events import DIGEST_ALGORITHM, DIGEST_VERSION, Event
from december.kernel.world import World

CONTRACT_VERSION = "december.observer.v1"


def _world_state(world: World) -> dict[str, Any]:
    return {
        "sim_time": world.sim_time,
        "containers": [
            {"container_id": container_id, "grain_grams": grams}
            for container_id, grams in sorted(world.containers.items())
        ],
        "residents": [
            {
                "resident_id": resident.resident_id,
                "name": resident.name,
                "role": resident.role,
                "x_millimetres": resident.x_millimetres,
                "y_millimetres": resident.y_millimetres,
                "activity": resident.activity,
            }
            for _, resident in sorted(world.residents.items())
        ],
        "ledger": {
            "created_grain_grams": world.created_total,
            "spoiled_grain_grams": world.spoiled_total,
            "live_grain_grams": world.total_live(),
        },
    }


def _event_document(event: Event) -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "sequence": event.sequence,
        "event_id": event.event_id,
        "event_type": event.event_type,
        "sim_time": event.sim_time,
        "payload": dict(event.payload),
        "actor_ids": list(event.actor_ids),
        "entity_ids": list(event.entity_ids),
        "causal_parent_ids": list(event.causal_parent_ids),
        "rng_draws": [dict(draw) for draw in event.rng_draws],
        "world_id": event.world_id,
        "branch_id": event.branch_id,
        "code_version": event.code_version,
        "previous_event_hash": event.prev_hash.hex(),
        "event_hash": event.event_hash.hex(),
    }


def _json_bytes(document: Any, *, pretty: bool = False) -> bytes:
    indent = 2 if pretty else None
    separators = None if pretty else (",", ":")
    return (
        json.dumps(document, ensure_ascii=False, sort_keys=True, indent=indent, separators=separators)
        + "\n"
    ).encode("utf-8")


def write_replay_bundle(
    directory: str | Path,
    *,
    snapshot_world: World,
    snapshot_through_sequence: int,
    snapshot_head_hash: bytes,
    events: Iterable[Event],
    final_world: World,
    scenario_id: str,
) -> dict[str, Any]:
    """Write a deterministic snapshot, ordered JSONL events, and manifest."""
    output = Path(directory)
    output.mkdir(parents=True, exist_ok=True)
    ordered_events = list(events)
    if ordered_events:
        expected = snapshot_through_sequence + 1
        if ordered_events[0].sequence != expected:
            raise ValueError(f"event stream starts at {ordered_events[0].sequence}, expected {expected}")
        if ordered_events[0].prev_hash != snapshot_head_hash:
            raise ValueError("event stream does not continue the snapshot hash chain")
        for previous, current in zip(ordered_events, ordered_events[1:]):
            if current.sequence != previous.sequence + 1 or current.prev_hash != previous.event_hash:
                raise ValueError("event stream is not contiguous")

    snapshot = {
        "contract_version": CONTRACT_VERSION,
        "snapshot_kind": "replay_start",
        "scenario_id": scenario_id,
        "world_id": "world:december",
        "branch_id": "canonical",
        "through_sequence": snapshot_through_sequence,
        "head_event_hash": snapshot_head_hash.hex(),
        "state_hash": snapshot_world.state_hash().hex(),
        "coordinate_system": {"unit": "millimetre", "millimetres_per_tile": 1_000},
        "state": _world_state(snapshot_world),
    }
    event_documents = [_event_document(event) for event in ordered_events]
    final_event_hash = (
        ordered_events[-1].event_hash.hex() if ordered_events else snapshot_head_hash.hex()
    )
    manifest = {
        "contract_version": CONTRACT_VERSION,
        "scenario_id": scenario_id,
        "world_id": "world:december",
        "branch_id": "canonical",
        "snapshot": "snapshot.json",
        "events": "events.jsonl",
        "snapshot_through_sequence": snapshot_through_sequence,
        "event_count": len(event_documents),
        "first_event_sequence": ordered_events[0].sequence if ordered_events else None,
        "last_event_sequence": ordered_events[-1].sequence if ordered_events else snapshot_through_sequence,
        "final_event_hash": final_event_hash,
        "final_state_hash": final_world.state_hash().hex(),
        "digest": {"algorithm": DIGEST_ALGORITHM, "version": DIGEST_VERSION},
    }

    output.joinpath("snapshot.json").write_bytes(_json_bytes(snapshot, pretty=True))
    output.joinpath("events.jsonl").write_bytes(
        b"".join(_json_bytes(event) for event in event_documents)
    )
    output.joinpath("manifest.json").write_bytes(_json_bytes(manifest, pretty=True))
    return manifest
