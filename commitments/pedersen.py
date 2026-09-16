"""Pedersen commitments: perfectly hiding, computationally binding.

A commitment to message m is C = g^m * h^r (mod p), where r is random and h
is a second group generator whose discrete logarithm relative to g is unknown
(it is derived by hashing a fixed domain string into the group).

Properties
----------
* Perfectly hiding: for every commitment there is exactly one randomness r
  making it match any message, so the receiver learns nothing about m.
* Computationally binding: opening the same commitment to two different
  messages would reveal log_g(h), breaking the discrete logarithm assumption.
* Homomorphic: C(m1, r1) * C(m2, r2) = C(m1+m2, r1+r2) -- the core property
  used inside many zero-knowledge protocols (e.g. range proofs).
"""
from __future__ import annotations

from common.group import G, P, Q, hash_to_group, rand_scalar

# Second generator with (heuristically) unknown discrete log relative to G.
H: int = hash_to_group(b"zkplab/pedersen-base-h/v1")


def commit(message: int, randomness: int | None = None) -> tuple[int, int]:
    """Commit to ``message`` in Z_q. Returns (commitment, randomness used)."""
    if not 0 <= message < Q:
        raise ValueError("message must be in Z_q")
    r = rand_scalar() if randomness is None else randomness % Q
    c = (pow(G, message, P) * pow(H, r, P)) % P
    return c, r


def open_commitment(commitment: int, message: int, randomness: int) -> bool:
    """Check that ``commitment`` opens to ``message`` with ``randomness``."""
    expected, _ = commit(message, randomness)
    return expected == commitment


def add(commitment1: int, commitment2: int) -> int:
    """Homomorphic addition: result commits to m1 + m2 with r1 + r2."""
    return (commitment1 * commitment2) % P


if __name__ == "__main__":
    c, r = commit(42)
    print("Pedersen open:", "OK" if open_commitment(c, 42, r) else "FAIL")
    c1, r1 = commit(10)
    c2, r2 = commit(32)
    c_sum = add(c1, c2)
    print("Homomorphic add:", "OK" if open_commitment(c_sum, 42, (r1 + r2) % Q) else "FAIL")
