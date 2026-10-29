# Dynamic coherence of event-token prices: next mathematical target

## The first extension after static and martingale OT

A collection of payoff-consistent *time-zero* quotes does not determine
how conditional claims should be repriced when information arrives.

Suppose all claims are quoted in one unit of collateral and terminal payoffs
are measurable on common `Omega`. With a filtration `F_0 subset F_1 ... F_T`
and common equivalent pricing measure `Q`, a continuously tradeable claim
should satisfy a discounted martingale property

    P_t(H) = E_Q[H | F_t],  for t <= settlement.

This is stronger than the time-zero constraint `P_0(H)=E_Q[H]`. It is a
conditional restriction on each information node, not ordinary Kantorovich
coupling of terminal marginal laws. It applies only under justified
frictionless dynamic-trading assumptions. Nontradable or suspended tokens
may not support the same conclusion.

## A transparent two-node calculation

With hypothetical time-zero quote inputs
`Q(A)=0.60`, `Q(B)=0.55`, `Q(A and B)=0.40`, the conditional prices implied by
this time-zero **model** are

    Q(B | A)     = 0.40 / 0.60 = 2/3,
    Q(B | not A) = (0.55 - 0.40) / 0.40 = 3/8.

The law of total expectation checks the number:

    (0.60)(2/3) + (0.40)(3/8) = 0.55.

If a live `B` contract is quoted after `A` resolves, observed information may
include *more than* the fact of `A`, and the relevant conditional law may
legitimately update further. One must define `F_t` from the actual
information feed before calling two prices dynamically inconsistent.

## A finite-tree LP research protocol

1. Construct a node tree based on timestamped observed information (not
   solely on eventual final resolutions).
2. Give each node a conditional likelihood or state-price mass under the
   same collateral numeraire; enforce conservation of probability mass.
3. Match observed claim quotes using node-specific constraints, allowing
   quote intervals and distinct collateral/cost treatment.
4. Solve a feasibility LP. If infeasible, compute minimum quote slack and
   then examine whether the apparent gap is executable with dynamic trades.
5. Compare to an *adapted optimal transport* formulation only after
   specifying source and target stochastic processes and nonanticipative
   coupling requirements. A simple sequence of events does not, by itself,
   make the joint law a causal transport model.

## Research questions with testable outcomes

- Can observed time-series token prices be embedded in a common conditional
  state-price system after synchronization and appropriate fee treatment?
- Are violations concentrated at information arrivals, market suspensions,
  early-resolution events or hidden conditional dependencies?
- Do option-surface marginals improve a model's bounds on the *conditional*
  path event once a hedgeable underlying is explicitly identified?
- Can executable dynamic hedges be implemented without assuming impossible
  round-trip fills after information jumps?

This file is a hypothesis map, not an executed study or new theorem.
