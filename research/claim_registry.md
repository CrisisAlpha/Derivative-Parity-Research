# Research claims and verification register

As of **2026-10-29 (Asia/Hong_Kong)**: local Python verification and the pinned
Lean build **PASS**. The initial 9 tests were independently reproduced; the
expanded suite passes 28 tests. `lake build` and the 21-declaration axiom audit
both exit 0. GitHub CI status is recorded separately; local success is not a
claim that remote CI has run. All scenario data are synthetic.

| ID | Exact claim | Status | Evidence and boundary |
| --- | --- | --- | --- |
| S-01 | For eight Boolean states, nonnegative real masses summing to one and exact A,B,C,AB,BC,AC quotes 3/5,11/20,9/20,2/5,3/10,11/50 imply ABC bounds [3/20,11/50], with both endpoints attained | **FORMALIZED_AND_COMPILED** | `ParityOT.Static.sharp_bounds`; `qLo_feasible`, `qHi_feasible`, `qLo_attains`, `qHi_attains`, `pathwise`, `hedge_costs`, `all_feasible_bounds` in `StaticCertificate.lean`. Actual pinned build and axiom audit pass. Independent rational certificate `binary` checks all 8 states and all 7 normalization/quote equations. |
| S-02 | Boolean triple subset bounds and AB+BC-B lower subhedge | **FORMALIZED_AND_COMPILED** | `ParityOT.triple_le_ac`, `triple_le_ab`, `lower_subhedge`; no axioms. The last theorem was renamed from the misleading draft name `lower_superhedge`. |
| S-03 | Nonnegative rational weights preserve finite pointwise payoff order | **FORMALIZED_AND_COMPILED** | `ParityOT.weighted_bound`; nonnegativity and pointwise dominance are explicit hypotheses. |
| S-04 | Universal bounds and two feasible attaining laws imply sharp endpoints | **FORMALIZED_AND_COMPILED** | `ParityOT.bound_with_attainment`; assembly lemma **assumes** bounds and attainment, not a strong-duality theorem or standalone instance proof. |
| S-05 | Static marginal-only [0,9/20], adjacent-pair [3/20,3/10], conditional C given AB [3/8,11/20], and band-ratio regressions | **NUMERICAL_TESTED** | `test_binary_three_event_bounds_and_conditional`, `test_conditional_ratio_with_exact_and_band_quote`; these variants/ratios are not separately Lean-formalized. |
| S-06 | Maximum-entropy fit P(111) approximately 0.18448614805 and P(101) approximately 0.03551385195 | **NUMERICAL_TESTED** | Re-executed `notebooks/01_correlated_event_ot.ipynb` moment and value assertions; model selection, not a model-free price or formal optimum. |
| M-01 | Two-date full-history MOT digital bounds [1/12,1/4], both attained | **FORMALIZED_AND_COMPILED** | `ParityOT.TwoDate.sharp_bounds`, supported by both `q*_feasible`, `q*_attains`, `pathwise`, `hedge_costs`, `all_feasible_bounds`. Every first-date history has a zero-gain equation. Scope is the eight specified states over all real laws, not general MOT. |
| M-01-OT | Corresponding ordinary two-date OT bounds [0,1/2] | **RATIONAL_CERTIFIED** | `two_ot` explicit rational primal/dual pair; exact all-state/all-constraint checks. Not Lean-checked. |
| M-01-J | Adding joint Q(110,130)=1/5 gives two-date MOT [1/10,1/5] | **RATIONAL_CERTIFIED** | `two_joint_mot`; checks both history gains and the extra quote. Not Lean-checked. |
| M-02 | Three-date rebound: ordinary OT [0,1/4], full-history MOT [0,1/16] | **RATIONAL_CERTIFIED** | `three_ot`, `three_mot` in `data/synthetic/rational_certificates.json`; all 48 state inequalities, all marginal equations, and all 10 history gains checked exactly. Lean certificates remain open. |
| M-03 | Three-date discrete barrier: ordinary OT [1/4,1/2], full-history MOT [11/40,3/8] | **RATIONAL_CERTIFIED** | `barrier_ot`, `barrier_mot`; same exact 48-state and 10-history checks. Lean certificates and continuous monitoring remain open. |
| C-01 | Intersection settlement differs from a normalized conditional ratio, requiring positive conditioning price | **CONJECTURE_OR_HYPOTHESIS** (formal obligation only) | Economic/mathematical assumptions stated in `research/settlement_semantics.md` and manuscript; ratio code numerically tested under S-05. No named Lean ratio theorem is claimed. |
| E-01 | Live market quotes yield useful out-of-sample tightening or executable violations | **CONJECTURE_OR_HYPOTHESIS** | No live market dataset, trades or empirical validation; see `research/hypotheses_and_experiments.md`. |

## Evidence and accepted foundations

- Lean 4.20.0 (`77cfc4d1a4f6`), mathlib v4.20.0 at
  `c211948581bde9846a99e32d97a03f0d5307c31e`; transitive pins in `lake-manifest.json`.
- `AxiomAudit.lean` prints all 21 named theorem dependencies. The three Boolean
  lemmas use no axioms. All remaining audited statements use only `propext`,
  `Classical.choice`, `Quot.sound`; no project-specific axioms or proof gaps.
- `python scripts/check_lean.py`: source guard, actual `lake build`, and fail-closed
  axiom allowlist. The separate Python job does not establish Lean success.
- `python -m parity_ot.certificates`: 8 exact primal/dual pairs pass (16 endpoints).
  `research/rational_certificates.md` gives explicit distributions and coefficients.
  Candidate generation uses floating-point HiGHS, but every accepted candidate is
  rechecked with exact Fraction arithmetic against an independently constructed model.
- `test_exact_model_matches_solver_instances` checks the exact matrices/payoffs
  against the numerical examples. This is NOT a formal bridge or verified solver.
- Commands, versions, setup failures and final outcomes: `outputs/QA.md` and logs
  in `outputs/validation/`. A fresh LaTeX build was not run; the imported PDF is stale
  relative to the updated manuscript source.

## Remaining proof obligations

Three-date Lean certificates; ordinary OT and extra-joint-quote Lean certificates;
formal Python-to-Lean model correspondence; conditional-ratio/quote-band duality;
general Kantorovich/MOT strong duality; arbitrary filtrations and continuous time.
No market completeness is presumed. Pricing requires a common measure, numeraire
and settlement convention; MOT additionally requires the stated tradable discounted
underlying. Nontradable news/election/sports events receive no martingale assumption.
A model interval or certificate is not a traded arbitrage.
