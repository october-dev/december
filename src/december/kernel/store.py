"""Append-only event store, single writer.

Backed by a file rather than PostgreSQL for now. Audit pass 2 (P2-F07) is right
that the Postgres integrity machinery solves a scale December does not yet have:
with one writer and one local machine, an append-only file plus the hash chain
gives reconstruction, corruption detection, and divergence localization.

What Postgres buys later is concurrent readers, projections, and operational
tooling. The interface here is narrow enough that swapping it in is a
contained change — and when that happens, the `xid8` snapshot fencing in
wiki/14 §D7 becomes mandatory rather than optional, because a second writer
reintroduces the commit-ordering hazard that single-writer append avoids.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

from .canonical import encode
from .events import GENESIS_HASH, Event, verify_chain

_RECORD_HEADER = 4  # bytes of big-endian record length


class SingleWriterViolation(RuntimeError):
    """A second writer attempted to open the log."""


class EventStore:
    """Append-only log with an enforced single writer.

    The writer lock is an exclusive lock file. It is not merely advisory
    bookkeeping: sequence order equals commit order only because exactly one
    process appends, and that property is what the projections rely on.
    """

    def __init__(self, path: str | os.PathLike[str], *, writable: bool = True) -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock_path = self._path.with_suffix(self._path.suffix + ".lock")
        self._writable = writable
        self._lock_fd: int | None = None
        if writable:
            self._acquire_writer_lock()
        self._sequence, self._head_hash = self._scan_tail()

    def _acquire_writer_lock(self) -> None:
        try:
            self._lock_fd = os.open(self._lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise SingleWriterViolation(
                f"another writer holds {self._lock_path}. December's ordering "
                "guarantee depends on exactly one appender."
            ) from exc
        os.write(self._lock_fd, str(os.getpid()).encode())

    def _scan_tail(self) -> tuple[int, bytes]:
        """Return (next_sequence, head_hash) by reading the existing log."""
        seq = 0
        head = GENESIS_HASH
        for ev in self.read_all():
            seq = ev.sequence + 1
            head = ev.event_hash
        return seq, head

    def append(self, event: Event) -> Event:
        """Seal and durably append one event, returning the sealed copy."""
        if not self._writable:
            raise SingleWriterViolation("store opened read-only")
        from dataclasses import replace

        staged = replace(event, sequence=self._sequence, prev_hash=self._head_hash).sealed()
        record = encode(
            {
                **staged.body(),
                "event_hash": staged.event_hash,
            }
        )
        with open(self._path, "ab") as fh:
            fh.write(len(record).to_bytes(_RECORD_HEADER, "big"))
            fh.write(record)
            fh.flush()
            os.fsync(fh.fileno())
        self._sequence = staged.sequence + 1
        self._head_hash = staged.event_hash
        return staged

    def read_all(self) -> Iterator[Event]:
        """Yield every event in sequence order."""
        if not self._path.exists():
            return
        from .codec import decode_event

        with open(self._path, "rb") as fh:
            while True:
                header = fh.read(_RECORD_HEADER)
                if not header:
                    return
                if len(header) < _RECORD_HEADER:
                    raise ValueError("truncated record header; log is corrupt")
                length = int.from_bytes(header, "big")
                body = fh.read(length)
                if len(body) < length:
                    raise ValueError("truncated record body; log is corrupt")
                yield decode_event(body)

    def verify(self) -> int:
        """Verify the whole chain. Returns the number of events checked."""
        events = list(self.read_all())
        verify_chain(events)
        return len(events)

    @property
    def head_hash(self) -> bytes:
        return self._head_hash

    @property
    def next_sequence(self) -> int:
        return self._sequence

    def close(self) -> None:
        if self._lock_fd is not None:
            os.close(self._lock_fd)
            self._lock_path.unlink(missing_ok=True)
            self._lock_fd = None

    def __enter__(self) -> "EventStore":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
