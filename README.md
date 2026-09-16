# ZeroKnowProof-lab

Personal study project on **zero-knowledge proof (ZKP) protocols** — from classic
sigma protocols to modern SNARKs/STARKs — implemented from scratch for learning.

> Juuls CS student, Moscow State University '28 · interested in ML & cybersecurity

## Why this project

Zero-knowledge proofs let one party prove a statement is true *without revealing
anything beyond its truth*. They are a cornerstone of modern cryptography:
privacy-preserving authentication, blockchain scaling (zk-Rollups), secure
voting, and verifiable computation. 

**Goal:** a public, well-tested implementation of each major ZKP family, with
explanatory write-ups.

## Roadmap

| Phase | Topic | Status |
|-------|-------|--------|
| 0 | Mathematical prerequisites (finite fields, groups, discrete log) | notes |
| 1 | Commitments & sigma protocols (Pedersen, Schnorr, Fiat-Shamir) |  implemented |
| 2 | Circuit arithmetization (R1CS) and Groth16 | next |
| 3 | PLONK and polynomial commitment schemes (KZG) | planned |
| 4 | STARKs (FRI, low-degree testing) | planned |
| 5 | Applications: anonymous credentials, range proofs, private inference | planned |

See [docs/roadmap.md](docs/roadmap.md) for details.

## Repository structure

```
ZeroKnowProof-lab/
├── common/            # shared group parameters (RFC 3526 group 14) and helpers
├── sigma_protocols/   # Schnorr identification, Fiat-Shamir transform
├── commitments/       # Pedersen commitments
├── tests/             # unit tests (stdlib unittest)
└── docs/              # roadmap and math notes
```

## Quickstart

No dependencies — standard library only (Python 3.10+).

```bash
python -m unittest discover -s tests -v
python -m sigma_protocols.schnorr
python -m sigma_protocols.fiat_shamir
python -m commitments.pedersen
```

> ⚠️ All code is **educational**. It uses textbook constructions with clean
> group parameters (RFC 3526 2048-bit MODP group) but no constant-time
> operations or side-channel hardening — do not use in production.

## Learning resources

- Boneh & Shoup, *A Graduate Course in Applied Cryptography* 
- Justin Thaler, *Proofs, Arguments, and Zero-Knowledge* 
- ZKProof community resources — [zkproof.org](https://zkproof.org)
- MIT 6.857 / Stanford CS251 lecture materials
- AI tools

