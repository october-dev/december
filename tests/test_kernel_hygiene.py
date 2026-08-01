"""Static checks enforcing the kernel execution constraints in wiki/14 §D2.

These are the rules that cannot be tested behaviourally, because a violation
may only manifest on another machine, under another hash seed, or years into a
run. Catching them at the source level is the only reliable option.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

KERNEL_DIR = Path(__file__).resolve().parents[1] / "src" / "december"
KERNEL_FILES = sorted(KERNEL_DIR.rglob("*.py"))

# Wall-clock and entropy sources that would break replay if read inside the kernel.
BANNED_CALLS = {
    ("time", "time"),
    ("time", "monotonic"),
    ("time", "time_ns"),
    ("datetime", "now"),
    ("datetime", "utcnow"),
    ("datetime", "today"),
    ("random", "random"),
    ("random", "randint"),
    ("random", "choice"),
    ("random", "shuffle"),
    ("os", "urandom"),
    ("uuid", "uuid4"),
    ("uuid", "uuid1"),
}


def _iter_kernel_modules():
    for path in KERNEL_FILES:
        yield path, ast.parse(path.read_text(), filename=str(path))


def test_no_wall_clock_or_ambient_entropy_in_kernel():
    """Simulated time is a state variable; entropy comes from named streams."""
    offences = []
    for path, tree in _iter_kernel_modules():
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                value = node.func.value
                if isinstance(value, ast.Name):
                    if (value.id, node.func.attr) in BANNED_CALLS:
                        offences.append(f"{path.name}:{node.lineno} {value.id}.{node.func.attr}()")
    assert not offences, "wall-clock or ambient entropy in kernel:\n" + "\n".join(offences)


def test_no_bare_iteration_over_sets():
    """Set and frozenset iteration order is not deterministic.

    Iterating a set literal or a `set(...)` call directly in a for-loop is
    banned; `sorted(...)` around it is fine.
    """
    offences = []
    for path, tree in _iter_kernel_modules():
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                it = node.iter
                if isinstance(it, ast.Set):
                    offences.append(f"{path.name}:{node.lineno} iterates a set literal")
                if (
                    isinstance(it, ast.Call)
                    and isinstance(it.func, ast.Name)
                    and it.func.id in {"set", "frozenset"}
                ):
                    offences.append(f"{path.name}:{node.lineno} iterates set()")
    assert not offences, "nondeterministic iteration:\n" + "\n".join(offences)


def test_no_float_literals_in_transition_code():
    """Canonical state is integer-valued (ADR-006 Option A).

    Float literals are permitted only in `units.py`, which owns the
    float/integer boundary and must handle them.
    """
    allowed = {"units.py"}
    offences = []
    for path, tree in _iter_kernel_modules():
        if path.name in allowed:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, float):
                offences.append(f"{path.name}:{node.lineno} float literal {node.value!r}")
    assert not offences, "float literals outside the quantization boundary:\n" + "\n".join(offences)


def test_no_division_operator_in_kernel_state_paths():
    """`/` yields a float; integer state must use `//` or `apply_rate`."""
    allowed = {"units.py"}
    offences = []
    for path, tree in _iter_kernel_modules():
        if path.name in allowed:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                offences.append(f"{path.name}:{node.lineno} true division")
    assert not offences, "true division in kernel:\n" + "\n".join(offences)


def test_kernel_does_not_import_numpy():
    """NumPy is the single largest source of cross-platform stream drift.

    Excluding it from the kernel is what lets the RNG be portable by
    construction rather than by pinning.
    """
    offences = []
    for path, tree in _iter_kernel_modules():
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    if a.name.split(".")[0] == "numpy":
                        offences.append(f"{path.name}:{node.lineno}")
            if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] == "numpy":
                offences.append(f"{path.name}:{node.lineno}")
    assert not offences, "numpy imported into the kernel:\n" + "\n".join(offences)
