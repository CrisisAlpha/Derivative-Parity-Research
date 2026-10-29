"""Finite-state optimal transport with optional full-filtration martingale constraints.

All prices are normalized present values of one-unit payoffs with discounting
suppressed. Every quoted payoff is represented on the *same* settlement states.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Mapping, Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.optimize import linprog


class InfeasibleModel(ValueError):
    """The supplied quotes and structural constraints admit no probability law."""


@dataclass
class PriceInterval:
    lower: float
    upper: float
    lower_coupling: NDArray[np.float64]
    upper_coupling: NDArray[np.float64]
    # For exact-quote problems, coefficients apply to certificate_features.
    lower_dual: NDArray[np.float64] | None
    upper_dual: NDArray[np.float64] | None
    certificate_features: NDArray[np.float64] | None
    certificate_prices: NDArray[np.float64] | None

    def verify(self, payoff: ArrayLike, atol: float = 1e-7) -> bool:
        """Check pointwise sub/super-replication and matching dual prices."""
        if self.certificate_features is None:
            return False
        c = np.asarray(payoff, dtype=float)
        f = self.certificate_features
        lo, hi = self.lower_dual, self.upper_dual
        p = self.certificate_prices
        if lo is None or hi is None or p is None:
            return False
        return bool(
            np.all(lo @ f <= c + atol)
            and np.all(hi @ f >= c - atol)
            and np.isclose(lo @ p, self.lower, atol=atol)
            and np.isclose(hi @ p, self.upper, atol=atol)
        )


def binary_paths(periods: int) -> NDArray[np.int64]:
    """All 0/1 histories of length `periods` in lexicographic order."""
    if periods < 1:
        raise ValueError("periods must be positive")
    return np.asarray(list(product((0, 1), repeat=periods)), dtype=int)


def cartesian_paths(levels: Sequence[Sequence[float]]) -> NDArray[np.float64]:
    """All finite-support price histories in lexicographic order."""
    if not levels or any(len(x) == 0 for x in levels):
        raise ValueError("Need nonempty support at every date")
    return np.asarray(list(product(*levels)), dtype=float)


def marginal_features(
    states: NDArray[np.float64],
    marginal_probabilities: Sequence[Mapping[float, float]],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Payoff rows 1{S_t=x} and marginal prices P(S_t=x)."""
    s = np.asarray(states, dtype=float)
    if s.ndim != 2 or s.shape[1] != len(marginal_probabilities):
        raise ValueError("states shape and number of marginal distributions disagree")
    rows, target = [], []
    for t, margin in enumerate(marginal_probabilities):
        if not np.isclose(sum(margin.values()), 1.0, atol=1e-9):
            raise ValueError(f"Probabilities for date {t} do not sum to 1")
        for level, prob in margin.items():
            rows.append(np.isclose(s[:, t], float(level)).astype(float))
            target.append(float(prob))
    return np.asarray(rows), np.asarray(target)


def martingale_features(states: NDArray[np.float64]) -> NDArray[np.float64]:
    """Full-filtration martingale equalities for each observed price history.

    On a path s=(s_1,...,s_T), rows are
      1{s_1=x_1,...,s_t=x_t} * (s_{t+1}-s_t)
    for every t < T and every support history (x_1,...,x_t).
    Each row must have zero expectation under a martingale law.

    This is NOT appropriate for unrelated political, sports or award outcomes.
    """
    s = np.asarray(states, dtype=float)
    if s.ndim != 2 or s.shape[1] < 2:
        raise ValueError("Need at least two monitoring dates")
    rows = []
    for t in range(s.shape[1] - 1):
        observed_prefixes = np.unique(s[:, : t + 1], axis=0)
        for prefix in observed_prefixes:
            mask = np.all(np.isclose(s[:, : t + 1], prefix), axis=1).astype(float)
            rows.append(mask * (s[:, t + 1] - s[:, t]))
    return np.asarray(rows)


