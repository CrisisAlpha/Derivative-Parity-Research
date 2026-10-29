"""Fail closed on source gaps, failed builds, or unapproved theorem axioms."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def code_only(text):
    # Lean has nested block comments. Preserve newlines for diagnostics.
    result, i, depth = [], 0, 0
    while i < len(text):
        if text.startswith("/-", i):
            depth += 1
            i += 2
        elif depth and text.startswith("-/", i):
            depth -= 1
            i += 2
        elif depth:
            result.append("\n" if text[i] == "\n" else " ")
            i += 1
        elif text.startswith("--", i):
            j = text.find("\n", i)
            i = len(text) if j < 0 else j
            result.append(" ")
        elif text[i] == '"':
            i += 1
            while i < len(text) and text[i] != '"':
                i += 2 if text[i] == "\\" else 1
            i += 1
            result.append(" ")
        else:
            result.append(text[i])
            i += 1
    if depth:
        raise ValueError("Unterminated block comment")
    return "".join(result)


def source_check(root=ROOT):
    files = [p for p in root.rglob("*.lean")
             if not any(x in {".lake", ".venv", ".git"} for x in p.relative_to(root).parts)]
    for path in files:
        code = code_only(path.read_text(encoding="utf-8"))
        if re.search(r"\b(sorry|sorryAx|admit|axiom|unsafe|native_decide|implemented_by)\b", code):
            raise RuntimeError(f"Forbidden proof gap, axiom or bypass: {path}")
    print(f"Lean source policy PASS ({len(files)} files)", flush=True)


def audit_output(output):
    expected = re.findall(r"#print axioms (\S+)", (ROOT / "AxiomAudit.lean").read_text())
    seen = set()
    for name, deps, empty in re.findall(
        r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|(does not depend on any axioms))", output
    ):
        axioms = set() if empty else set(re.findall(r"[\w.]+", deps))
        if axioms - ALLOWED_AXIOMS:
            raise RuntimeError(f"Unapproved axioms for {name}: {axioms - ALLOWED_AXIOMS}")
        seen.add(name)
    if seen != set(expected):
        raise RuntimeError(f"Incomplete audit: expected {set(expected)}, saw {seen}")
    print(f"Axiom allowlist PASS ({len(seen)} declarations)", flush=True)


if __name__ == "__main__":
    source_check()
    if "--source-only" not in sys.argv:
        subprocess.run(["lake", "build"], cwd=ROOT, check=True)
        proc = subprocess.run(["lake", "env", "lean", "-DwarningAsError=true", "AxiomAudit.lean"],
                              cwd=ROOT, text=True, encoding="utf-8", capture_output=True)
        print(proc.stdout, end="")
        print(proc.stderr, end="", file=sys.stderr)
        proc.check_returncode()
        audit_output(proc.stdout)
