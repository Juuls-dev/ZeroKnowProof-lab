"""Fiat-Shamir transform: make Schnorr non-interactive.

The interactive challenge c is replaced by a hash of the protocol transcript,
which makes the proof publicly verifiable without a back-and-forth:

    c = H(domain || y || t)          (hash to scalar)
    s = k + c*x mod q

The output (t, s) is a signature-of-knowledge of x. The same construction is
the foundation of Schnorr signatures and a stepping stone to SNARKs, where the
"hash" is replaced by a polynomial commitment argument.
"""
from __future__ import annotations

from common.group import G, P, Q, int_to_bytes, hash_to_scalar, rand_scalar

_DOMAIN = b"zkplab/schnorr-fs/v1"


def prove(x: int) -> tuple[int, int, int]:
    """Produce a non-interactive proof of knowledge of x. Returns (y, t, s)."""
    y = pow(G, x, P)
    k = rand_scalar()
    t = pow(G, k, P)
    c = hash_to_scalar(_DOMAIN, int_to_bytes(y), int_to_bytes(t))
    s = (k + c * x) % Q
    return y, t, s


def verify(y: int, commitment: int, response: int) -> bool:
    """Check a Fiat-Shamir Schnorr proof (y, t, s)."""
    c = hash_to_scalar(_DOMAIN, int_to_bytes(y), int_to_bytes(commitment))
    lhs = pow(G, response, P)
    rhs = (commitment * pow(y, c, P)) % P
    return lhs == rhs


if __name__ == "__main__":
    from common.group import rand_scalar

    secret = rand_scalar()
    proof = prove(secret)
    print("Fiat-Shamir Schnorr proof:", "ACCEPT" if verify(*proof) else "REJECT")
