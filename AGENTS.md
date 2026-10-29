# Codex repository instructions — Derivative Parity Research

## Mission and scope
This repository studies robust pricing and mathematical parity across binary / conditional event contracts, option-implied marginals, and (only when an underlying is dynamically tradable) martingale optimal transport. Work as a quantitative researcher and research engineer, not a generic app developer. Maintain scientific reproducibility and do not invent empirical quotes, verified proofs, or executable arbitrage.

## Scientific trust levels (mandatory)
Each quantitative claim must have one of the following statuses, recorded in `research/claim_registry.md`:
- **FORMALIZED_AND_COMPILED**: a named Lean 4 theorem compiles using the pinned toolchain and dependencies, with its assumptions explicit. State the theorem name, compiler result, and imported axioms when relevant.
- **RATIONAL_CERTIFIED**: an explicit primal feasible rational witness and a statewise-valid rational dual hedge certify a finite LP endpoint. This is *not* a Lean proof unless those exact witnesses are checked inside Lean.
- **NUMERICAL_TESTED**: floating-point solver output has passed named reproducible Python tests with tolerances; it is not an exact certificate.
- **CONJECTURE_OR_HYPOTHESIS**: mathematical conjecture, proposed novelty, or untested empirical assertion.
Never promote a status without the required evidence. Existing Lean source is **draft, not yet compiled**, despite prior Python tests passing.

## Required tooling and execution
- Use the pinned `lean-toolchain`, `lakefile.lean`, and a consistent mathlib revision; compile by running `lake update` only when necessary and `lake build`.
- Do not use `sorry`, `admit`, `unsafe` proof shortcuts, or new project-specific `axiom` declarations to pass CI. Do not suppress failed checks. Mathlib's standard mathematical foundations can remain in scope.
- Prefer kernel-checkable finite definitions over untrusted solver-oracle assumptions. Inspect `#print axioms` for the central theorems, and distinguish accepted foundations from newly introduced assumptions.
- Run `python -m pip install -e '.[test,research]'` and `python -m pytest -q`; `PYTHONPATH=src python -m pytest -q` is acceptable if dependencies already exist. Re-run any numerical examples before claiming their values.
- CI must include separately failing Lean and Python jobs. The existence of an action file or green Python job does not imply Lean verification.
- If `lake build` fails, diagnose and fix; if unresolved, report exactly why, keep status unverified, and leave the pull request in draft.

## Proof and solver standards
- Model binary events by explicit state payoffs and the correct settlement rules; an intersection token is not automatically a conditional-probability token.
- Explicitly list constraints defining an admissible distribution, including normalization, nonnegativity, available quote bands, and temporal information structure.
- For static finite OT, prefer rational dual inequalities *on every state* plus explicit rational primal couplings attaining endpoints. Avoid claiming a general strong-duality theorem when only finite witnesses were proved.
- For MOT, the conditional martingale equation must be imposed at each time on every history / atom of the filtration. A marginal mean equality alone is insufficient.
- For financial underlyings, specify numeraire, discounting, tradability and funding assumptions. Nonfinancial event histories are not generally martingales.
- For conditional ratios require positive conditioning price and compatible normalizations. Treat maximum-entropy/KL estimates as models, not model-free price bounds.
- Distinguish no-arbitrage model bounds from executable trades: account for bid/ask, fees, liquidity, settlement definitions, position limits and feasible shorting.
- Never describe synthetic examples as observed market opportunities.

## First Codex delivery
1. Bootstrap existing project files at the **repository root**, not in a nested duplicate directory. Preserve path structure and avoid generated build junk.
2. Create branch `research/ot-lean-foundations` from `main` (if it is already present, choose a nonconflicting branch name), leaving `main` untouched.
3. Inspect the existing Lean proof draft and `research/lean_verification_scope.md`; compile it using the pinned toolchain, fix errors, and provide the compiler log / version evidence.
4. Check and extend `.github/workflows/lean.yml` to actually run `lake build` and forbid explicit proof gaps and new project axioms.
5. Verify Python tests independently and check that synthetic numerical claims in the manuscript and README agree with code and scenario data.
6. Add a finite *exact rational* certification for the three-event static bounds [0.15,0.22], then aim to formalize it in Lean (explicit feasible endpoint couplings and all-state hedges).
7. Record each result in `research/claim_registry.md`, and make uncertainty and open obligations visible in the manuscript.
8. Commit on the research branch, open a **draft pull request** targeting `main`, and include test evidence plus open questions. Do **not** merge or publish a paper without human review.

## Human review gates
Never merge a PR, make a research-publication claim, scrape restricted sources, spend money, access private market data, or trade. Repository is public: keep all files, secrets and credentials appropriately public-safe. Ask for approval before any outbound or consequential action beyond ordinary development commits and the requested draft PR.
