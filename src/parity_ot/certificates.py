"""Exact finite certificates, independently checked with Fraction arithmetic.

The model rows are constructed from integer settlement states, not rounded
solver matrices. A candidate reconstructed from a solver is accepted only if
every exact primal equation and every statewise dual inequality holds.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def dot(a, b):
    if len(a) != len(b):
        raise ValueError("Dimension mismatch")
    return sum((x * y for x, y in zip(a, b)), F(0))


def exact_model(name):
    """Return states, equality-row labels, rows, prices and target payoff."""
    if name == "binary":
        states = list(product((0, 1), repeat=3))
        rows = [[F(1)] * 8] + [
            [F(f(a, b, c)) for a, b, c in states]
            for f in (lambda a,b,c:a, lambda a,b,c:b, lambda a,b,c:c,
                      lambda a,b,c:a*b, lambda a,b,c:b*c, lambda a,b,c:a*c)]
        return states, ["mass", "A", "B", "C", "AB", "BC", "AC"], rows, \
            list(map(F, ("1", "3/5", "11/20", "9/20", "2/5", "3/10", "11/50"))), \
            [F(a*b*c) for a,b,c in states]
    if name not in {"two_ot", "two_mot", "two_joint_mot", "three_ot",
                    "three_mot", "barrier_ot", "barrier_mot"}:
        raise ValueError(name)
    levels = [[90,110], [70,90,110,130]]
    margins = [[F(1,2)]*2, [F(1,4)]*4]
    if name.startswith(("three", "barrier")):
        levels.append([50,70,90,110,130,150])
        margins.append(list(map(F, ("1/8","1/8","1/4","1/4","1/8","1/8"))))
    states = list(product(*levels))
    rows, prices, labels = [[F(1)]*len(states)], [F(1)], ["mass"]
    for t, support in enumerate(levels):
        for x, p in zip(support, margins[t]):
            rows.append([F(s[t] == x) for s in states])
            prices.append(p)
            labels.append(f"S{t+1}={x}")
    if name == "two_joint_mot":
        rows.append([F(s == (110,130)) for s in states])
        prices.append(F(1,5))
        labels.append("S1=110,S2=130")
    if name.endswith("mot"):
        for t in range(len(levels)-1):
            for history in product(*levels[:t+1]):
                rows.append([F(s[t+1]-s[t]) if s[:t+1] == history else F(0)
                             for s in states])
                prices.append(F(0))
                labels.append(f"gain after {history}")
    if name.startswith("barrier"):
        payoff = [F(max(s) >= 130) for s in states]
    else:
        payoff = [F(s[0] == 110 and s[1] <= 90 and
                    (len(s) == 2 or s[2] >= 130)) for s in states]
    return states, labels, rows, prices, payoff


def verify_certificate(name, certificate):
    """Raise on any failed exact constraint; no tolerances or solver calls."""
    states, labels, rows, prices, payoff = exact_model(name)
    for side in ("lower", "upper"):
        endpoint = certificate[side]
        q = list(map(F, endpoint["primal"]))
        dual = list(map(F, endpoint["dual"]))
        value = F(endpoint["value"])
        if len(q) != len(states) or len(dual) != len(rows):
            raise ValueError(f"{name}/{side}: dimension mismatch")
        if any(x < 0 for x in q):
            raise ValueError(f"{name}/{side}: negative mass")
        for label, row, price in zip(labels, rows, prices):
            if dot(row, q) != price:
                raise ValueError(f"{name}/{side}: failed {label}")
        for i, h in enumerate(payoff):
            hedge = dot(dual, [row[i] for row in rows])
            if (side == "lower" and hedge > h) or (side == "upper" and hedge < h):
                raise ValueError(f"{name}/{side}: hedge fails at {states[i]}")
        if dot(q, payoff) != value or dot(dual, prices) != value:
            raise ValueError(f"{name}/{side}: primal/dual value mismatch")


def load_certificates():
    path = Path(__file__).resolve().parents[2] / "data/synthetic/rational_certificates.json"
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    for name, certificate in load_certificates().items():
        verify_certificate(name, certificate)
        print(f"{name}: exact primal/dual PASS [{certificate['lower']['value']}, "
              f"{certificate['upper']['value']}]")
