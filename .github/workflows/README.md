# Verification workflows

`tests.yml` runs Python tests in a separate failing job. `lean.yml` installs the
pinned toolchain/dependencies, then runs `python scripts/check_lean.py`: source-gap
policy, an actual `lake build`, and a complete named-theorem axiom audit. It permits
only the standard foundations documented in `research/lean_verification_scope.md`.
Local build outcomes and remote CI links/status are separately recorded in
`outputs/QA.md`. A passing Python job does not establish Lean verification.
