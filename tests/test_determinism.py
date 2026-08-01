"""The determinism suite from wiki/14 §D9.

A failure in any of these is a Blocker for Gate 1. Determinism is not a property
that can be added later; it is either maintained continuously or lost.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from december.kernel.events import ChainIntegrityError, verify_chain
from december.kernel.rng import StreamRegistry
from december.kernel.store import EventStore, SingleWriterViolation
from december.kernel.world import Kernel

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_scenario(path, seed: bytes = b"seed-1") -> tuple[bytes, int]:
    """A fixed scenario. Returns (final state hash, event count)."""
    with EventStore(path) as store:
        k = Kernel(store, StreamRegistry(seed))
        k.create_grain("granary", 500_000)
        k.create_grain("household", 25_000)
        k.transfer("granary", "household", 40_000)
        for _ in range(10):
            k.advance_day(spoil_rate_ppm=3_000)
        k.transfer("household", "granary", 1_000)
        return k.world.state_hash(), store.verify()


def test_same_seed_same_history(tmp_path):
    """Identical inputs produce an identical world."""
    h1, n1 = run_scenario(tmp_path / "a.dec")
    h2, n2 = run_scenario(tmp_path / "b.dec")
    assert h1 == h2
    assert n1 == n2


def test_different_seed_different_history(tmp_path):
    """The seed actually drives the stochastic outcome.

    Without this, `test_same_seed_same_history` could pass trivially on a world
    that has no randomness at all.
    """
    h1, _ = run_scenario(tmp_path / "a.dec", seed=b"seed-1")
    h2, _ = run_scenario(tmp_path / "b.dec", seed=b"seed-2")
    assert h1 != h2


def test_replay_from_empty_reproduces_state(tmp_path):
    """Recorded-history reconstruction (wiki/14 §D1 guarantee 1)."""
    path = tmp_path / "log.dec"
    live_hash, _ = run_scenario(path)
    with EventStore(path, writable=False) as store:
        replayed = Kernel.replay(store, StreamRegistry(b"seed-1"))
    assert replayed.world.state_hash() == live_hash


def test_replay_needs_no_rng(tmp_path):
    """Replay must not recompute draws.

    Reconstruction is fed a deliberately wrong seed. If it still reproduces the
    state, no RNG was consulted — which is the property that makes replay
    portable across machines even when re-execution would not be.
    """
    path = tmp_path / "log.dec"
    live_hash, _ = run_scenario(path, seed=b"seed-1")
    with EventStore(path, writable=False) as store:
        replayed = Kernel.replay(store, StreamRegistry(b"COMPLETELY-DIFFERENT"))
    assert replayed.world.state_hash() == live_hash


def test_hash_seed_sensitivity(tmp_path):
    """Identical history under different PYTHONHASHSEED values.

    Catches any latent dependence on set/dict iteration order or str hashing.
    Runs in subprocesses because PYTHONHASHSEED is fixed at interpreter start.
    """
    script = (
        "import sys; sys.path.insert(0, %r);\n"
        "from december.kernel.store import EventStore\n"
        "from december.kernel.rng import StreamRegistry\n"
        "from december.kernel.world import Kernel\n"
        "import tempfile, os\n"
        "d = tempfile.mkdtemp()\n"
        "s = EventStore(os.path.join(d, 'l.dec'))\n"
        "k = Kernel(s, StreamRegistry(b'seed-1'))\n"
        "k.create_grain('granary', 500000)\n"
        "k.create_grain('household', 25000)\n"
        "k.transfer('granary', 'household', 40000)\n"
        "[k.advance_day(spoil_rate_ppm=3000) for _ in range(10)]\n"
        "print(k.world.state_hash().hex())\n"
    ) % str(REPO_ROOT / "src")

    hashes = set()
    for seed in ("0", "1", "42"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        out = subprocess.run(
            [sys.executable, "-c", script], capture_output=True, text=True, env=env, check=True
        )
        hashes.add(out.stdout.strip())
    assert len(hashes) == 1, f"history varies with PYTHONHASHSEED: {hashes}"


def test_tampering_breaks_the_chain(tmp_path):
    """An altered historical event invalidates the chain."""
    path = tmp_path / "log.dec"
    run_scenario(path)
    with EventStore(path, writable=False) as store:
        events = list(store.read_all())
    from dataclasses import replace

    events[2] = replace(events[2], payload={**events[2].payload, "grams": 999_999})
    with pytest.raises(ChainIntegrityError, match="hash mismatch"):
        verify_chain(events)


def test_sequence_gap_is_detected(tmp_path):
    """A missing event is caught rather than silently skipped.

    This is the failure mode that makes a naive high-water-mark consumer unsafe
    (wiki/14 §D7). Single-writer append prevents it arising; this asserts we
    would notice if it ever did.
    """
    path = tmp_path / "log.dec"
    run_scenario(path)
    with EventStore(path, writable=False) as store:
        events = list(store.read_all())
    del events[3]
    with pytest.raises(ChainIntegrityError, match="sequence gap"):
        verify_chain(events)


def test_single_writer_is_enforced(tmp_path):
    """Two concurrent writers are refused."""
    path = tmp_path / "log.dec"
    with EventStore(path):
        with pytest.raises(SingleWriterViolation):
            EventStore(path)


def test_cosmetic_draws_do_not_perturb_physical_outcomes(tmp_path):
    """Adding draws in one stream cannot change another subsystem's results.

    The property wiki/06 requires of named streams. Here a 'cosmetic' stream is
    consumed heavily between physical steps; the physical outcome must be
    untouched.
    """
    def scenario(path, burn_cosmetic: bool):
        with EventStore(path) as store:
            rng = StreamRegistry(b"seed-1")
            k = Kernel(store, rng)
            k.create_grain("granary", 500_000)
            for i in range(10):
                if burn_cosmetic:
                    cosmetic = rng.stream("ui", "camera", "jitter")
                    for j in range(50):
                        cosmetic.ppm(i * 100 + j)
                k.advance_day(spoil_rate_ppm=3_000)
            return k.world.state_hash()

    assert scenario(tmp_path / "a.dec", False) == scenario(tmp_path / "b.dec", True)
