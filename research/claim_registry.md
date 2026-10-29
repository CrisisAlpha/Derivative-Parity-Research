# Research claims and verification register

**As of 2026-10-29: none of the Lean theorem drafts has been compiled in the original ChatGPT environment.** Do not state otherwise until Codex executes the pinned toolchain successfully.

| ID | Claim | Current status | Evidence available | Upgrade obligation |
| --- | --- | --- | --- | --- |
| S-01 | Three correlated binary events with six synthetic quote constraints have triple-event bounds [0.15, 0.22] | NUMERICAL_TESTED | `notebooks/01_correlated_event_ot.ipynb`, `tests/test_bounds.py` | Produce exact rational endpoint couplings and exact all-state hedge certificates; check in Lean |
| S-02 | Pathwise inclusion-exclusion lower hedge and event subset upper hedges hold for Bool outcomes | CONJECTURE_OR_HYPOTHESIS **as formal status** (Lean source drafted) | `LeanNotes.lean` | Compile with `lake build`, inspect assumptions, mark FORMALIZED_AND_COMPILED |
| S-03 | Finite-state nonnegative weights preserve payoff-order inequality | CONJECTURE_OR_HYPOTHESIS **as formal status** (Lean source drafted) | `LeanNotes.lean` | Compile and audit assumptions |
| M-01 | Synthetic two-date rally-then-decline claim has ordinary OT [0,0.50] versus martingale OT [1/12,1/4] | NUMERICAL_TESTED | `src/parity_ot/examples.py`, `tests/test_bounds.py` | Prove finite rational primal/dual certificates, and then Lean-check |
| M-02 | Synthetic three-date rally/decline/rebound claim has ordinary OT [0,1/4] versus martingale OT [0,1/16] | NUMERICAL_TESTED | `src/parity_ot/examples.py`, `tests/test_bounds.py` | Check every full-history martingale constraint with rational certificates; Lean-check |
| M-03 | Synthetic three-date monitored barrier has ordinary OT [1/4,1/2] versus martingale OT [11/40,3/8] | NUMERICAL_TESTED | `src/parity_ot/examples.py`, `tests/test_bounds.py` | Rational endpoint certificates and pathwise hedges |
| C-01 | Joint intersection-token price differs from conditional probability ratio unless explicitly normalized by the conditioning event | CONJECTURE_OR_HYPOTHESIS **as formal status** | `research/settlement_semantics.md` | State assumptions precisely, then formalize basic ratio bounds |
| E-01 | Observable market quotes offer empirically tighter out-of-sample price intervals / arbitrage flags | CONJECTURE_OR_HYPOTHESIS | `research/hypotheses_and_experiments.md` | Real contract dataset, common settlement normalization, executable quote checks |

A previous run of `PYTHONPATH=src python -m pytest -q` reported **9 passed** in the preparatory environment. This is not evidence that CI, `lake build`, or the new Codex checkout has passed.

## Audit evidence for every PR

Record Python command, exit status, and relevant version numbers; Lean toolchain and mathlib revisions; `lake build` result and theorems compiled; exact rational certificate code/data and how it was checked; any unverified statements; and GitHub CI run URL. Do not report “verified” on the basis of an unchecked screenshot or prose argument.
