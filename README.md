# Derivative Parity Research: Conditional and Path-Dependent Event Contracts

**Status: public research repository, [draft PR #1](https://github.com/CrisisAlpha/Derivative-Parity-Research/pull/1) (October 29, 2026).**
The source tree is imported at the repository root from the v0.2 handoff.
All examples are synthetic. See the [claim register](research/claim_registry.md)
for the distinction between compiled Lean theorems, exact rational certificates,
floating-point experiments and open research hypotheses.

## Question

How much can we infer about conditional or history-dependent event payouts from
prices of overlapping traded contracts, without specifying an arbitrary joint
law? When a claim depends on a hedgeable asset, how much more do the asset's
martingale conditions restrict these prices?

## Reproducible findings (all synthetic)

| Claim | Ordinary coupling | Full martingale coupling |
|---|---|---|
| Binary A and B and C, six quotes | [0.15, 0.22] | Not applicable |
| Rally S1=110 then S2<=90 | [0, 0.50] | [0.08333, 0.25] |
| Same two-date claim + hypothetical joint quote | (computed in code) | [0.10, 0.20] |
| Rally -> decline -> rebound, three monitoring dates | [0, 0.25] | [0, 0.06250] |
| Touched S>=130 at three monitoring dates | [0.25, 0.50] | [0.275, 0.375] |

All numbers are conditional on artificial finite supports and explicitly stated
marginals. They are not observed market prices, empirical signals, or proofs of
arbitrage in an exchange.

## Run

```bash
python -m pip install -e '.[test,research]'
python -m pytest -q
python -m parity_ot.examples
python -m parity_ot.certificates
python scripts/render_results.py
python scripts/execute_notebooks.py
python scripts/check_lean.py
python -m pip install -e '.[manuscript]'
python scripts/build_manuscript.py  # Tectonic 0.15.0 must be on PATH
```

The package assumes a Python environment with NumPy and SciPy; rendering also
requires Matplotlib. If installation is unavailable, setting
`PYTHONPATH=src` allows execution using already-installed packages.

## Contents

- `src/parity_ot/transport.py`: finite-state primal bounds, quote intervals,
  full-history martingale constraints, conditional-ratio LPs and exact-quote
  dual certificates.
- `src/parity_ot/examples.py`: transparent scenario definitions and outputs.
- `tests/`: exact analytic regressions, full-filtration equality checks,
  pointwise dual hedge verification, infeasibility and bid/ask monotonicity.
- `notebooks/01_correlated_event_ot.ipynb`: prior synthetic event-coupling
  notebook (included for continuity).
- `notebooks/02_path_martingale_ot.ipynb`: executable MOT worked examples.
- `manuscript/main.tex` + `references.bib`: working note with propositions and
  proofs. The active bibliography is inline; `references.bib` is retained for
  migration. The pinned manuscript build job compiles current source and checks
  the resulting PDF, figure, references and input hashes.
- `research/`: hypothesis map, novelty guardrails, market semantics,
  and a dynamic-coherence research extension.
- `outputs/`: generated numerical summaries, charts and test audit.

## Scientific and execution safeguards

1. Binary/event claims do **not** inherit martingale constraints merely
   because they occur in chronological order. Only use MOT for a
   dynamically tradable, appropriately discounted underlying.
2. A quoted intersection token `A & B` is not a normalized claim paying
   `P(B|A)`; the latter is a ratio and requires `P(A)>0`.
3. The static LP is a *consistency test* under a common pricing measure,
   numeraire and settlement convention; market completeness is not required.
   Inconsistent settlement rules or different discounting may explain apparent gaps.
4. Quote bands, latency, displayed depth, slippage, fee schedules, shorting
   restrictions and settlement delays must be modeled before using a dual
   hedge as an executable trade.
5. Maximum-entropy or KL transport selects a **model** within a sharp
   interval, not a model-free fair price.
6. This package does not access APIs, contact people, or place orders.

## Literature

Primary links and assessment of novelty in `research/literature_map.md`. The
closest prior work includes Beiglbock et al. (2013), Guo--Loeper (2021),
Engstrom et al. (2025), Krsek--Pammer (2025), Rana et al. (2026), and
Shi--Zhai (2026). Nothing in this pilot claims to supersede those results.

## GitHub / Overleaf / Codex

The canonical target is the **public** repository `CrisisAlpha/Derivative-Parity-Research`.
The canonical default branch is deliberately set to **`main`**. This repository
setting does not move its commit: `main` remains the approved empty base
`d38727a701d22ebaed84a6ba6965933e8c921ad3` until a separately authorized merge.
All current research is reviewed on `research/ot-lean-foundations` in draft PR #1.
The earlier automatic default of the first-pushed research branch was a bootstrap
side effect, not the intended permanent policy. This PR does not merge anything.
Use the first-time bootstrap instructions in `CODEX_HANDOFF.md` and paste
`CODEX_TASK_PROMPT.txt` into Codex. Repo root `AGENTS.md` specifies required
formal-verification and research-quality rules. GitHub PRs and CI runs should
be treated as the durable record, not ChatGPT chat state. Overleaf may import
`manuscript/` (or later sync through Git if the Overleaf plan supports it).

*No open-source license is inferred or granted by this working package.*

## Lean verification status

**Local verification: 58 Python tests pass; Lean 4.20.0 `lake build` passes;
all 21 theorem axiom audits pass.** The static 15%-22% and two-date MOT
1/12-1/4 bounds have compiled Lean certificates over all real feasible laws.
Those laws allow zero masses. Equivalence to a full-support reference measure
requires positive masses and changes endpoint attainment into infimum/supremum
for these two examples; see [the explicit demonstration](research/dynamic_coherence.md).

See [verification scope](research/lean_verification_scope.md) and
[run evidence](outputs/QA.md) for actual build results and accepted foundations.
`StaticCertificate.lean` states the sharp 15%-22% finite bounds over real laws;
`TwoDateCertificate.lean` states the two-date finite MOT bounds. Three-date
examples have exact rational certificates, with Lean formalization still open.
Neither finite certification nor a numerical OT interval implies a traded arbitrage.

Exact witnesses are in [readable tables](research/rational_certificates.md) and
`data/synthetic/rational_certificates.json`. `python -m parity_ot.certificates`
checks the committed witnesses without invoking an optimizer. Candidate regeneration
with `python scripts/generate_certificates.py` invokes SciPy and then requires every
exact check to pass. The historical `MANIFEST.sha256` describes the imported handoff,
not subsequent commits. The supplied PDF is preserved as
`manuscript/historical/handoff-v0.2.pdf`. Current builds go to
`outputs/manuscript-build/` and the manuscript CI artifact, with compiler logs,
input/PDF SHA256 hashes and extracted-text checks. These are draft review
artifacts; no manuscript release or publication is performed.
