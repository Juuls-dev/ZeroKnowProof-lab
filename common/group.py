"""Shared group parameters and helpers for ZeroKnowProof-lab exercises.

Every protocol in this repository works in the order-q subgroup of Z_p^*,
where p is the 2048-bit safe prime of RFC 3526 "group 14" and q = (p-1)/2.

Educational code only -- do not use in production.
"""
from __future__ import annotations

import hashlib
import secrets

_P_HEX = (
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
    "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
    "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
    "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
    "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
    "15728E5A8AACAA68FFFFFFFFFFFFFFFF"
)

# Modulus and subgroup order.
P: int = int(_P_HEX, 16)
Q: int = (P - 1) // 2

# Generator of the order-q subgroup: 2 is a generator of the full group
# (RFC 3526), so 2^2 = 4 generates the subgroup of order q.
G: int = pow(2, 2, P)


def rand_scalar() -> int:
    """Uniform random element of Z_q."""
    return secrets.randbelow(Q)


def int_to_bytes(n: int) -> bytes:
    """Fixed-width big-endian encoding of a group element / scalar."""
    return n.to_bytes((P.bit_length() + 7) // 8, "big")


def _hash_parts(*parts: bytes) -> bytes:
    h = hashlib.sha256()
    for part in parts:
        h.update(len(part).to_bytes(4, "big"))
        h.update(part)
    return h.digest()


def hash_to_scalar(*parts: bytes) -> int:
    """Hash arbitrary byte strings to a scalar in Z_q (Fiat-Shamir)."""
    return int.from_bytes(_hash_parts(*parts), "big") % Q


def hash_to_group(*parts: bytes) -> int:
    """Hash arbitrary byte strings to an element of the order-q subgroup."""
    x = int.from_bytes(_hash_parts(*parts), "big") % P
    return pow(x, 2, P)  # squaring maps any element into the subgroup
