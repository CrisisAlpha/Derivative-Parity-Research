# Verification workflows

`tests.yml` runs Python tests in a separate failing job. `lean.yml` installs the
pinned toolchain/dependencies, then runs `python scripts/check_lean.py`: source-gap
policy, an actual `lake build`, and a complete named-theorem axiom audit. It permits
only the standard foundations documented in `research/lean_verification_scope.md`.
Local build outcomes and remote CI links/status are separately recorded in
`outputs/QA.md`. A passing Python job does not establish Lean verification.

`manuscript.yml` separately compiles the actual `manuscript/main.tex` using
Tectonic 0.15.0 and verifies that its generated PDF contains current-source text,
nonempty pages and the comparison figure, with no unresolved citations or
references in the final compiler log. Source/PDF hashes and the compiler output
are retained in a draft review artifact, including logs on failure. It does not
read the historical handoff PDF, merge the PR or publish a release.
