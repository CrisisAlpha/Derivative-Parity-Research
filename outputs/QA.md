# Reproduction and verification record - 2026-10-29 (Asia/Hong_Kong)

## Scientific referee follow-up

The findings P0-A/P0-B/P0-C/P1 in the user's task were checked against the actual
source and addressed on `research/ot-lean-foundations`. After initially being
unavailable, the complete `PR1_SCIENTIFIC_REVIEW.md` was supplied at the workspace
root and read against the named sources. The original is preserved in
`research/reviews/PR1_SCIENTIFIC_REVIEW.md`; the finding-by-finding response and
provenance are in `research/reviews/PR1_RESPONSE.md`. This supersedes the earlier
missing-attachment limitation. The review targets `3756fa88`, not the revised
head; a fresh scientific review is still required. Its independent BigInt audit
is the referee's reported evidence, distinct from our Python and Lean runs.

| Check | Actual local outcome |
| --- | --- |
| `python -m pytest -q` | **58 passed**, including alternate Lean assumption syntax, omitted audits, equivalent-law mixtures, conditional-event preconditions and distinct histories |
| `python -m parity_ot.certificates` | **PASS**, all 16 endpoints; original finite q>=0 examples unchanged |
| `python scripts/check_lean.py` | **PASS**: source policy, 5 promoted claims/21 theorem inventory, actual pinned `lake build`, 21 axiom checks |
| `python scripts/build_manuscript.py --tectonic <Tectonic-0.15.0 executable>` | **PASS**, current source produces six nonempty pages and one embedded comparison figure; no unresolved references/citations or missing glyphs |
| Visual PDF inspection | All six rendered pages inspected; no clipping or missing figure/text detected |
| Canonical default branch | Deliberately set to `main` using repository metadata; main SHA remains `d38727a701d22ebaed84a6ba6965933e8c921ad3` |

The current PDF and its logs are generated review artifacts under
`outputs/manuscript-build/` (ignored by Git); CI retains the same artifact with
the exact source commit, input/PDF SHA256 hashes and verification report.
The original PDF was moved unchanged to `manuscript/historical/handoff-v0.2.pdf`.
The pinned compiler fetched its TeX dependencies from bundle v33, resolving to
`https://data1b.fullyjustified.net/tlextras-2022.0r0.tar`. No manuscript release or
publication was performed. Active citations use the inline bibliography;
`references.bib` remains a migration resource. Resolving citations in a build is
not a fresh bibliographic or novelty audit of the cited literature.

Referee-fix failures and repairs (not hidden):

- First expanded test run: **1 failed, 57 passed**. A new near-price-history test
  incorrectly required bitwise equality of `2-1.000001` with the decimal literal
  `0.999999`. The test now uses absolute tolerance 1e-15 for the floating increment
  and still checks cross-history zero entries exactly. No existing numerical
  example, certificate or formal proof was weakened.
- First current-source LaTeX compilation exited 0 and passed PDF checks, but
  reported missing Windows Fontconfig configuration, two overfull boxes and an
  underfull bibliography line. Its transcript is retained in
  `outputs/validation/referee/latex-first-build.txt`. Added a local Fontconfig
  configuration for the portable Windows compiler, broke long displayed math,
  made source paths breakable, and used a ragged-right bibliography. Rebuild
  exited 0 without those diagnostics; no citations or figures were missing.

The Lean theorem sources and pinned toolchain/mathlib revisions were not relaxed.
All 21 audited results retain the original foundation summary: three Boolean
lemmas use no axioms, the other 18 use only `propext`, `Classical.choice`,
`Quot.sound`. `formal_claims.json` now mechanically links the promoted registry
rows to every explicit audit. The finite equivalence/strict-positivity arguments
are analytic deductions, not new Lean theorems; the conditional identity is
established mathematics awaiting formalization, not a conjecture.

The final PR comment records the exact head SHA and CI/artifact links after
GitHub completes them. PR #1 remains draft; no main commit, merge, live market
fetch, trade, or publication is authorized by this follow-up.

## Initial-PR local outcomes (historical)

| Command | Exit | Outcome |
| --- | --- | --- |
| `python -m pip install -e '.[test,research]'` | 0 | Installed in a fresh `.venv`; added the missing pandas research dependency required by notebook 01 |
| `python -m pytest tests/test_bounds.py -q` | 0 | Original **9 passed** independently reproduced before extensions |
| `python -m pytest -q` | 0 | Final **28 passed**, including exact endpoint, model-correspondence, corrupted-certificate and CI-policy tests |
| `python -m parity_ot.examples` | 0 | Every reported manuscript OT/MOT interval reproduced |
| `python scripts/generate_certificates.py` | 0 | 8 candidate primal/dual pairs rationally reconstructed and then exactly validated |
| `python -m parity_ot.certificates` | 0 | All 16 endpoints exactly checked; 8 or 48 states per instance; every quote and full-history gain equation |
| `python scripts/render_certificates.py` | 0 | Explicit primal and dual tables written to `research/rational_certificates.md` |
| `python scripts/render_results.py` | 0 | Summary JSON and figure regenerated |
| `python scripts/build_notebook.py` | 0 | MOT notebook regenerated and executed |
| `python scripts/execute_notebooks.py` | 0 | Both notebooks executed, including notebook 01 maximum-entropy numerical assertions |
| `lake build` via `python scripts/check_lean.py` | 0 | All three project proof modules compile; warnings treated as errors |
| `lake env lean -DwarningAsError=true AxiomAudit.lean` via the same script | 0 | 21 declarations audited, accepted foundations only |
| LaTeX build | not run | Neither `latexmk` nor `pdflatex` is installed. Imported `manuscript/main.pdf` is a historical handoff artifact, not a build of current source |

