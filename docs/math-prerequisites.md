# Math prerequisites

Condensed notes on the algebra behind everything in this repository.
Target: enough intuition to read the code, not a full course.

## 1. Modular arithmetic

Computation in `Z_n = {0, 1, ..., n-1}` with addition/multiplication taken
modulo `n`. Every algorithm here works modulo a large prime `p`, so `Z_p` is a
**field**: every nonzero element has a multiplicative inverse (found with the
extended Euclidean algorithm).

## 2. Cyclic groups and generators

`Z_p*` (nonzero elements under multiplication) is a cyclic group of order
`p-1`: there is a generator `g` such that `{g^0, g^1, ..., g^(p-2)}` covers
all of `Z_p*`.

For a **safe prime** `p = 2q + 1` (both `p` and `q` prime), the subgroup of
**quadratic residues** — elements `x = y^2 mod p` — has prime order `q`. We
work there: `4 = 2^2` generates it (RFC 3526 group 14, used in
`common/group.py`).

Why prime order matters: exponents live in `Z_q`, which is itself a field, so
division/extraction works cleanly and every non-identity element generates the
whole subgroup.

## 3. Discrete logarithm problem (DLP)

Given `g` and `y = g^x mod p`, find `x`. For well-chosen 2048-bit `p` this is
computationally infeasible (index calculus, the best known attack, is ~`2^100`).

**Everything in this repo is "hard because DLP is hard":**
- Schnorr soundness: extracting `x` from two accepting transcripts requires
  solving for the secret, i.e. knowledge of `x` itself (special soundness).
- Pedersen binding: opening one commitment to two messages reveals
  `log_g(h)`.

## 4. The three security notions of a ZK protocol

| Notion | Question | Schnorr |
|--------|----------|---------|
| Completeness | Does an honest prover always convince an honest verifier? | Yes: `g^(k+cx) = g^k · (g^x)^c` |
| Soundness | Can a cheating prover succeed without knowing the secret? | Only with probability ~1/q per attempt |
| Zero-knowledge | Does the verifier learn anything beyond truth? | Transcripts are simulatable (HVZK) |

## 5. Random self-reducibility & hashing into the group

- **Fiat-Shamir**: a public hash replaces the verifier's random challenge,
  turning 3 messages into a signature-of-knowledge. Security holds in the
  *random oracle model*.
- **Hash-to-group**: `SHA-256` output squared modulo `p` gives an element of
  the order-q subgroup; used to derive the Pedersen base `h` with unknown
  discrete log.

## Further reading
- Boneh & Shoup, chapters 1–2, 10
- Victor Shoup, *A Computational Introduction to Modern Number Theory*
