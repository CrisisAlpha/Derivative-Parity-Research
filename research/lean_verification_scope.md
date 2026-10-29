# Formal verification contract (Lean 4)

**Current status: source drafted, compilation unverified.** The available working container
has no `lean`, `lake`, or `elan` installed and cannot reach GitHub to fetch a toolchain.
Do not mark these theorems verified until `lake build` passes using the pinned toolchain.

## Intended proved layer
- Boolean payoffs and set-inclusion bounds for joint and triple outcomes.
- Pathwise inclusion-exclusion inequality, including a short position in event B.
- Finite-state weak duality: positive state weights preserve pointwise hedge dominance.
- Sharpness criterion: every feasible model is bounded and models attain both endpoints.

## Still requiring formalization
- Derive explicit 8-state rational couplings attaining the 15% / 22% bounds.
- Full multi-date martingale constraints, conditional information filtrations.
- Prove the Python LP instances correspond to encoded Lean primal matrices.
- Verified extraction/validation of a SciPy dual solution as a rational certificate.
- Strong Kantorovich / martingale OT duality (do not claim proven).

## CI
`.github/workflows/lean.yml` runs Lean alongside separate Python tests.
Do not use `sorry`, `admit`, or opaque axioms to bypass formal verification.
Also note: absence of `sorry` does not establish correctness without successful compilation.
