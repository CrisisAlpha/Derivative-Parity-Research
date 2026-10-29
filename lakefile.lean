import Lake
open Lake DSL

package parity_ot where
  moreLeanArgs := #["-DwarningAsError=true"]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.20.0"

@[default_target]
lean_lib LeanNotes where
  srcDir := "."
  roots := #[`LeanNotes, `StaticCertificate, `TwoDateCertificate]
