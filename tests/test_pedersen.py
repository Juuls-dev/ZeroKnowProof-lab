"""Tests for Pedersen commitments."""
import unittest

from commitments.pedersen import add, commit, open_commitment
from common.group import Q, rand_scalar


class TestPedersen(unittest.TestCase):
    def test_open_valid_commitment(self):
        c, r = commit(42)
        self.assertTrue(open_commitment(c, 42, r))

    def test_wrong_message_rejected(self):
        c, r = commit(42)
        self.assertFalse(open_commitment(c, 43, r))

    def test_wrong_randomness_rejected(self):
        c, r = commit(42)
        self.assertFalse(open_commitment(c, 42, (r + 1) % Q))

    def test_homomorphic_addition(self):
        c1, r1 = commit(10)
        c2, r2 = commit(32)
        c_sum = add(c1, c2)
        self.assertTrue(open_commitment(c_sum, 42, (r1 + r2) % Q))

    def test_commitment_deterministic_given_randomness(self):
        c1, r = commit(7, randomness=rand_scalar())
        c2, _ = commit(7, randomness=r)
        self.assertEqual(c1, c2)


if __name__ == "__main__":
    unittest.main()
