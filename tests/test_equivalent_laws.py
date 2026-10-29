"""Exact finite demonstrations; these tests do not constitute Lean proofs."""
from fractions import Fraction as F
import pytest
from parity_ot.certificates import exact_model, load_certificates, dot


@pytest.mark.parametrize("t", [F(0), F(1,1000), F(1,2), F(999,1000), F(1)])
def test_binary_parametrization_and_full_support(t):
    x = F(3,20) + F(7,100)*t
    q = [F(8,25)-x, x-F(7,100), x-F(3,20), F(3,10)-x,
         x-F(1,50), F(11,50)-x, F(2,5)-x, x]
    _, _, rows, prices, payoff = exact_model("binary")
    cert = load_certificates()["binary"]
    mixture = [(1-t)*F(lo)+t*F(hi) for lo,hi in
               zip(cert["lower"]["primal"],cert["upper"]["primal"])]
    assert q == mixture
    assert all(dot(row,q) == p for row,p in zip(rows,prices))
    assert dot(q,payoff) == x
    assert all(p > 0 for p in q) == (0 < t < 1)
    assert q[2] == x-F(3,20) and q[5] == F(11,50)-x


def test_two_date_full_support_feasible_midpoint():
    q = [F(x,24) for x in [5,3,3,1,1,3,3,5]]
    _, labels, rows, prices, payoff = exact_model("two_mot")
    assert all(p > 0 for p in q)
    assert all(dot(row,q) == p for row,p in zip(rows,prices))
    assert sum(label.startswith("gain after") for label in labels) == 2
    assert F(1,12) < dot(q,payoff) < F(1,4)
