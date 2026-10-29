# Derivative Parity Research: Conditional and Path-Dependent Event Contracts

**Status: research sandbox, v0.1 (October 29, 2026).** This directory is a
self-contained GitHub-ready research module intended to join the larger
"Mathematical Parity Between Perpetual Contracts, Binary Event Predictions,
and Option Surfaces" project. It does **not** replace previously developed
workspace materials and is undergoing GitHub publication and formal verification.

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
python scripts/render_results.py
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
- `manuscript/main.tex` + `references.bib`: Overleaf-ready working note,
  with propositions and proofs. Compile with `latexmk -pdf main.tex` from
  inside `manuscript/`.
- `research/`: hypothesis map, novelty guardrails, market semantics,
  and a dynamic-coherence research extension.
- `outputs/`: generated numerical summaries, charts and test audit.

## Scientific and execution safeguards

1. Binary/event claims do **not** inherit martingale constraints merely
   because they occur in chronological order. Only use MOT for a
   dynamically tradable, appropriately discounted underlying.
2. A quoted intersection token `A & B` is not a normalized claim paying
   `P(B|A)`; the latter is a ratio and requires `P(A)>0`.
3. The static LP is a common-payoff/no-arbitrage *consistency test* under
   market completeness assumptions; inconsistent settlement rules or
   different discounting may explain apparent parity gaps.
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
Use the first-time bootstrap instructions in `CODEX_HANDOFF.md` and paste
`CODEX_TASK_PROMPT.txt` into Codex. Repo root `AGENTS.md` specifies required
formal-verification and research-quality rules. GitHub PRs and CI runs should
be treated as the durable record, not ChatGPT chat state. Overleaf may import
`manuscript/` (or later sync through Git if the Overleaf plan supports it).

*No open-source license is inferred or granted by this working package.*

## Lean verification status

`LeanNotes.lean` is a proposed Lean 4 finite-state formalization with a dedicated CI workflow. **It has not yet been compiled in this environment**; therefore no claims of machine-checked proof status are made. See `research/lean_verification_scope.md`. Formal numerical optimality and martingale results remain open verification tasks.
