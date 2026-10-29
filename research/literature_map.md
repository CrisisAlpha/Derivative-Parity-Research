# Evidence and novelty map (checked October 29, 2026)

| Source | Original contribution | Relevance | What we must NOT claim |
|---|---|---|---|
| Beiglbock, Henry-Labordere & Penkner (2013), [DOI](https://doi.org/10.1007/s00780-013-0205-8) | No-duality-gap robust bounds using martingale transport | Model-independent exotic option pricing and semi-static hedging | MOT bounds or dual superhedges are new |
| Guo & Loeper (2021), [DOI](https://doi.org/10.1214/20-AAP1617) | Path-dependent semimartingale transport and calibration | Continuous-path constrained pricing | OT on path functionals is new |
| Engstrom, Kallblad & Karlsson (2025), [DOI](https://doi.org/10.1137/24M1670573) | Efficient structured multimarginal MOT and entropic methods | Scaling across dates | Entropic regularization itself is new |
| Krsek & Pammer (2025), [DOI](https://doi.org/10.1007/s00245-025-10240-y) | Adapted/causal transport duality, finance applications | Information-respecting couplings | Causal transport itself is new |
| Rana et al. (2026), [arXiv](https://arxiv.org/abs/2603.22596) | Coherent joint parlay AMM, pairwise exponential-family belief state, loss dynamics | Comparison against parametric joint model | Pairwise coherent pricing is new |
| Shi & Zhai (2026), [arXiv](https://arxiv.org/abs/2610.23517) | Logical-market consistency and combinatorial arbitrage with order book replay | Major near-neighbor; must benchmark | Detecting logical arbitrage across related event contracts is new |
| Gnosis Conditional Tokens, [docs](https://conditional-tokens.readthedocs.io/en/latest/developer-guide.html) | Multi-condition token position semantics | Settlement claim definitions | Intersection tokens equal conditional-probability contracts |

## Candidate contribution (hypothesis, NOT established)

A settlement-aligned, *path-conditioned* comparison of prediction-event tokens,
option-implied marginal distributions and executable dual hedges could quantify
how information arrivals reduce no-arbitrage price intervals, and when market
quotes deviate from those intervals after costs.

Novelty depends on identifying an empirical effect or a theorem not implied
by the papers above. In particular the 2026 combinatorial arbitrage paper is
very close on static payoff-consistency detection. Focus on time evolution,
conditional information, hedgeability, and interval calibration; do not
repackage LP feasibility as a novel pricing engine.

## Theoretical distinctions

- **Ordinary OT:** optimizes over couplings of observed marginals.
- **Martingale OT:** additionally imposes a conditional mean restriction for a
  dynamically tradable (discounted) asset.
- **Adapted/causal OT:** compares process laws with nonanticipating couplings.
  A path distribution merely being chronological does **not** impose a causal
  transport condition. We must define source and destination processes and the
  relevant filtration before claiming an adapted transport theorem.
- **Entropic regularization:** chooses a reference-dependent coupling; price
  interval endpoints remain model-free only when no prior or penalty is added.

## Missing evidence before any academic novelty claim

1. A systematic review of pathwise robust pricing in event/forecast markets.
2. Real synchronized contract-level quotes and verified settlement equivalence.
3. Out-of-sample tests that explicitly compare against Shi--Zhai and Rana et al.
4. Computational scaling and tolerance sensitivity as date count increases.
5. A complete economic model of conditional-token settlement and financing.
