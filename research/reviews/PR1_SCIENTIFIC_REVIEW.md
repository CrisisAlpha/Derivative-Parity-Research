# Scientific referee review: Derivative-Parity-Research PR #1

Date: 2026-10-29
PR: https://github.com/CrisisAlpha/Derivative-Parity-Research/pull/1
Reviewed head: `3756fa88b551e472a4c9155d9da9c55b5fd9a417`
Branch: `research/ot-lean-foundations` -> `main`
Status: REVISIONS REQUIRED. Keep draft; do not merge.

## Summary and independent verification

The finite-state OT/MOT proof-of-concept is substantively sound. I reviewed the
Lean source, quote constraints, dynamic-gain rows, exact-certificate algorithm,
tests, economic assumptions, and research-claim registry. I also independently
reconstructed the full discrete state spaces and all LP equality rows in a
separate exact-arithmetic implementation (BigInt rational arithmetic; not the
repository's Fraction verifier). It checked primal feasibility, dual statewise
inequalities, primal/dual objective equality, every extra quote, and all full
price-history gains. All sixteen lower/upper endpoints passed.

| Scenario | States | Equalities | Martingale history gains | Lower | Upper | Independent exact audit |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| binary | 8 | 7 | 0 | 3/20 | 11/50 | PASS |
| two_ot | 8 | 7 | 0 | 0 | 1/2 | PASS |
| two_mot | 8 | 9 | 2 | 1/12 | 1/4 | PASS |
| two_joint_mot | 8 | 10 | 2 | 1/10 | 1/5 | PASS |
| three_ot | 48 | 13 | 0 | 0 | 1/4 | PASS |
| three_mot | 48 | 23 | 10 | 0 | 1/16 | PASS |
| barrier_ot | 48 | 13 | 0 | 1/4 | 1/2 | PASS |
| barrier_mot | 48 | 23 | 10 | 11/40 | 3/8 | PASS |

The two named theorem declarations `ParityOT.Static.sharp_bounds` and
`ParityOT.TwoDate.sharp_bounds` genuinely quantify over all feasible real-valued
nonnegative state weights and assemble finite sharp bounds using pointwise
sub/superhedges plus explicitly attaining distributions. They are instance-specific,
not a proof of general Kantorovich or martingale OT strong duality. The documented
GitHub Actions runs for PR head `3756fa88` report success for both Python and Lean.
I reviewed the Lean source and CI evidence; I did not independently run Lean in my
own environment. The reported axiom audit covers 21 declarations.

An exact finite certificate has a simple correctness rationale. If all admissible
q satisfy q >= 0 and Aq=b, and each dual coefficient vector y_lo/y_hi satisfies
`y_lo A <= H <= y_hi A` componentwise, then `y_lo b <= H q <= y_hi b`.
Feasible rational q_lo/q_hi with objectives equal to the dual values establish
sharp endpoints for the **nonnegative** feasible class. This has been independently
checked for all eight models listed above.

## P0 / required corrections

### P0-A. Equivalence vs. nonnegative model laws

File: `research/dynamic_coherence.md` (first section) and cross-references in
`research/lean_verification_scope.md`, `manuscript/main.tex`.

The dynamic-coherence note assumes a common **equivalent** pricing measure Q,
but the formal feasible sets permit zero state weights. The static attaining
law `Static.qLo` places zero mass on 010 and `Static.qHi` on 101.

In fact, under full support (and hence Q(010)>0, Q(101)>0):

- At 010, the lower hedge `AB + BC - B` equals -1 while ABC equals 0.
  Therefore, any full-support Q prices ABC strictly above 3/20.
- At 101, the upper hedge AC equals 1 while ABC equals 0.
  Therefore, any full-support Q prices ABC strictly below 11/50.

The displayed sharp endpoints are **attained** in the nonnegative feasible class,
not in the class of equivalent Q to an everywhere-positive physical P. In these
particular examples a strictly positive admissible mixture of the two attaining
laws exists; the numerical infimum/supremum over full-support laws remain the
same, but they are no longer attained. Analogous slack arises in the two-date
examples. No physical reference P has been defined in the current model.

Acceptance criteria: distinguish `Q in P(Omega)` from `Q ~ P`; if equivalence is
mentioned, define P and its support, and distinguish extremum attainment from
infimum/supremum. Add a targeted note or regression that makes this distinction
explicit. Do not change valid Lean theorems merely to conceal this distinction.

### P0-B. Proof policy misses alternate Lean axiom syntax

File: `scripts/check_lean.py`, tests in `tests/test_lean_policy.py`.

The source checker forbids `axiom`, `sorry`, `unsafe` and other bypasses but
misses `constant` / `constants` (and the plural `axioms`). A Lean declaration
`constant c : False` creates a new axiom just as `axiom c : False` does. The
existing 21 audited declarations report only standard foundations; this is a
future CI enforcement loophole, NOT an allegation that the current theorems
are invalid.

Acceptance criteria: reject unauthorized custom constant/axiom declarations,
including alternate syntax, with negative tests; audit every new theorem
promoted to `FORMALIZED_AND_COMPILED` in the claim register, not just a static
hardcoded subset. Prefer the kernel's reported axiom dependencies as the
ultimate trust check, with source scanning as defense in depth.

Lean documentation: https://lean-lang.org/doc/reference/latest/Axioms

### P0-C. Rebuild the current LaTeX source

Files: `manuscript/main.tex`, `manuscript/main.pdf`, CI.

The repository openly acknowledges that the checked-in PDF is a historical
handoff artifact, not a build of current `main.tex`. Add a reproducible
`latexmk -pdf` build in CI (or an equivalent pinned build procedure), verify
figures and bibliography, and make sure any downloadable manuscript artifact
is generated from current source. The stale PDF must not be presented as the
reviewed current paper.

## P1 / recommended improvements

1. **Default branch:** The repository currently lists `research/ot-lean-foundations`
   as its default branch; the `main` PR base is an empty root commit. Make
   the canonical default intentionally `main` when appropriate, so cloning
   and future review workflows do not silently treat an unmerged branch as
   accepted research.
2. **Conditional identity status:** The registry classifies
   `Q(B|A)=Q(A and B)/Q(A)` under `CONJECTURE_OR_HYPOTHESIS`. Given Q(A)>0,
   this is a mathematical identity, not a conjecture. Say "established
   mathematically; Lean formalization outstanding", while leaving actual
   venue settlement interpretation to a separate empirical protocol.
3. **Conditional API semantics:** If `conditional_ratio_interval` is advertised
   as a conditional-probability solver, validate or explicitly assume
   `0 <= numerator <= conditioning <= 1` on each state, plus indicator
   interpretation. A general payoff ratio is not necessarily a probability.
4. **Filtration precision:** The implemented constraints are full history of
   *monitored asset-price observations*, not the complete information field
   available to market participants. Preserve that qualification in text.
5. **Next Lean scope:** Formalize 48-state MOT rebound/barrier primal/dual
   certificates and then the Python-to-Lean model bridge. Continue to label
   the 48-state results RATIONAL_CERTIFIED until those declarations are built
   and axiom-audited. No empirical or general-duality claim is yet supported.

## Acceptance gate

Keep PR #1 in draft until all P0 fixes are committed and separately passing
Lean, Python, and LaTeX builds are visible, with a short changelog. The already
proven synthetic bounds may remain. Do not merge automatically or claim
publication readiness or executable arbitrage. Request a new scientific
review on the updated head SHA.

## Tooling limitation

I attempted a GitHub PR review and a PR discussion comment via the ChatGPT
GitHub connector. Both were rejected with HTTP 403 `Resource not accessible by
integration`; therefore THIS REVIEW WAS NOT POSTED TO GITHUB. This file is the
portable review record for Codex or a user to attach to the pull request.
