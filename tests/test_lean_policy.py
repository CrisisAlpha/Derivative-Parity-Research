"""Regression tests for the CI proof-gap and axiom guard."""
import importlib.util
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location("check_lean", Path(__file__).parents[1] / "scripts/check_lean.py")
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


def test_nested_comments_and_strings_do_not_create_false_gaps():
    assert policy.code_only('/- sorry /- axiom -/ admit -/ "unsafe" -- sorry\n theorem t').strip() == "theorem t"


@pytest.mark.parametrize("source", ["example : True := by sorry", "example : True := by\n admit",
                                  "axiom invented : False", "example : True := by native_decide",
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
