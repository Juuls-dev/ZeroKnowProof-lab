"""Tests for the interactive Schnorr protocol."""
import unittest

from common.group import P, rand_scalar
from sigma_protocols.schnorr import Prover, Verifier, run_protocol


class TestSchnorr(unittest.TestCase):
    def test_honest_run_accepted(self):
        prover = Prover.generate()
        verifier = Verifier(y=prover.y)
        self.assertTrue(run_protocol(prover, verifier))

    def test_wrong_secret_rejected(self):
        prover = Prover.generate()
        # Verifier expects a public key for a *different* secret.
        verifier = Verifier(y=pow(prover.y, 2, P))
        self.assertFalse(run_protocol(prover, verifier))

    def test_wrong_challenge_rejected(self):
        prover = Prover.generate()
        commitment = prover.commit()
        response = prover.respond(challenge=rand_scalar())
        verifier = Verifier(y=prover.y)
        # Replay the response against a fresh, unrelated challenge.
        self.assertFalse(verifier.verify(commitment, rand_scalar(), response))

    def test_nonce_cleared_after_response(self):
        prover = Prover.generate()
        prover.commit()
        prover.respond(challenge=123)
        self.assertIsNone(prover._nonce)


if __name__ == "__main__":
    unittest.main()
