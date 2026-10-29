from copy import deepcopy
from fractions import Fraction as F
import numpy as np
import pytest
from parity_ot.certificates import exact_model, load_certificates, verify_certificate
from parity_ot.examples import binary_three_event, two_date_underlying, three_date_underlying


@pytest.mark.parametrize("name", list(load_certificates()))
def test_exact_endpoints_all_states_and_all_constraints(name):
    verify_certificate(name, load_certificates()[name])


def test_exact_model_matches_solver_instances():
    b, d2, d2j, d3 = binary_three_event(), two_date_underlying(), two_date_underlying(.2), three_date_underlying()
    cases = [("binary", b, "full", "payoff"), ("two_ot", d2, "ot", "payoff"),
             ("two_mot", d2, "mot", "payoff"), ("two_joint_mot", d2j, "mot", "payoff"),
             ("three_ot", d3, "ot", "payoff"), ("three_mot", d3, "mot", "payoff"),
             ("barrier_ot", d3, "barrier_ot", "barrier"), ("barrier_mot", d3, "barrier_mot", "barrier")]
    for name, e, key, target in cases:
        states, _, rows, prices, payoff = exact_model(name)
        assert np.array_equal(states, e["states"])
        assert np.array_equal(np.array(rows, dtype=float), e[key].certificate_features)
        assert np.array_equal(np.array(prices, dtype=float), e[key].certificate_prices)
        assert np.array_equal(np.array(payoff, dtype=float), e[target])
    assert sum(x.startswith("gain after") for x in exact_model("three_mot")[1]) == 10


@pytest.mark.parametrize("part", ["primal", "dual", "value"])
def test_corrupted_certificate_is_rejected(part):
    cert = deepcopy(load_certificates()["binary"])
    if part == "value":
        cert["lower"][part] = "0"
    else:
        cert["lower"][part][0] = str(F(cert["lower"][part][0]) + 1)
    with pytest.raises(ValueError):
        verify_certificate("binary", cert)
