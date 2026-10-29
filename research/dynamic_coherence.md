# Dynamic coherence of event-token prices: next mathematical target

## The first extension after static and martingale OT

A collection of payoff-consistent *time-zero* quotes does not determine
how conditional claims should be repriced when information arrives.

Suppose all claims are quoted in one unit of collateral and terminal payoffs
are measurable on common `Omega`. With a filtration `F_0 subset F_1 ... F_T`
and a common admissible pricing law `Q`, the discounted value process for a
dynamically tradable claim is modeled by

    P_t(H) = E_Q[H | F_t],  for t <= settlement.

This is stronger than the time-zero constraint `P_0(H)=E_Q[H]`. It is a
conditional restriction on each information node, not ordinary Kantorovich
coupling of terminal marginal laws. It applies only under justified
frictionless dynamic-trading assumptions. Nontradable or suspended tokens
may not support the same conclusion.

## Nonnegative admissible laws versus equivalent pricing measures

The finite LPs and the compiled Lean `Feasible` predicates impose **q_i >= 0**,
not strict positivity. No physical/reference measure `P` is part of those
definitions. These are closed subsets of the finite probability simplex, hence
compact; a nonempty feasible set attains its linear payoff extrema. In a finite market model with a
specified full-support reference law `P`, equivalence `Q ~ P` instead requires
**q_i > 0 on every atom**. An equivalent martingale measure may be required by
an appropriate no-arbitrage theorem under additional trading assumptions;
mere existence of a nonnegative calibrated law is not that assertion.

For the six-quote Boolean model, let `x = Q(ABC)`. The seven equality constraints
give the following entire one-parameter family, in order 000 through 111:

    q(x) = (8/25-x, x-7/100, x-3/20, 3/10-x,
            x-1/50, 11/50-x, 2/5-x, x).

Nonnegativity is equivalent to `3/20 <= x <= 11/50`. The two stored endpoint
witnesses have `q^-(010)=0` and `q^+(101)=0`. Strict positivity requires
`x > 3/20` from atom 010 and `x < 11/50` from atom 101; all other coordinates
are then positive. Consequently the attainable values under equivalence to
full-support `P` are **(3/20,11/50)**. The lower and upper numbers are an
**infimum and supremum**, not a minimum and maximum in that class. This also
makes the fixed-denominator conditional interval **(3/8,11/20)** in that class.

Explicitly, for `0 < t < 1`,

    q_t = (1-t) q^- + t q^+,
    E_{q_t}[1_ABC] = 3/20 + (7/100)t.

Every q_t has full support, retains all six exact quotes, and approaches the
two endpoints as t tends to 0 or 1. At t=1/2 one obtains
`q_*=(27,23,7,23,33,7,43,37)/200`, whose eight entries are strictly positive.
This is an explicit density argument, not an assumption that zero atoms are
allowed by equivalence. `tests/test_equivalent_laws.py` checks the rational
identities and representative mixtures; the continuum argument above is
ordinary algebra and is **not a new Lean theorem**.

The two-date MOT example has the same distinction. The midpoint of its stated
endpoint witnesses is `(5,3,3,1,1,3,3,5)/24`, which is strictly positive and
satisfies both history gain equations. With `u,v,w,z` denoting the S1=110
joint row, full support gives `u,v > 0` and `w,z < 1/4`. Thus
`u+v < 2u+v = z < 1/4`, and
`3(u+v) = 1/2-w+v > 1/4`. The attainable target values are strictly between
1/12 and 1/4, with those endpoints approached by feasible positive mixtures.

More generally, if a convex finite admissible set has a feasible full-support
law q_*, mixing any feasible boundary law with q_* preserves all linear
constraints and approximates the boundary law by full-support laws. Only with
that existence hypothesis do closure extrema give the same infimum/supremum
over equivalent laws. We do not assume this for every new OT/MOT instance.
None of this changes the valid q_i >= 0 numerical examples or Lean proofs.

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

The final research questions are hypotheses, not an executed empirical study.
The finite support/equivalence calculation above is an established algebraic
deduction awaiting Lean formalization, separate from those hypotheses.
