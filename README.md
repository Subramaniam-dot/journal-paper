# Journal paper — calibrated-posterior wireless capsule endoscope RF localization

LaTeX source + assets for the journal manuscript. Synced to Overleaf via GitHub.

## Compile

- **Overleaf:** import this repo (or link it under *Menu → GitHub*), set **`main.tex`** as the main
  document. Bibliography is `refs.bib` (BibTeX, IEEEtran style) — Overleaf builds it automatically.
- **Local:** `latexmk -pdf main.tex` (needs the `IEEEtran` class + `bibtex`).

## Structure

```
main.tex            IEEEtran journal manuscript (root)
sections/           intro, related, dataset, method, results, discussion, conclusion
refs.bib            BibTeX references
figures/            all figures — main.tex includes the *.pdf versions (vector, fonts embedded)
*.py / *.mjs        figure generators (see below)
package.json        node deps for the .mjs (D3/SVG) generators
```

## Regenerating figures (optional — built PDFs are already committed)

- **matplotlib figures:** `python make_figures.py`, `make_geometry_figs.py`, `make_bimodal_fig.py`,
  `make_phase_sensitivity_fig.py` (shared style in `paperstyle.py` — sans-serif, embedded TrueType,
  Okabe–Ito colorblind palette, IEEE column widths).
- **D3/SVG schematics:** `npm install` then `node make_study_overview.mjs`, `make_method_cfm_d3.mjs`,
  `make_condition_variants.mjs`.

All figures pass the IEEE submission gate (0 Type-3 fonts, embedded TrueType, correct column widths).

## Note

All quantitative results are **SIMULATION** (full-wave CST, 4-receiver MICS-band cuboid). The
contribution is the calibrated posterior; no claim to state-of-the-art point accuracy.
