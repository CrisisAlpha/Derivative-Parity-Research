"""Regression tests for the CI proof-gap and axiom guard."""
import importlib.util
import json
import shutil
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location("check_lean", Path(__file__).parents[1] / "scripts/check_lean.py")
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


def test_nested_comments_and_strings_do_not_create_false_gaps():
    assert policy.code_only('/- sorry /- axiom -/ admit -/ "unsafe" -- sorry\n theorem t').strip() == "theorem t"


@pytest.mark.parametrize("source", ["example : True := by sorry", "example : True := by\n admit",
                                  "axiom invented : False", "example : True := by native_decide",
                                  "axioms invented : False", "constant invented : False",
                                  "constants (invented : False)", "namespace Demo\nconstant invented : False\nend Demo",
                                  "axioms\n invented : False", "constants\n (a b : False)",
                                  "unsafe def bypass := 0"])
def test_source_policy_rejects_gaps_in_any_project_module(tmp_path, source):
    nested = tmp_path / "Nested"
    nested.mkdir()
    (nested / "Proof.lean").write_text(source)
    with pytest.raises(RuntimeError, match="Forbidden"):
        policy.source_check(tmp_path)


def test_axiom_audit_rejects_unexpected_axioms_and_missing_results():
    with pytest.raises(RuntimeError, match="Unapproved axioms"):
        policy.audit_output("'ParityOT.Static.sharp_bounds' depends on axioms: [sorryAx]")
    with pytest.raises(RuntimeError, match="Incomplete audit"):
        policy.audit_output("")


def test_print_axioms_is_allowed_but_declarations_still_fail(tmp_path):
    path = tmp_path / "Audit.lean"
    path.write_text("#print axioms Demo.theorem\n")
    policy.source_check(tmp_path)
    path.write_text("#print axioms Demo.theorem\nconstants (bad : False)\n")
    with pytest.raises(RuntimeError, match="Forbidden"):
        policy.source_check(tmp_path)


@pytest.mark.parametrize("change", ["remove_audit", "remove_claim", "add_promotion", "duplicate_audit"])
def test_promoted_claims_cannot_escape_audit(tmp_path, change):
    (tmp_path / "research").mkdir()
    for name in ["research/formal_claims.json", "research/claim_registry.md", "AxiomAudit.lean"]:
        shutil.copyfile(policy.ROOT / name, tmp_path / name)
    if change == "remove_claim":
        path = tmp_path / "research/formal_claims.json"
        claims = json.loads(path.read_text())
        del claims["S-01"]
        path.write_text(json.dumps(claims))
    elif change == "add_promotion":
        path = tmp_path / "research/claim_registry.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n| NEW | X | **FORMALIZED_AND_COMPILED** | X |\n", encoding="utf-8")
    else:
        path = tmp_path / "AxiomAudit.lean"
        source = path.read_text()
        line = "#print axioms ParityOT.Static.sharp_bounds"
        path.write_text(source.replace(line, "") if change == "remove_audit" else source + "\n" + line)
    with pytest.raises(RuntimeError, match="mismatch"):
        policy.audit_inventory(tmp_path)