def price_interval(
    payoff: ArrayLike,
    feature_payoffs: ArrayLike | None = None,
    quote_lows: ArrayLike | None = None,
    quote_highs: ArrayLike | None = None,
    extra_equalities: ArrayLike | None = None,
    extra_values: ArrayLike | None = None,
) -> PriceInterval:
    """Sharp LP bounds subject to quote ranges and linear structural constraints.

    feature_payoffs must have shape (n_contracts,n_states). The quote ranges
    may be exact. All structural equalities are *expectations*, not ex-post
    restrictions on paths. Coefficients for the two hedges are supplied only
    for fully exact-quote instances.
    """
    c = np.asarray(payoff, dtype=float).reshape(-1)
    n = len(c)
    if n == 0 or not np.isfinite(c).all():
        raise ValueError("Expected a finite nonempty payoff vector")
    if feature_payoffs is None:
        f = np.empty((0, n), dtype=float)
    else:
        f = np.atleast_2d(np.asarray(feature_payoffs, dtype=float))
    if f.shape[1] != n:
        raise ValueError("Each feature payoff must have one value per state")
    m = len(f)
    if m:
        if quote_lows is None or quote_highs is None:
            raise ValueError("Both lower and upper quote arrays are required")
        low = np.asarray(quote_lows, dtype=float).reshape(-1)
        high = np.asarray(quote_highs, dtype=float).reshape(-1)
        if low.shape != (m,) or high.shape != (m,):
            raise ValueError("Quote arrays must match feature rows")
        if np.any(low > high + 1e-12) or not np.isfinite(low).all() or not np.isfinite(high).all():
            raise ValueError("Quote intervals must be finite and ordered")
    else:
        low = high = np.empty((0,), dtype=float)

    if extra_equalities is not None:
        d = np.atleast_2d(np.asarray(extra_equalities, dtype=float))
        if d.shape[1] != n:
            raise ValueError("Structural equality row dimension mismatch")
        if extra_values is None:
            raise ValueError("extra_values required when extra_equalities supplied")
        v = np.asarray(extra_values, dtype=float).reshape(-1)
        if len(v) != len(d):
            raise ValueError("One RHS is required for each structural equality")
    else:
        d = np.empty((0, n), dtype=float)
        v = np.empty((0,), dtype=float)

    exact = np.isclose(low, high, atol=1e-12, rtol=0)
    eq = np.vstack((np.ones((1, n)), f[exact], d))
    rhs = np.r_[1.0, low[exact], v]
    band_f = f[~exact]
    if len(band_f):
        ub = np.vstack((band_f, -band_f))
        ub_rhs = np.r_[high[~exact], -low[~exact]]
    else:
        ub = ub_rhs = None

    args = dict(A_eq=eq, b_eq=rhs, A_ub=ub, b_ub=ub_rhs,
                bounds=(0, None), method="highs")
    lower_res = linprog(c, **args)
    upper_res = linprog(-c, **args)
    if not (lower_res.success and upper_res.success):
        raise InfeasibleModel(f"No feasible coupling: min={lower_res.message}; max={upper_res.message}")

    lower_price = float(lower_res.fun)
    upper_price = float(-upper_res.fun)
    if len(band_f) == 0:
        lo_dual = np.asarray(lower_res.eqlin.marginals)
        hi_dual = -np.asarray(upper_res.eqlin.marginals)
        cert_features, cert_prices = eq, rhs
    else:
        # Inequality-dual terms are essential for band-based hedge certificates.
        # Do not mislabel equality multipliers alone as a complete hedge.
        lo_dual = hi_dual = cert_features = cert_prices = None
    return PriceInterval(lower_price, upper_price, lower_res.x, upper_res.x,
                         lo_dual, hi_dual, cert_features, cert_prices)


@dataclass
class ConditionalInterval:
    """Bounds on E[H]/E[A] with an explicitly positive conditioning event."""
    lower: float
    upper: float
    lower_coupling: NDArray[np.float64]
    upper_coupling: NDArray[np.float64]


def conditional_ratio_interval(
    numerator_payoff: ArrayLike,
    conditioning_payoff: ArrayLike,
    feature_payoffs: ArrayLike,
    quote_lows: ArrayLike,
    quote_highs: ArrayLike,
    min_denominator: float = 1e-6,
) -> ConditionalInterval:
    """Sharp conditional ratio bounds via the Charnes-Cooper transformation.

    Given feasible probability vectors q, compute inf/sup E_q[numerator]/
    E_q[conditioning] with E_q[conditioning] >= min_denominator > 0.
    Use numerator=1_{A and B} and conditioning=1_A for Q(B|A).

    Variables y=q/E_q[A] and t=1/E_q[A] satisfy
      A^T y = 1, sum(y)=t, low_j t <= F_j^T y <= high_j t,
      y >= 0, 0 <= t <= 1/min_denominator.
    The objective E_q[numerator]/E_q[A] becomes numerator^T y.

    This is about a common pricing measure, not necessarily calibrated
    real-world forecasts, and presumes a fixed known settlement payoff.
    """
    num = np.asarray(numerator_payoff, dtype=float).reshape(-1)
    den = np.asarray(conditioning_payoff, dtype=float).reshape(-1)
    n = len(num)
    f = np.atleast_2d(np.asarray(feature_payoffs, dtype=float))
    lo = np.asarray(quote_lows, dtype=float).reshape(-1)
    hi = np.asarray(quote_highs, dtype=float).reshape(-1)
    if num.shape != den.shape or f.shape[1] != n or len(lo) != len(f) or len(hi) != len(f):
        raise ValueError("Payoff and quote dimensions do not align")
    if min_denominator <= 0 or min_denominator > 1:
        raise ValueError("min_denominator must be in (0,1]")
    if not (np.isfinite(num).all() and np.isfinite(den).all() and
            np.isfinite(f).all() and np.isfinite(lo).all() and np.isfinite(hi).all()):
        raise ValueError("All input numbers must be finite")
    if np.any(lo > hi):
        raise ValueError("Unordered quote interval")
    exact = np.isclose(lo, hi, atol=1e-12, rtol=0)
    # y variables followed by t variable.
    A_eq = [np.r_[den, 0.], np.r_[np.ones(n), -1.]]
    b_eq = [1.,0.]
    for j in np.flatnonzero(exact):
        A_eq.append(np.r_[f[j], -lo[j]])
        b_eq.append(0.)
    A_ub, b_ub = [], []
    for j in np.flatnonzero(~exact):
        A_ub += [np.r_[f[j], -hi[j]], np.r_[-f[j], lo[j]]]
        b_ub += [0., 0.]
    args = dict(A_eq=np.asarray(A_eq), b_eq=np.asarray(b_eq),
                A_ub=np.asarray(A_ub) if A_ub else None,
                b_ub=np.asarray(b_ub) if A_ub else None,
                bounds=[(0,None)]*n+[(0,1/min_denominator)], method='highs')
    obj = np.r_[num,0.]
    reslo = linprog(obj,**args)
    reshi = linprog(-obj,**args)
    if not (reslo.success and reshi.success):
        raise InfeasibleModel(f"No positive-conditioning coupling: {reslo.message} / {reshi.message}")
    return ConditionalInterval(float(reslo.fun),float(-reshi.fun),
                               reslo.x[:n]/reslo.x[n],
                               reshi.x[:n]/reshi.x[n])
