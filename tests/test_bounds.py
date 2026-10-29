"""Exact numerical assertions and pointwise hedge checks on synthetic cases."""
import numpy as np
import pytest

from parity_ot.examples import (binary_three_event, two_date_underlying,
                                three_date_underlying)
from parity_ot.transport import InfeasibleModel, price_interval


def test_binary_three_event_bounds_and_conditional():
    e = binary_three_event()
    assert np.allclose([e['single'].lower,e['single'].upper], [0.,.45])
    assert np.allclose([e['neighbors'].lower,e['neighbors'].upper],[.15,.30])
    assert np.allclose([e['full'].lower,e['full'].upper],[.15,.22])
    assert np.allclose(e['conditional'], [.375,.55])
    assert e['full'].verify(e['payoff'])


def test_binary_no_arbitrage_violation():
    e = binary_three_event()
    # Adding an inconsistent 30% quoted triple contradicts the 22% AC quote.
    f = np.vstack([e['features'],e['payoff']])
    p = np.r_[e['prices'],.30]
    with pytest.raises(InfeasibleModel):
        price_interval(e['payoff'],f,p,p)


def test_two_date_ordinary_vs_martingale():
    e = two_date_underlying()
    assert np.allclose([e['ot'].lower,e['ot'].upper], [0.,.50])
    assert np.allclose([e['mot'].lower,e['mot'].upper], [1./12.,.25])
    assert e['ot'].verify(e['payoff'])
    assert e['mot'].verify(e['payoff'])
    for q in [e['mot'].lower_coupling, e['mot'].upper_coupling]:
        assert np.allclose(e['martingale_features']@q,0.,atol=1e-9)
        assert np.isclose(q.sum(),1.)
        assert np.all(q >= -1e-10)


def test_two_date_explicit_dynamic_hedges():
    e = two_date_underlying()
    s = e['states']
    h = e['payoff']
    # Gains from buying -1/20 shares at time 1 IF S1=110, zero initial cost.
    d = ((s[:,0] == 110).astype(float))*(s[:,1]-s[:,0])
    upper = (s[:,1] == 130).astype(float) - d/20.
    lower = ((s[:,0] == 110).astype(float)
             - (s[:,1] == 110).astype(float))/3. - d/60.
    assert np.all(lower <= h+1e-10)
    assert np.all(h <= upper+1e-10)
    # Prices under the given marginal distributions: 1/12 and 1/4.
    assert np.isclose(.5/3. - .25/3.,e['mot'].lower)
    assert np.isclose(.25,e['mot'].upper)


def test_joint_quote_tightens_mot_interval():
    e = two_date_underlying(extra_joint_quote=.20)
    assert np.allclose([e['mot'].lower,e['mot'].upper], [.10,.20])
    assert e['mot'].verify(e['payoff'])


def test_three_date_full_filtration():
    e = three_date_underlying()
    assert e['states'].shape == (48,3)
    assert np.allclose([e['ot'].lower,e['ot'].upper], [0.,.25])
    assert np.allclose([e['mot'].lower,e['mot'].upper], [0.,.0625])
    assert np.allclose([e['barrier_ot'].lower,e['barrier_ot'].upper],[.25,.5])
    assert np.allclose([e['barrier_mot'].lower,e['barrier_mot'].upper],[.275,.375])
    assert e['mot'].verify(e['payoff'])
    for q in [e['mot'].lower_coupling,e['mot'].upper_coupling]:
        assert np.allclose(e['martingale_features']@q,0.,atol=1e-9)


def test_quote_bands_do_not_shrink_interval():
    e = binary_three_event()
    exact = e['full']
    bands = price_interval(e['payoff'],e['features'],
                           e['prices']-.005,e['prices']+.005)
    assert bands.lower <= exact.lower + 1e-8
    assert bands.upper >= exact.upper - 1e-8
    assert bands.upper_dual is None  # Incomplete dual would be misleading.


def test_invalid_quote_order():
    with pytest.raises(ValueError):
        price_interval([0,1],[[0,1]],[.7],[.6])


def test_conditional_ratio_with_exact_and_band_quote():
    from parity_ot.transport import conditional_ratio_interval
    e = binary_three_event()
    s = e['states']
    a, b, c = s.T
    numerator = (a*b*c).astype(float)
    denominator = (a*b).astype(float)
    exact = conditional_ratio_interval(numerator, denominator,
                                       e['features'], e['prices'], e['prices'])
    assert np.allclose([exact.lower,exact.upper], [.375,.55])
    # Now vary the price of A in a two-quote synthetic system and bound P(B|A).
    f = np.vstack([a.astype(float),(a*b).astype(float)])
    conditional = conditional_ratio_interval((a*b).astype(float),a.astype(float),
                                             f,[.58,.40],[.62,.40])
    assert np.allclose([conditional.lower,conditional.upper],
                       [.4/.62,.4/.58])
    for q in [conditional.lower_coupling,conditional.upper_coupling]:
        assert np.isclose(q.sum(),1.)
        assert q.min() >= -1e-8
