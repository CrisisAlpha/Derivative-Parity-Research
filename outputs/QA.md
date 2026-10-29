# Quality assurance snapshot - October 29, 2026

- `PYTHONPATH=src python -m pytest -q` : **9 passed**.
- `python -m parity_ot.examples` : all synthetic results produced.
- `PYTHONPATH=src python scripts/build_notebook.py` : second notebook executed
  with `nbclient` and stored with outputs.
- `PYTHONPATH=src python scripts/render_results.py` : summary JSON and PNG chart
  generated from the same code used in unit tests.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` in
  `manuscript/` : compiled a 5-page PDF after cleaning stale auxiliary files.
- PDF rendered to page images for visual inspection; all five pages readable.
- Existing three-binary-event notebook copied into the research package for
  continuity; its source was from the previous conversation prototype.
- No live prediction-market or option data used; no actual GitHub repository
  was changed, no orders placed, and no paper was publicly published.
- The manuscript uses a self-contained reference list to compile without
  `bibtex`; `references.bib` is retained for migration to Overleaf.

**Numerical caveats:** results are sharp *conditional on the finite supports,
normalized quotes and modeling constraints written in the code*. They are not
continuous-time bounds, executable venue arbitrage estimates, or forecasts.
