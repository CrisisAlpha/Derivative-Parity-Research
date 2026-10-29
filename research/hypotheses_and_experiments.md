# Hypotheses, preregistration candidates, and staged experiments

Project: Mathematical Parity Between Perpetual Contracts, Binary Event
Predictions, and Option Surfaces / OT extension.

## H1: Joint information reduces identification width

When pairwise or related joint contracts are added to a feasible set defined
by singleton event prices, the robust interval cannot widen. Test magnitude
in real venue-level cross-sections and report selection effects: venues list
joints non-randomly. Toy check: ABC [0, .45] -> [.15, .30] -> [.15, .22].

## H2: Asset-price martingale restrictions add measurable information

For claims on hedgeable underlying prices, using maturity marginals recovered
from option markets and valid martingale restrictions yields equal or tighter
bounds relative to ordinary multi-marginal OT. Toy examples are constructed
under explicitly zero-rate, no-payout conditions. On actual perp/spot/option
data, normalize forwards, rates, collateral and funding before inferring Q.

## H3: More informative models should be judged by holdout coverage

Entropy/KL, Gaussian or vine copula and pairwise Ising pricing may each give a
point estimate within the no-arbitrage range. Evaluate held-out exact
settlements with log loss/Brier score under a *physical* forecast model, and
market-valuations with quote errors under the *pricing* measure, treating the
two as different targets. Do not claim pricing-measure point estimates are
calibrated forecasts without risk-premium adjustments.

## H4: Executable violations are smaller than naive midpoint deviations

Calculate upper/lower statewise hedge portfolios and compare to actual
bid/ask/depth and fees. The forecast that apparent violations are rare after
execution costs is a hypothesis to be falsified, not a pre-judged result.
Include capital lockup and the availability of short positions.

## Experimental phases

**P0 / finished for v0.1:** Finite-support LP implementation, exact binary
and MOT examples, verified dual portfolios and reproducible tests.

**P1 / next:** Research adjudication of settlement-equivalent event pairs,
provider API terms, timestamped market snapshots, and coverage inventory.
No live data acquired in this package.

**P2:** Cross-sectional interval contraction using snapshot synchronized
market quotes, documented event-state atomization and fee-inclusive pricing.

**P3:** Option-derived marginals for underlyings; convex-order feasibility,
forward parity, spot/perp funding conventions; run MOT and cost-aware hedges.

**P4:** Dynamic-update protocol and information filtration; compare
path-conditioned forecasts against risk-neutral interval consistency across
time, with leakage-free training windows and out-of-sample holdouts.

## Primary outcomes

1. `width = upper - lower` by instrument and information set.
2. `contraction = width_base - width_augmented` on identical target contracts.
3. Fraction of incompatible quote systems and compatibility-restoration slack.
4. Fee-/spread-/size-adjusted executable dual violations, not raw midpoint gaps.
5. CPU time, number of atoms, number of constraints, duality gap and tolerances.

## QA and stop rules

- Do not impose martingale restrictions on a sport/election event path.
- Do not treat observed Yes price as empirical occurrence probability.
- Do not combine markets with inconsistent settlement wording and oracles.
- Do not mine results from unversioned or unsynchronized order books.
- Report infeasibility rather than silently fitting contradictory exact quotes.
- Avoid preemptively claiming a publishable novel theorem.
