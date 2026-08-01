"""Counter-based named RNG streams.

Implements the scheme in wiki/14 §D3. A stream is a pure function of its key
and a counter, so it holds no sequential state, can be evaluated from any point,
and needs nothing in snapshots.

Deliberately built on BLAKE2b rather than NumPy. Because the whole construction
is integer and byte operations, it is bit-identical on every platform by
construction — no SIMD dispatch, no BLAS, no distribution-layer version drift.
That portability is a direct dividend of the ADR-006 Option A decision.

Never seed a stream from Python's `hash()`: it is salted per process and would
make streams irreproducible across runs.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

_DIGEST_BYTES = 32


def stream_key(
    root_seed: bytes,
    branch_id: str,
    subsystem: str,
    entity_id: str,
    purpose: str,
) -> bytes:
    """Derive a stable 16-byte stream key.

    Components are length-prefixed so that ("ab", "c") and ("a", "bc") cannot
    collide into the same key.
    """
    h = hashlib.blake2b(digest_size=16)
    h.update(len(root_seed).to_bytes(4, "big"))
    h.update(root_seed)
    for part in (branch_id, subsystem, entity_id, purpose):
        raw = part.encode("utf-8")
        h.update(len(raw).to_bytes(4, "big"))
        h.update(raw)
    return h.digest()


@dataclass(frozen=True, slots=True)
class Stream:
    """A named, reproducible source of randomness.

    `key` identifies the stream; `counter` is the position within it. Draws are
    explicit about their counter so a recorded event can be re-derived and
    audited without replaying the subsystem that produced it.
    """

    key: bytes
    subsystem: str
    purpose: str

    def _block(self, counter: int) -> bytes:
        h = hashlib.blake2b(digest_size=_DIGEST_BYTES, key=self.key)
        h.update(counter.to_bytes(16, "big"))
        return h.digest()

    def bits(self, counter: int, n: int) -> int:
        """Return `n` uniformly distributed bits as an int."""
        if n <= 0:
            raise ValueError("n must be positive")
        out = 0
        produced = 0
        block_index = 0
        while produced < n:
            block = self._block((counter << 32) | block_index)
            out = (out << (_DIGEST_BYTES * 8)) | int.from_bytes(block, "big")
            produced += _DIGEST_BYTES * 8
            block_index += 1
        return out >> (produced - n)

    def below(self, counter: int, bound: int) -> int:
        """Uniform integer in [0, bound), free of modulo bias.

        Uses rejection sampling with a per-attempt counter perturbation, so the
        result depends only on (key, counter, bound) and never on floats.
        """
        if bound <= 0:
            raise ValueError("bound must be positive")
        if bound == 1:
            return 0
        n = (bound - 1).bit_length()
        limit = 1 << n
        threshold = limit - (limit % bound)
        for attempt in range(128):
            candidate = self.bits((counter << 16) | attempt, n)
            if candidate < threshold:
                return candidate % bound
        # Astronomically unlikely; deterministic fallback keeps replay total.
        return self.bits((counter << 16) | 0xFFFF, n + 64) % bound

    def ppm(self, counter: int) -> int:
        """Uniform draw in [0, 1_000_000), for comparison against a rate.

        Returning parts-per-million rather than a float keeps probability
        comparisons in integer arithmetic all the way down.
        """
        return self.below(counter, 1_000_000)

    def occurs(self, counter: int, rate_ppm: int) -> bool:
        """True with probability `rate_ppm` / 1e6."""
        if rate_ppm <= 0:
            return False
        if rate_ppm >= 1_000_000:
            return True
        return self.ppm(counter) < rate_ppm


class StreamRegistry:
    """Derives streams for a world/branch.

    One stream per (subsystem, entity, purpose) means adding a cosmetic draw in
    one subsystem cannot perturb another — the property wiki/06 requires.
    """

    __slots__ = ("_root_seed", "_branch_id")

    def __init__(self, root_seed: bytes, branch_id: str = "canonical") -> None:
        if not root_seed:
            raise ValueError("root_seed must be non-empty")
        self._root_seed = root_seed
        self._branch_id = branch_id

    def stream(self, subsystem: str, entity_id: str, purpose: str) -> Stream:
        return Stream(
            key=stream_key(self._root_seed, self._branch_id, subsystem, entity_id, purpose),
            subsystem=subsystem,
            purpose=purpose,
        )
