"""Fixed-unit integer quantities for canonical world state.

Implements ADR-006 Option A. Every conserved or discrete quantity that enters
canonical state is a scaled integer with a declared unit. Floating point is
permitted *inside* a transition calculation, but only its explicitly quantized
output may be stored, and quantization always goes through `quantize` so the
rounding rule cannot drift between subsystems.

The declared units are deliberately small so that realistic world quantities
never need fractions: grain is grams, water is millilitres, energy is
kilojoules, time is seconds, distance is millimetres.
"""

from __future__ import annotations

from typing import Final, NewType

# Declared canonical units. Extending this set is a schema change (ADR-006).
Grams = NewType("Grams", int)
Millilitres = NewType("Millilitres", int)
Kilojoules = NewType("Kilojoules", int)
Seconds = NewType("Seconds", int)
Millimetres = NewType("Millimetres", int)
SquareMetres = NewType("SquareMetres", int)
Count = NewType("Count", int)

# Proportions and rates are parts-per-million, so that a "percentage" is an
# integer and no ratio ever introduces a float into canonical state.
PPM = NewType("PPM", int)
PPM_ONE: Final[int] = 1_000_000


class QuantizationError(ValueError):
    """A value could not be quantized into canonical integer state."""


def quantize(value: float | int, *, unit: str = "unit") -> int:
    """Convert a computed value into a canonical integer.

    This is the single boundary between float arithmetic (allowed inside a
    transition) and canonical state (never float). Rounding is half-to-even,
    matching IEEE 754's default mode, so it is stable across platforms and
    unbiased over many draws — a biased rule would accumulate drift in a world
    that quantizes millions of times.

    NaN and infinity are rejected rather than silently coerced: they indicate a
    defective transition, and admitting them would poison the event log.
    """
    if isinstance(value, bool):  # bool is an int subclass; almost never intended
        raise QuantizationError(f"refusing to quantize a bool as {unit}")
    if isinstance(value, int):
        return value
    if value != value:  # NaN
        raise QuantizationError(f"cannot quantize NaN as {unit}")
    if value in (float("inf"), float("-inf")):
        raise QuantizationError(f"cannot quantize {value} as {unit}")
    # round() is half-to-even in Python and returns int for a 1-arg call.
    return round(value)


def apply_rate(amount: int, rate_ppm: int) -> int:
    """Apply a parts-per-million rate to an integer quantity, exactly.

    Uses integer arithmetic throughout, so the result is identical on every
    platform and needs no quantization. Ties round half-to-even to match
    `quantize`.
    """
    if rate_ppm < 0:
        raise ValueError("rate_ppm must be non-negative")
    numerator = amount * rate_ppm
    whole, remainder = divmod(numerator, PPM_ONE)
    twice = remainder * 2
    if twice > PPM_ONE or (twice == PPM_ONE and whole % 2 == 1):
        whole += 1
    return whole


def is_canonical_scalar(value: object) -> bool:
    """True if `value` may appear in canonical state or an event payload.

    Floats are excluded by design. This predicate is the enforcement point for
    the ADR-006 property test that no canonical field is float-typed.
    """
    if isinstance(value, bool):
        return True
    if isinstance(value, int):
        return True
    return isinstance(value, (str, bytes, type(None)))