Raw final command outputs are in `outputs/validation/`. The notebook log includes
Windows Jupyter event-loop and local-kernel transport warnings; both executions
completed with exit 0. These are not Lean warnings or proof exceptions.

## Environment and pins

Windows x86_64, Python 3.12.10, NumPy 2.5.4, SciPy 1.18.1, pytest 9.2.0,
pandas 3.1.0. Full installed Python version snapshot: `outputs/python-environment.txt`.
The snapshot is an audit record, not a cross-platform dependency lockfile.

Lean: `Lean (version 4.20.0, x86_64-w64-windows-gnu, commit 77cfc4d1a4f6, Release)`.
Mathlib: release `v4.20.0`, commit `c211948581bde9846a99e32d97a03f0d5307c31e`.
`lake-manifest.json` pins every transitive revision from that release's manifest.
The source checkout of mathlib is unmodified.

## Setup and failed attempts, followed by fixes

- No Lean installation was initially on PATH. Installed elan and the exact pinned
  Lean 4.20.0 toolchain; no package-access permission remains missing.
- A full mathlib clone stalled. A shallow checkout of the pinned tag succeeded.
  `lake update` then attempted to fetch all tags; it was interrupted. The root
  manifest was constructed from the pinned mathlib release manifest and its exact
  commit, and every dependency was fetched at its recorded SHA. No version changed.
- Cache invocation with repository-relative `Mathlib/...lean` paths failed; using
  module names succeeded. ProofWidgets initially lacked its release tag; fetching
  `v0.0.60` and retrying `lake -v build proofwidgets:release` succeeded.
- Final cache commands used module names: `lake exe cache get Mathlib.Data.Real.Basic
  Mathlib.Algebra.BigOperators.Fin Mathlib.Tactic.FinCases Mathlib.Tactic.NormNum`
  and `lake exe cache get Mathlib.Algebra.BigOperators.Field
  Mathlib.Algebra.Order.BigOperators.Group.Finset`.
- The first actual project `lake build` failed on missing finite-sum imports and
  executable-code generation for real division. Added the appropriate pinned
  mathlib imports and marked classical real definitions `noncomputable`; corrected
  the sum/division rewrite direction. The subsequent actual build passed, followed
  by a final logged successful build/audit. No failed checks were suppressed.

## Formal results and trust boundary

`ParityOT.Static.sharp_bounds` proves the exact [3/20,11/50] bounds and attaining
rational laws for the six-quote Boolean model over **all real feasible weights**.
`ParityOT.TwoDate.sharp_bounds` proves [1/12,1/4] and attainment for the specified
MOT model, with gain equations at both first-date histories. Supporting feasibility,
attainment, pathwise-hedge and cost theorems are all audited. The three Boolean
lemmas depend on no axioms; the other 18 audited theorems depend only on
`propext`, `Classical.choice`, `Quot.sound`. No new project axioms or proof gaps.

The exact Python certificates cover all eight model variants, with all ten
full-history gains for each three-date MOT endpoint. Three-date Lean proofs,
ordinary-OT/extra-quote Lean proofs, a formal Python-to-Lean correspondence,
conditional ratios and general strong duality remain open. Numerical max-entropy
fits are model selections, not formally certified fair prices. No market data,
market credentials, trades, or executable arbitrage claims are involved.

## Bootstrap and GitHub status

Source archive: `Derivative-Parity-OT-Codex-Handoff-v0.2.zip`, SHA256
`f3fbd8f1cc1954c2e1abcd6b601b1d5582fa8a29057523bd4800b958074e6888`.
Imported its `Derivative-Parity-Research/` **contents** into the target checkout
root. The original unrelated `k25-research` repository was not edited.
`MANIFEST.sha256` is the original archive manifest and applies to the bootstrap
source snapshot, not subsequent research commits.

GitHub initially confirmed a public, completely empty repository: no commits or
branches, including no `main`. The research history has an empty root commit
`d38727a` followed by the source import and implementation. The user explicitly
approved creating the missing `main` at empty commit
`d38727a701d22ebaed84a6ba6965933e8c921ad3` solely to provide the PR base.
GitHub confirms that exact ref; it contains zero files. All research source and
implementation changes remain on `research/ot-lean-foundations`.
GitHub confirmed both push-triggered CI runs **PASS** for implementation commit
`32077c46880e81bd7f0492a7a53e476677681ab5`:

- [Python tests](https://github.com/CrisisAlpha/Derivative-Parity-Research/actions/runs/40860564196)
- [Lean build and axiom audit](https://github.com/CrisisAlpha/Derivative-Parity-Research/actions/runs/40860564091)

The Lean job log explicitly shows `Built StaticCertificate`, `Built TwoDateCertificate`,
`Built LeanNotes`, `Build completed successfully`, and `Axiom allowlist PASS (21 declarations)`.
These are remote Linux results in addition to the local Windows results above.
Subsequent evidence/status commits update documentation, not the verified proof/code files.
GitHub confirmed [draft PR #1](https://github.com/CrisisAlpha/Derivative-Parity-Research/pull/1)
is OPEN and DRAFT, targeting `main` from `research/ot-lean-foundations`. It includes
the theorem/CI checklist and remaining formal obligations. It has not been merged.
The GitHub connector returned integration-permission errors for branch/PR creation;
the existing authenticated Git and GitHub CLI connections completed the approved actions.
