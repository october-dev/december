"""Conservation, integer-state, and encoding invariants.

These enforce the laws in wiki/01 and the ADR-006 numeric policy at the level
where they can actually be violated: the encoder and the transition pipeline.
"""

from __future__ import annotations

import random

import pytest

from december.domain.units import (
    PPM_ONE,
    QuantizationError,
    apply_rate,
    is_canonical_scalar,
    quantize,
)
from december.kernel.canonical import CanonicalEncodingError, encode
from december.kernel.codec import decode
from december.kernel.rng import StreamRegistry
from december.kernel.store import EventStore
from december.kernel.world import Kernel, PreconditionFailed


# -- ADR-006: no float may reach canonical state ------------------------

def test_encoder_rejects_floats():
    with pytest.raises(CanonicalEncodingError, match="quantize it first"):
        encode({"grams": 1.5})


def test_encoder_rejects_sets():
    """Sets have nondeterministic iteration order (wiki/14 §D2 rule 4)."""
    with pytest.raises(CanonicalEncodingError, match="not deterministic"):
        encode({"ids": {"a", "b"}})


def test_quantize_is_half_to_even():
    assert quantize(0.5) == 0
    assert quantize(1.5) == 2
    assert quantize(2.5) == 2
    assert quantize(-0.5) == 0
    assert quantize(-1.5) == -2


def test_quantize_rejects_nan_and_infinity():
    for bad in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(QuantizationError):
            quantize(bad)


def test_apply_rate_is_exact_integer_arithmetic():
    assert apply_rate(1_000_000, PPM_ONE) == 1_000_000
    assert apply_rate(1_000_000, 0) == 0
    assert apply_rate(1_000, 500_000) == 500
    # Half-to-even at the tie: 1 * 0.5 -> 0, 3 * 0.5 -> 2
    assert apply_rate(1, 500_000) == 0
    assert apply_rate(3, 500_000) == 2


def test_canonical_scalar_predicate_excludes_float():
    assert is_canonical_scalar(5)
    assert is_canonical_scalar("x")
    assert not is_canonical_scalar(1.0)


def test_canonical_round_trip():
    value = {
        "a": [1, -2, 0, None, True, False],
        "b": {"nested": "ünïcodé", "raw": b"\x00\xff"},
        "big": 2**200,
    }
    assert decode(encode(value)) == value


def test_encoding_is_order_independent():
    """Two dicts with the same contents encode identically."""
    a = {"x": 1, "y": 2, "z": 3}
    b = {"z": 3, "y": 2, "x": 1}
    assert encode(a) == encode(b)


# -- Conservation --------------------------------------------------------

def test_conservation_under_random_command_sequences(tmp_path):
    """Property test: arbitrary valid command sequences conserve mass.

    Uses a fixed RNG for the *test driver* so a failure reproduces exactly.
    """
    rnd = random.Random(20260801)
    with EventStore(tmp_path / "log.dec") as store:
        k = Kernel(store, StreamRegistry(b"prop-seed"))
        containers = ["granary", "household_a", "household_b", "field_store"]
        k.create_grain("granary", 1_000_000)

        for _ in range(400):
            action = rnd.choice(["transfer", "transfer", "day", "create"])
            if action == "create":
                k.create_grain(rnd.choice(containers), rnd.randint(1, 5_000))
            elif action == "day":
                k.advance_day(spoil_rate_ppm=rnd.randint(0, 20_000))
            else:
                src, dst = rnd.sample(containers, 2)
                available = k.world.containers.get(src, 0)
                if available > 1:
                    k.transfer(src, dst, rnd.randint(1, available))
            k.world.check_conservation()  # raises on violation

        assert k.world.total_live() + k.world.spoiled_total == k.world.created_total


def test_no_negative_stocks(tmp_path):
    with EventStore(tmp_path / "log.dec") as store:
        k = Kernel(store, StreamRegistry(b"seed"))
        k.create_grain("granary", 100)
        with pytest.raises(PreconditionFailed):
            k.transfer("granary", "household", 101)
        assert k.world.containers["granary"] == 100
        assert all(v >= 0 for v in k.world.containers.values())


def test_rejected_command_emits_no_event(tmp_path):
    """A rejection must not mutate state or append to canonical history."""
    path = tmp_path / "log.dec"
    with EventStore(path) as store:
        k = Kernel(store, StreamRegistry(b"seed"))
        k.create_grain("granary", 100)
        before = store.next_sequence
        for bad in (0, -5, 101):
            with pytest.raises(PreconditionFailed):
                k.transfer("granary", "household", bad)
        assert store.next_sequence == before


def test_transfer_to_self_is_rejected(tmp_path):
    with EventStore(tmp_path / "log.dec") as store:
        k = Kernel(store, StreamRegistry(b"seed"))
        k.create_grain("granary", 100)
        with pytest.raises(PreconditionFailed):
            k.transfer("granary", "granary", 10)


# -- RNG stream properties ----------------------------------------------

def test_streams_are_independent():
    """Different (subsystem, entity, purpose) triples give different draws."""
    reg = StreamRegistry(b"seed")
    a = reg.stream("economy", "granary", "spoilage")
    b = reg.stream("economy", "household", "spoilage")
    c = reg.stream("health", "granary", "spoilage")
    draws = [tuple(s.ppm(i) for i in range(20)) for s in (a, b, c)]
    assert len(set(draws)) == 3


def test_stream_draws_are_reproducible():
    s1 = StreamRegistry(b"seed").stream("economy", "granary", "spoilage")
    s2 = StreamRegistry(b"seed").stream("economy", "granary", "spoilage")
    assert [s1.ppm(i) for i in range(50)] == [s2.ppm(i) for i in range(50)]


def test_below_is_uniform_enough_and_unbiased():
    """A crude uniformity check that would catch modulo bias."""
    s = StreamRegistry(b"seed").stream("test", "x", "uniform")
    counts = [0] * 7
    for i in range(70_000):
        counts[s.below(i, 7)] += 1
    assert all(9_200 < c < 10_800 for c in counts), counts


def test_occurs_matches_its_rate():
    s = StreamRegistry(b"seed").stream("test", "x", "bernoulli")
    hits = sum(s.occurs(i, 250_000) for i in range(40_000))
    assert 9_400 < hits < 10_600  # ~25% of 40k
