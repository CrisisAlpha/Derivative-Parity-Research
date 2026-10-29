# Historical handoff artifact

`handoff-v0.2.pdf` is the unchanged PDF supplied in the original handoff archive.
It is not a build of the current `manuscript/main.tex` and must not be used as
evidence that current source compiles.

Run `python scripts/build_manuscript.py` with Tectonic 0.15.0 and the
`.[manuscript]` Python extra to build current source. The separate manuscript CI
job retains the resulting PDF, compiler log, extracted text and SHA256 provenance
under `outputs/manuscript-build/` as a draft review artifact. No release or paper
publication is performed. `references.bib` is retained for migration; the active
manuscript currently uses its inline bibliography.
