# Roadmap

Phases are ordered by dependency. Each phase ends with working code + notes
committed to this repository.

## Phase 0 — Prerequisites
- [x] Cyclic groups, modular arithmetic, the discrete logarithm problem
- [x] Choosing safe parameters (RFC 3526 group 14, order-q subgroup)
- Notes: [math-prerequisites.md](math-prerequisites.md)

## Phase 1 — Commitments & sigma protocols ✅
- [x] Pedersen commitment scheme (`commitments/pedersen.py`) — hiding & binding
- [x] Schnorr identification protocol (`sigma_protocols/schnorr.py`)
- [x] Fiat-Shamir transform (`sigma_protocols/fiat_shamir.py`)
- [ ] Chaum-Pedersen protocol (proof of DH tuple equality)
- [ ] Okamoto's protocol (protocol with multiple generators)
- [ ] Write-up: security notions (completeness, soundness, zero-knowledge)

## Phase 2 — SNARKs: R1CS and Groth16
- [ ] Arithmetic circuits and R1CS arithmetization
- [ ] QAP (Quadratic Arithmetic Programs)
- [ ] Trusted setup (Powers of Tau ceremony, conceptually)
- [ ] Groth16 implementation (Python, then port to Rust/arkworks)
- Tooling to explore: `circom`/`snarkjs`, `arkworks`

## Phase 3 — PLONK and polynomial commitments
- [ ] PLONK arithmetization (wires, gates, permutation argument)
- [ ] KZG polynomial commitment scheme
- [ ] Universal trusted setup

## Phase 4 — STARKs
- [ ] Polynomial IOPs, low-degree testing
- [ ] FRI (Fast Reed-Solomon IOP)
- [ ] Hash-based commitments (no trusted setup)

## Phase 5 — Applications
- [ ] Range proofs (Bulletproofs-style, on top of Pedersen)
- [ ] Anonymous credentials (issuance + selective disclosure)
- [ ] Age verification without revealing the birthdate
- [ ] ZK-friendly hashing (Poseidon) and a toy private-voting demo

## Cross-cutting
- [ ] Port performance-critical modules to Rust (`arkworks` ecosystem)
- [ ] Continuous benchmarking notes (Python vs Rust proving times)
