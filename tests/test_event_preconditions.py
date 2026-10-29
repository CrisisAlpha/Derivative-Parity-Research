import numpy as np
import pytest
from parity_ot.transport import conditional_ratio_interval, InfeasibleModel, martingale_features, marginal_features


@pytest.mark.parametrize("num,den,match", [
    ([0,.5],[0,1],"0/1"), ([0,1],[0,2],"0/1"),
    ([-1,0],[0,1],"0/1"), ([0,1],[1,0],"subset"),
    ([0,np.nan],[0,1],"finite")])
def test_conditional_event_preconditions(num,den,match):
    with pytest.raises(ValueError,match=match):
        conditional_ratio_interval(num,den,[[1,1]],[1],[1])


@pytest.mark.parametrize("cutoff", [np.nan, np.inf, 0, -1, 1.01])
def test_finite_positive_conditioning_cutoff(cutoff):
    with pytest.raises(ValueError,match="min_denominator"):
        conditional_ratio_interval([0,1],[0,1],[[1,1]],[1],[1],cutoff)


def test_impossible_conditioning_event_is_infeasible():
    with pytest.raises(InfeasibleModel):
        conditional_ratio_interval([0,0],[0,0],[[1,1]],[1],[1])


def test_nearby_distinct_histories_and_marginals_are_not_merged():
    s = np.array([[1.,0.], [1.,2.], [1.000001,0.], [1.000001,2.]])
    mart = martingale_features(s)
    np.testing.assert_allclose(mart, [[-1,1,0,0],[0,0,-1.000001,.999999]], rtol=0, atol=1e-15)
    assert np.count_nonzero(mart[0,2:]) == np.count_nonzero(mart[1,:2]) == 0
    rows, _ = marginal_features(s,[{1.:.5,1.000001:.5},{0.:.5,2.:.5}])
    assert np.array_equal(rows[:2], [[1,1,0,0],[0,0,1,1]])


def test_equal_last_price_retains_distinct_earlier_histories():
    s = np.array([[90,100,90],[90,100,110],[110,100,90],[110,100,110]])
    rows = martingale_features(s)
    assert np.array_equal(rows[-2:], [[-10,10,0,0],[0,0,-10,10]])
    # Last-price conditioning alone cancels these two nonzero history gains.
    q = np.array([.5,0,0,.5])
    assert (rows[-2:] @ q).sum() == 0
    assert np.array_equal(rows[-2:] @ q, [-5,5])
