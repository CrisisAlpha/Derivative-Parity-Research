"""Generate candidates from HiGHS, then reject unless exact checks pass.

Generation is optional: verification of committed witnesses needs no solver.
Rational reconstruction is a candidate search, never a feasibility assumption.
"""
from fractions import Fraction as F
import json
from pathlib import Path
from parity_ot.examples import binary_three_event, two_date_underlying, three_date_underlying
from parity_ot.certificates import exact_model, verify_certificate

b, d2, d2j, d3 = binary_three_event(), two_date_underlying(), two_date_underlying(.2), three_date_underlying()
instances = {"binary": b["full"], "two_ot": d2["ot"], "two_mot": d2["mot"],
             "two_joint_mot": d2j["mot"], "three_ot": d3["ot"], "three_mot": d3["mot"],
             "barrier_ot": d3["barrier_ot"], "barrier_mot": d3["barrier_mot"]}
result = {}
for name, interval in instances.items():
    certificate = {}
    for side in ("lower", "upper"):
        rational = lambda x: str(F(float(x)).limit_denominator(1000000))
        certificate[side] = {
            "value": rational(getattr(interval, side)),
            "primal": list(map(rational, getattr(interval, side + "_coupling"))),
            "dual": list(map(rational, getattr(interval, side + "_dual"))),
        }
    if name == "binary":
        # Human-readable hedges: AB + BC - B and AC.
        certificate["lower"]["dual"] = list(map(str, [0,0,-1,0,1,1,0]))
        certificate["upper"]["dual"] = list(map(str, [0,0,0,0,0,0,1]))
    verify_certificate(name, certificate)
    result[name] = certificate
path = Path(__file__).resolve().parents[1] / "data/synthetic/rational_certificates.json"
path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(result)} exactly checked certificate pairs to {path}")
