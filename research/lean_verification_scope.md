# Formal verification scope (Lean 4)

**Actual local build: PASS. All 21 audited declarations pass the axiom allowlist.**
The build log and axiom output are recorded under `outputs/validation/`; see `outputs/QA.md`.
Toolchain: `leanprover/lean4:v4.20.0`; mathlib tag `v4.20.0`, commit
`c211948581bde9846a99e32d97a03f0d5307c31e`. Transitive revisions are locked in
`lake-manifest.json`. No dependency version was upgraded.

## Statements and explicit assumptions

- `LeanNotes.lean`: Boolean subset and inclusion-exclusion payoffs;
  `weighted_bound` assumes nonnegative rational weights and pointwise dominance.
  `bound_with_attainment` is a generic assembly lemma that **assumes** universal
  bounds and endpoint feasibility/attainment; by itself it proves no LP instance.
- `StaticCertificate.lean`: `ParityOT.Static.sharp_bounds` quantifies over **all real**
  nonnegative eight-state laws with total mass one and six exact quote equations.
  State order is 000, 001, 010, 011, 100, 101, 110, 111; quotes for A, B, C, AB, BC,
  AC are 3/5, 11/20, 9/20, 2/5, 3/10, 11/50. The target is ABC.
  Explicit rational `qLo` and `qHi` attain 3/20 and 11/50. `pathwise` checks
  AB + BC - B <= ABC <= AC on each state; `hedge_costs` and `all_feasible_bounds`
  connect those inequalities to every feasible law.
- `TwoDateCertificate.lean`: `ParityOT.TwoDate.sharp_bounds` quantifies over all
  real nonnegative laws on {90,110} x {70,90,110,130}. Mass is one, first-date
  high mass is 1/2 (the low mass follows by normalization), and each terminal
  mass is 1/4. BOTH history gains, after 90 and after 110, have zero expectation.
  The target is 1{S1=110, S2<=90}; rational witnesses attain 1/12 and 1/4.
  The lower and upper dynamic hedges are the explicit formulas in the manuscript.

These models presume common normalized pricing and settlement payoffs. The MOT
interpretation additionally presumes a discounted dynamically tradable asset,
zero funding/interest/payout adjustments in this toy model, and the natural
price filtration. None of these economic hypotheses is inferred from live data.
No martingale condition is imposed on nontradable event histories. Ratios need
a positive conditioning price and compatible settlement normalization; an
intersection token is not automatically a conditional-probability token.

## Trust boundary and CI

Run `python scripts/check_lean.py` with `lake` on PATH. It scans every project Lean
file, runs **lake build**, then typechecks `AxiomAudit.lean` with warnings as errors.
It requires output for every audited declaration and permits only `propext`,
`Classical.choice`, and `Quot.sound`; a missing audit, unexpected axiom, proof gap,
unsafe declaration or native-decision shortcut fails the command. The real-valued
definitions use `noncomputable` because real division has no executable code;
their proofs remain kernel checked. The separate Python workflow cannot make
Lean CI green. `tests/test_lean_policy.py` exercises the rejection paths.

## Open obligations (not claimed)

- Lean certificates for the three-date 48-state rebound and barrier instances,
  ordinary OT variants, and the extra two-date joint quote. All have separately
  checked rational primal/dual certificates in Python, including every history.
- A Lean-verified bridge from Python's state/constraint construction to the Lean
  definitions. Python exact-model correspondence tests are useful evidence,
  not a verified compiler or solver extraction theorem.
- General Kantorovich/MOT strong duality, arbitrary-filtration conditional
  expectation theory, continuous-time limits and continuous barrier monitoring.
- Formal conditional-ratio optimization, quote-band duality, entropy models,
  executable trading assumptions and empirical assertions.

Finite instance certificates prove bounds plus attaining models without invoking
a general strong-duality theorem. Float regression tests alone do not certify an
optimum. Neither exact nor formal finite bounds establish a traded arbitrage.
