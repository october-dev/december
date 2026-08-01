"""Canonical serialization.

Every hash in December is taken over bytes produced here. The encoding must be
deterministic across platforms and Python versions, which rules out `repr`,
`pickle`, and any float representation.

The format is a small self-describing binary encoding rather than JSON, because
JSON would happily accept a float and because its number formatting is a
platform question we do not want to inherit. Refusing floats at the encoder is
what makes the ADR-006 "no float in canonical state" rule enforceable rather
than aspirational.
"""

from __future__ import annotations

from typing import Any

# Type tags. Never renumber these — doing so silently changes every historical
# hash. Adding a new tag is a schema change requiring a digest-version bump.
_T_NULL = b"\x00"
_T_FALSE = b"\x01"
_T_TRUE = b"\x02"
_T_INT = b"\x03"
_T_STR = b"\x04"
_T_BYTES = b"\x05"
_T_LIST = b"\x06"
_T_MAP = b"\x07"


class CanonicalEncodingError(TypeError):
    """A value cannot be canonically encoded."""


def _encode_uint(n: int) -> bytes:
    """Length-prefixed big-endian unsigned integer."""
    if n == 0:
        return b"\x00"
    width = (n.bit_length() + 7) // 8
    return bytes([width]) + n.to_bytes(width, "big")


def _encode_int(n: int) -> bytes:
    """Sign byte followed by magnitude, so -0 and 0 cannot differ."""
    sign = b"\x00" if n >= 0 else b"\x01"
    return sign + _encode_uint(abs(n))


def encode(value: Any) -> bytes:
    """Encode a value to canonical bytes.

    Accepts None, bool, int, str, bytes, list/tuple, and dict with str keys.
    Rejects floats explicitly — the error message is deliberately loud because
    a float reaching this function means a transition wrote unquantized state.
    """
    if value is None:
        return _T_NULL
    if value is True:
        return _T_TRUE
    if value is False:
        return _T_FALSE
    if isinstance(value, float):
        raise CanonicalEncodingError(
            "float in canonical state; quantize it first (ADR-006 Option A). "
            f"Offending value: {value!r}"
        )
    if isinstance(value, int):
        return _T_INT + _encode_int(value)
    if isinstance(value, str):
        raw = value.encode("utf-8")
        return _T_STR + _encode_uint(len(raw)) + raw
    if isinstance(value, bytes):
        return _T_BYTES + _encode_uint(len(value)) + value
    if isinstance(value, (list, tuple)):
        out = [_T_LIST, _encode_uint(len(value))]
        out.extend(encode(v) for v in value)
        return b"".join(out)
    if isinstance(value, dict):
        # Sorting by the encoded key makes ordering independent of both
        # insertion order and locale collation.
        items = sorted(value.items(), key=lambda kv: str(kv[0]).encode("utf-8"))
        out = [_T_MAP, _encode_uint(len(items))]
        for k, v in items:
            if not isinstance(k, str):
                raise CanonicalEncodingError(f"map keys must be str, got {type(k).__name__}")
            out.append(encode(k))
            out.append(encode(v))
        return b"".join(out)
    if isinstance(value, (set, frozenset)):
        raise CanonicalEncodingError(
            "set/frozenset is not canonically encodable: iteration order is not "
            "deterministic. Convert to a sorted list first."
        )
    raise CanonicalEncodingError(f"not canonically encodable: {type(value).__name__}")
