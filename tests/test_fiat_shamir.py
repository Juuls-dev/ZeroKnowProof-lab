"""Tests for the Fiat-Shamir transformed Schnorr proof."""
import unittest

from common.group import G, P, Q, rand_scalar
from sigma_protocols.fiat_shamir import prove, verify


class TestFiatShamir(unittest.TestCase):
    def test_valid_proof_verifies(self):
        y, t, s = prove(rand_scalar())
        self.assertTrue(verify(y, t, s))

    def test_tampered_commitment_rejected(self):
        y, t, s = prove(rand_scalar())
        self.assertFalse(verify(y, (t + 1) % P, s))

    def test_tampered_response_rejected(self):
        y, t, s = prove(rand_scalar())
        self.assertFalse(verify(y, t, (s + 1) % Q))

    def test_wrong_public_key_rejected(self):
        y, t, s = prove(rand_scalar())
        wrong_y = pow(G, rand_scalar(), P)
        self.assertFalse(verify(wrong_y, t, s))


if __name__ == "__main__":
    unittest.main()
