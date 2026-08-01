"""Event envelope and hash chaining.

Implements the Phase 1 integrity minimum from wiki/14: hash-chained envelopes,
per-aggregate versions, and a canonical full-state hash at snapshots. The
heavier machinery the first audit proposed — per-event lattice hashing, `xid8`
snapshot fencing — is deliberately deferred until measurement shows it is
needed, per audit pass 2 finding P2-F07.

The chain is what makes the log tamper-evident: each event commits to its
predecessor, so altering any historical event invalidates every hash after it.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Mapping

from .canonical import encode

DIGEST_ALGORITHM = "blake2b-256"
DIGEST_VERSION = 1

GENESIS_HASH = b"\x00" * 32


@dataclass(frozen=True, slots=True)
class Event:
    """One immutable canonical mutation.

    `sequence` is assigned by the store, which is single-writer, so sequence
    order equals commit order by construction. That is the primary defence
    against the sequence-gap hazard in wiki/14 §D7 — a `bigserial` high-water
    mark alone would be unsafe once a second writer existed.
    """

    event_type: str
    sim_time: int  # seconds since world epoch
    sequence: int
    payload: Mapping[str, Any]
    actor_ids: tuple[str, ...] = ()
    entity_ids: tuple[str, ...] = ()
    causal_parent_ids: tuple[str, ...] = ()
    rng_draws: tuple[Mapping[str, Any], ...] = ()
    world_id: str = "world:december"
    branch_id: str = "canonical"
    code_version: str = "dev"
    prev_hash: bytes = GENESIS_HASH
    event_hash: bytes = field(default=b"")

    def body(self) -> dict[str, Any]:
        """The hashed content of the event, excluding its own hash."""
        return {
            "event_type": self.event_type,
            "sim_time": self.sim_time,
            "sequence": self.sequence,
            "payload": dict(self.payload),
            "actor_ids": list(self.actor_ids),
            "entity_ids": list(self.entity_ids),
            "causal_parent_ids": list(self.causal_parent_ids),
            "rng_draws": [dict(d) for d in self.rng_draws],
            "world_id": self.world_id,
            "branch_id": self.branch_id,
            "code_version": self.code_version,
            "prev_hash": self.prev_hash,
            "digest_algorithm": DIGEST_ALGORITHM,
            "digest_version": DIGEST_VERSION,
        }

    def compute_hash(self) -> bytes:
        return hashlib.blake2b(encode(self.body()), digest_size=32).digest()

    def sealed(self) -> "Event":
        """Return a copy with `event_hash` filled in."""
        from dataclasses import replace

        return replace(self, event_hash=self.compute_hash())

    @property
    def event_id(self) -> str:
        return f"evt_{self.event_hash.hex()[:16]}"


class ChainIntegrityError(RuntimeError):
    """The event chain does not verify."""


def verify_chain(events: list[Event]) -> None:
    """Verify hash linkage and sequence continuity over a full log.

    Raises on the first inconsistency, naming the offending sequence number so
    a failure localizes immediately rather than requiring a manual diff.
    """
    expected_prev = GENESIS_HASH
    expected_seq = 0
    for ev in events:
        if ev.sequence != expected_seq:
            raise ChainIntegrityError(
                f"sequence gap: expected {expected_seq}, found {ev.sequence}"
            )
        if ev.prev_hash != expected_prev:
            raise ChainIntegrityError(
                f"broken chain at sequence {ev.sequence}: "
                f"prev_hash {ev.prev_hash.hex()[:16]} != {expected_prev.hex()[:16]}"
            )
        recomputed = ev.compute_hash()
        if ev.event_hash != recomputed:
            raise ChainIntegrityError(
                f"event {ev.sequence} hash mismatch: content was altered"
            )
        expected_prev = ev.event_hash
        expected_seq += 1
