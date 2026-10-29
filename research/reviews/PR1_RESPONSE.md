# Response to the complete PR #1 scientific review

The supplied [review](PR1_SCIENTIFIC_REVIEW.md), dated 2026-10-29, concerns
`3756fa88b551e472a4c9155d9da9c55b5fd9a417`. It was received at the workspace
root after the first referee-fix update. Its unmodified file SHA256 is
`6ddd5183283dd2effcdd4380f6a97ca0073af429b8e22d4fca96bd051aed59c6`.
This receipt supersedes the missing-file limitation in the earlier PR update.
The referee reports an independent BigInt certificate check but explicitly did
not run Lean; those statements are preserved as the referee's evidence, not
represented as a second local Lean run.

All named sources were inspected. The implementation fixes are in `afe7067`
and manuscript exact-head provenance in `167104d`; this follow-up records the
complete review and adds its direct hedge-slack explanation. Neither the Lean
theorem sources nor the valid numerical instances were relaxed.

| Finding | Response and source evidence | Status |
| --- | --- | --- |
| P0-A: nonnegative versus equivalent laws | `research/dynamic_coherence.md` defines the support distinction, gives the entire static family, strict hedge slack and positive mixtures, and treats two-date MOT. `manuscript/main.tex`, the scope and claim registry distinguish attained extrema from unattained infimum/supremum. `tests/test_equivalent_laws.py` checks rational witnesses. | Addressed; additional equivalence deductions are not Lean formalizations. |
| P0-B: assumption syntax and complete audits | `scripts/check_lean.py` rejects alternate assumption forms; `tests/test_lean_policy.py` covers these and audit omissions. `research/formal_claims.json` links every promoted claim to the explicit `AxiomAudit.lean` inventory. Kernel-reported dependencies remain the final allowlist check after the actual build. | Addressed; 5 claims / 21 declarations audited. |
| P0-C: current manuscript | `.github/workflows/manuscript.yml` runs pinned Tectonic 0.15.0 on the exact PR head. `scripts/build_manuscript.py` checks the generated PDF, figure, references and source hashes, retaining logs. The old PDF is explicitly historical at `manuscript/historical/handoff-v0.2.pdf`. | Addressed; six-page current artifact verified. |
| P1.1: canonical default | Repository metadata deliberately selects `main`; README explains that it remains the empty PR base at `d38727a701d22ebaed84a6ba6965933e8c921ad3`. | Addressed; no main commit or merge. |
| P1.2: conditional identity | C-01 is `ESTABLISHED_NOT_FORMALIZED`, with positive denominator and separate settlement interpretation. | Addressed; Lean identity proof remains open. |
| P1.3: conditional API | `conditional_ratio_interval` requires 0/1 event indicators, numerator subset of conditioning, and a finite positive denominator cutoff. Tests reject non-events, non-subsets and invalid cutoffs. | Addressed; generic payoff ratios are outside this API. |
| P1.4: filtration | `martingale_features`, manuscript and scope specify the natural filtration of monitored price histories. Exact prefix matching keeps nearby nodes distinct. Additional market information needs separately specified atoms/equalities. | Addressed; no arbitrary-filtration theorem claimed. |
| P1.5: next Lean scope | M-02/M-03 remain `RATIONAL_CERTIFIED`. Prioritize 48-state rebound/barrier certificates, then the Python-to-Lean model bridge, with compilation and axiom audits before promotion. | Open future work, explicitly retained. |

The full local checks recorded in `outputs/QA.md` and
`outputs/validation/referee/` passed: 58 Python tests, all 16 exact certificate
endpoints, pinned `lake build`, all 21 axiom audits, and the current manuscript
build. Three Boolean lemmas use no axioms; the other 18 depend only on
`propext`, `Classical.choice`, `Quot.sound`. Earlier failures and their repairs
remain recorded. The final PR update binds the new head to separate Python,
Lean and manuscript CI results and its generated artifact.

Request a new scientific review of that updated head. The implementation's
response is not referee acceptance. Keep PR #1 draft and unmerged. General
duality, conditional-ratio/quote-band formalization, arbitrary filtrations and
continuous time also remain open. No publication or executable-arbitrage claim
is made.
