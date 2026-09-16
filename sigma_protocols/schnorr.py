"""Interactive Schnorr identification protocol.

A canonical sigma protocol: the prover convinces the verifier that she knows
the discrete logarithm x of her public key y = g^x (mod p) without revealing
anything about x (honest-verifier zero knowledge).

Protocol flow
-------------
1. Prover picks random k, sends commitment t = g^k.
2. Verifier replies with a random challenge c.
3. Prover sends response s = k + c*x (mod q).
4. Verifier accepts iff g^s = t * y^c (mod p).

Security properties: completeness (always accepts an honest prover),
special soundness (two accepting transcripts with different challenges yield
the secret), HVZK (transcripts are simulatable without the secret).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from common.group import G, P, Q, rand_scalar


@dataclass
class Prover:
    """Holds the secret key; single-use per identification session."""

    x: int  # secret key, an element of Z_q
    y: int = field(init=False)  # public key y = g^x mod p

    def __post_init__(self) -> None:
        self.y = pow(G, self.x, P)
        self._nonce: int | None = None

    @classmethod
    def generate(cls) -> "Prover":
        return cls(x=rand_scalar())

    def commit(self) -> int:
        """First protocol message: commitment t = g^k for random k."""
        self._nonce = rand_scalar()
        return pow(G, self._nonce, P)

    def respond(self, challenge: int) -> int:
        """Third protocol message: s = k + c*x mod q."""
        if self._nonce is None:
            raise RuntimeError("call commit() before respond()")
        s = (self._nonce + challenge * self.x) % Q
        self._nonce = None  # nonces must never be reused
        return s


@dataclass
class Verifier:
    """Checks the prover's claim against the public key y."""

    y: int

    def challenge(self) -> int:
        """Second protocol message: random c in Z_q."""
        return rand_scalar()

    def verify(self, commitment: int, challenge: int, response: int) -> bool:
        lhs = pow(G, response, P)
        rhs = (commitment * pow(self.y, challenge, P)) % P
        return lhs == rhs


def run_protocol(prover: Prover, verifier: Verifier) -> bool:
    """Run one full identification session."""
    commitment = prover.commit()
    challenge = verifier.challenge()
    response = prover.respond(challenge)
    return verifier.verify(commitment, challenge, response)


if __name__ == "__main__":
    prover = Prover.generate()
    verifier = Verifier(y=prover.y)
    print("Schnorr identification:", "ACCEPT" if run_protocol(prover, verifier) else "REJECT")
