"""Decoder for the canonical encoding.

Kept separate from `canonical.encode` because encoding is a correctness-critical
kernel operation while decoding is I/O recovery. A round-trip property test
(tests/test_canonical.py) pins them together.
"""

from __future__ import annotations

from typing import Any

from .canonical import (
    _T_BYTES,
    _T_FALSE,
    _T_INT,
    _T_LIST,
    _T_MAP,
    _T_NULL,
    _T_STR,
    _T_TRUE,
)
from .events import Event


class _Reader:
    __slots__ = ("_buf", "_pos")

    def __init__(self, buf: bytes) -> None:
        self._buf = buf
        self._pos = 0

    def take(self, n: int) -> bytes:
        if self._pos + n > len(self._buf):
            raise ValueError("truncated canonical record")
        out = self._buf[self._pos : self._pos + n]
        self._pos += n
        return out

    def uint(self) -> int:
        width = self.take(1)[0]
        if width == 0:
            return 0
        return int.from_bytes(self.take(width), "big")

    def value(self) -> Any:
        tag = self.take(1)
        if tag == _T_NULL:
            return None
        if tag == _T_TRUE:
            return True
        if tag == _T_FALSE:
            return False
        if tag == _T_INT:
            negative = self.take(1) == b"\x01"
            magnitude = self.uint()
            return -magnitude if negative else magnitude
        if tag == _T_STR:
            return self.take(self.uint()).decode("utf-8")
        if tag == _T_BYTES:
            return self.take(self.uint())
        if tag == _T_LIST:
            return [self.value() for _ in range(self.uint())]
        if tag == _T_MAP:
            return {self.value(): self.value() for _ in range(self.uint())}
        raise ValueError(f"unknown canonical type tag {tag!r}")


def decode(buf: bytes) -> Any:
    return _Reader(buf).value()


def decode_event(buf: bytes) -> Event:
    d = decode(buf)
    return Event(
        event_type=d["event_type"],
        sim_time=d["sim_time"],
        sequence=d["sequence"],
        payload=d["payload"],
        actor_ids=tuple(d["actor_ids"]),
        entity_ids=tuple(d["entity_ids"]),
        causal_parent_ids=tuple(d["causal_parent_ids"]),
        rng_draws=tuple(d["rng_draws"]),
        world_id=d["world_id"],
        branch_id=d["branch_id"],
        code_version=d["code_version"],
        prev_hash=d["prev_hash"],
        event_hash=d["event_hash"],
    )
