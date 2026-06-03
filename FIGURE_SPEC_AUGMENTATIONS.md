# AUGMENTATIONS AND CORRECTIONS

Verification performed from `reports/paper` on 2026-06-03:

- Rendered the four D-graded figures at 150 dpi with:
  - `pdftoppm -r 150 -png figures/fig_study_overview.pdf /tmp/fig_study_overview`
  - `pdftoppm -r 150 -png figures/fig_bimodal.pdf /tmp/fig_bimodal`
  - `pdftoppm -r 150 -png figures/fig_point_ranking.pdf /tmp/fig_point_ranking`
  - `pdftoppm -r 150 -png figures/fig_peraxis.pdf /tmp/fig_peraxis`
- Ran `pdffonts figures/fig_NAME.pdf` and `pdfinfo figures/fig_NAME.pdf` on every `figures/*.pdf`.

## Rendered inspection of the four D-graded figures

### `fig_study_overview.pdf`

Rendered PNG: `/tmp/fig_study_overview-1.png`, `2813 x 1063 px`.

What is visible:

- A very wide four-panel, slide-like overview with a large baked-in title, subtitle, panels A-D, flow arrows, a cuboid receiver schematic, waveform/data schematic, conditional-posterior schematic, and metric cards.
- The current baked-in title is `Calibrated posterior pipeline for RF capsule localization`; the subtitle is `full-wave simulation evidence now; physical phantom validation is the next gate`.
- Panel colors in the current rendered file are A `#2d6ca6`, B `#7560a8`, C `#1b5e20`, and D `#b15a2b`.
- The small explanatory labels in panels A-D are legible in the raw PNG only because the source canvas is huge; if scaled to a real column width, the smallest text becomes too small.

Additional issues not already explicit in the master spec:

- This PDF is not a Matplotlib PDF. `pdfinfo` reports `Producer: cairo 1.18.0`; `pdffonts` shows mixed Arial TrueType plus `[none]` Type 3 fonts. A Matplotlib-only `figstyle.py` will not fix this file.
- `pdffonts` Type 3 objects are `[none]` at object IDs `8 0`, `10 0`, `13 0`, `36 0`, `37 0`, `116 0`, and `183 0`. TrueType fonts are `Arial-BoldMT` and `ArialMT` subsets.
- `pdfinfo` page size is exactly `1350 x 510 pts` = `18.750 x 7.083 in`, not a legal single-column or double-column figure.
- Source SVG font sizes are `34px`, `25px`, `21px`, `20px`, `19px`, `18px`, `16px`, and `15px`; because cairo maps `1800 px -> 1350 pt`, those are `25.50 pt`, `18.75 pt`, `15.75 pt`, `15.00 pt`, `14.25 pt`, `13.50 pt`, `12.00 pt`, and `11.25 pt` in the raw PDF. If the `1350 pt` PDF is scaled to `515.5 pt`, the `15px`/`11.25 pt` text becomes `4.30 pt`, `18px`/`13.50 pt` becomes `5.15 pt`, and `19px`/`14.25 pt` becomes `5.44 pt`.
- The current file uses purple `#7560a8`, not the `#9467bd` purple called out elsewhere in the spec. This is still not an Okabe-Ito color, but the exact hex should be corrected.
- Panel A relies on color text (`green: upper pair; orange: lower pair`) and tiny port labels (`P1`, `P2`, `P3`, `P4`) rather than directly labeling receiver heights. Under column scaling, the port labels are easy to lose.
- Panel D mixes quantitative claims and scope caveat in a single mini-dashboard. The metric line `error-spread rank rho approx 0.60` is typographically informal for a final manuscript figure; use `Spearman rho = 0.60` or move this detail to the caption/table.

### `fig_bimodal.pdf`

Rendered PNG: `/tmp/fig_bimodal-1.png`, `930 x 431 px`.

What is visible:

- Two side-by-side scatter panels with a global title.
- Left panel: purple posterior samples, black true-position star near `y = 4 cm`, orange posterior-mean X near `y = 0`, dashed `y = 0` mirror plane, and an outlined mirror-mode star near `y = -4 cm`.
- Right panel: green posterior samples forming a narrow horizontal band around `y = -4 cm`, black true-position star and orange posterior-mean X nearly coincident, with the legend inside the axes at the top.

Additional issues not already explicit in the master spec:

- The x-axis scales are not comparable. From the selected data and Matplotlib autoscale, the left panel x-span is approximately `5.295 cm` (`-7.088` to `-1.793 cm`), while the right panel x-span is approximately `0.922 cm` (`0.871` to `1.793 cm`), a `5.744x` span ratio. The y-scale is shared (`-7.5` to `7.5 cm`), but the x-scale mismatch still exaggerates the right-panel compactness.
- The mirror-mode marker in the left panel is not included in the visible legend because the legend is drawn from the right axes only. It is annotated as `mirror mode`, but the open-star glyph itself has no legend key.
- The orange posterior-mean X sits directly on the dashed `y = 0` line in the left panel, so the reference line competes with the most important error visual.
- The right-panel legend consumes plotting space and visually dominates the panel, even though the data occupy a narrow band near the bottom.
- Exact selected-point values from the script/data: mirror point index `145`, true position `[-4.000, 4.000, -6.000] cm`, posterior mean `[-4.221, 0.134, -6.078] cm`, mirror-capture fraction `0.45`; anti-symmetric point index `360`, true position `[1.335, -3.842, -2.732] cm`, posterior mean `[1.322, -3.909, -2.668] cm`, mirror-capture fraction `0.0`.
- Color-only encoding remains: mirror samples use `#9467bd` at alpha `0.30`; anti-symmetric samples use `#1b5e20` at alpha `0.30`; posterior mean uses `#b15a2b`; mirror plane uses `#8a847b`.
- Source font sizes: global serif font `9 pt`, suptitle `9.2 pt`, panel titles `8.8 pt`, axes labels `9 pt`, ticks `8 pt`, legend `6.2 pt`, mirror annotation `6.6 pt`.

Corrections to the master spec:

- The honesty issue is not only generic `6x zoom`; the measured x-span ratio is approximately `5.744x`, with shared y-limits but incompatible x-limits.

### `fig_point_ranking.pdf`

Rendered PNG: `/tmp/fig_point_ranking-1.png`, `634 x 461 px`.

What is visible:

- Horizontal bar chart ranked by 3D MAE, with `Clean CFM` and `Det. backbone` as the two shortest bars at the top.
- Most classical bars are gray, the CFM bar is dark green, the deterministic backbone bar is dark gray, and a dotted green reference line is drawn at the CFM value.
- The baked-in title is `Point accuracy: CFM ties the backbone, beats all classical`.

Additional issues not already explicit in the master spec:

- The comparison between `Clean CFM` (`0.354 cm`, CI `0.339-0.369`) and `Det. backbone` (`0.340 cm`, no CI in the source tuple) is visually under-specified. The figure claims a tie but only one of the two headline methods has uncertainty shown.
- The reference line uses the same dark green `#1b5e20` as the Clean CFM bar and is drawn at exactly `0.354`, so it merges with the bar endpoint instead of acting as a clear reference.
- The x-axis spans out to the `GPR` value (`4.153 cm`), so the headline difference between `0.340 cm` and `0.354 cm` is compressed into a tiny region with no numeric labels.
- The y tick label `$k$-NN` introduces `DejaVuSans-Oblique` Type 3 math text while the rest of the labels are serif. This is unnecessary typographic inconsistency for a model name.
- Color-only encoding remains: `Clean CFM` is `#1b5e20`, `Det. backbone` is `#3d3d3a`, all other bars are `#8a847b` at alpha `0.60`, and there are no hatches/direct labels to survive grayscale.
- Source font sizes: title `9.5 pt`, x label `9 pt`, y/x ticks `8 pt`, base font `9 pt`.

### `fig_peraxis.pdf`

Rendered PNG: `/tmp/fig_peraxis-1.png`, `565 x 405 px`.

What is visible:

- Grouped bars for x/y/z per-axis MAE.
- Clean CFM and deterministic backbone are small bars near the baseline; HistGB is moderate; GPR dominates y and z.
- The legend is inside the plot area at the top and overlaps the tallest GPR y bar.
- The baked-in title is `Per-axis error: CFM is balanced; classical struggle on y`.

Additional issues not already explicit in the master spec:

- The y-axis maximum is visually tight at `3.0 cm` while the tallest source value is `GPR-y = 2.872 cm`, leaving only `0.128 cm` of headroom before the top axis. With the legend inside the axes, this makes the tallest bar look clipped/obscured.
- The title begins very close to the left edge of the cropped PDF. Even where not clipped, the tight bounding box leaves no optical margin.
- The y-axis label is `per-axis MAE (cm)` but the title says `classical struggle on y`; the chart should label the hard axis with a direct annotation or value callout instead of relying on title prose.
- Color-only encoding remains: `Clean CFM` is `#1b5e20`, `Det. backbone` is `#3d3d3a`, `HistGB` is `#b15a2b`, and `GPR` is `#8a847b`, all at alpha `0.85`; no hatch patterns or direct labels are present.
- The math `$y$` in the title creates `DejaVuSans-Oblique` Type 3 text for a plain axis letter.
- Source font sizes: title `9.5 pt`, axes labels `9 pt`, ticks `8 pt`, legend `6.6 pt`, base font `9 pt`.

## Global font and width measurements

Expected page widths are `252 pt` for single column or `515.5 pt`/`515.52 pt` for double column. Every PDF has at least one Type 3 font according to `pdffonts`.

| PDF | `pdfinfo` page size | Width in inches | Width status | Font types and Type 3 object IDs |
|---|---:|---:|---|---|
| `fig_bimodal.pdf` | `446.059 x 206.549 pts` | `6.195 in` | Off target | Type 3: `DejaVuSans-Oblique` obj `17 0`, `DejaVuSerif` obj `22 0` |
| `fig_cal_vs_disc.pdf` | `268.825 x 204.865 pts` | `3.734 in` | Off target | Type 3: `DejaVuSans-Oblique` obj `15 0`, `DejaVuSerif-Bold` obj `20 0`, `DejaVuSerif` obj `33 0` |
| `fig_crps.pdf` | `230.633 x 204.229 pts` | `3.203 in` | Off target | Type 3: `DejaVuSerif` obj `15 0` |
| `fig_deployability.pdf` | `272.889 x 199.603 pts` | `3.790 in` | Off target | Type 3: `DejaVuSerif` obj `15 0` |
| `fig_error_spread.pdf` | `241.693 x 205.125 pts` | `3.357 in` | Off target | Type 3: `DejaVuSans-Oblique` obj `17 0`, `DejaVuSerif` obj `22 0` |
| `fig_geometry.pdf` | `282.085 x 275.184 pts` | `3.918 in` | Off target | Type 3: `DejaVuSans-Oblique` obj `16 0`, `DejaVuSans` obj `21 0`, `DejaVuSerif-Bold` obj `34 0`, `DejaVuSerif` obj `58 0` |
| `fig_geometry_ablation.pdf` | `515.52 x 193.833 pts` | `7.160 in` | Width OK for double column | Type 3: `DejaVuSans-Oblique` obj `15 0`, `DejaVuSans` obj `20 0`, `DejaVuSerif-Bold` obj `28 0`, `DejaVuSerif` obj `47 0` |
| `fig_hero_grid.pdf` | `501.926 x 158.899 pts` | `6.971 in` | Off target | Type 3: `DejaVuSerif-Bold` obj `18 0`, `DejaVuSerif` obj `39 0` |
| `fig_method_cfm.pdf` | `1425 x 420 pts` | `19.792 in` | Off target | TrueType: `ArialMT`, `Arial-BoldMT`; Type 3: `[none]` objs `26 0`, `119 0`, `294 0` |
| `fig_method_condition_variants.pdf` | `1125 x 420 pts` | `15.625 in` | Off target | TrueType: `Arial-BoldMT`, `ArialMT`; Type 3: `[none]` objs `8 0`, `63 0` |
| `fig_orient.pdf` | `328.668 x 181.949 pts` | `4.565 in` | Off target | Type 3: `DejaVuSans` obj `16 0`, `DejaVuSerif` obj `21 0` |
| `fig_peraxis.pdf` | `270.88 x 194.037 pts` | `3.762 in` | Off target | Type 3: `DejaVuSans-Oblique` obj `15 0`, `DejaVuSerif` obj `20 0` |
| `fig_point_ranking.pdf` | `304.248 x 221.257 pts` | `4.226 in` | Off target | Type 3: `DejaVuSans-Oblique` obj `15 0`, `DejaVuSans` obj `21 0`, `DejaVuSerif` obj `29 0` |
| `fig_posterior_cloud.pdf` | `343.481 x 199.477 pts` | `4.770 in` | Off target | Type 3: `DejaVuSans-Oblique` obj `17 0`, `DejaVuSans` obj `24 0`, `DejaVuSerif` obj `29 0` |
| `fig_reliability.pdf` | `247.606 x 197.21 pts` | `3.439 in` | Off target; close but not `252 pt` | Type 3: `DejaVuSans-Oblique` obj `21 0`, `DejaVuSans` obj `26 0`, `DejaVuSerif-Bold` obj `36 0`, `DejaVuSerif` obj `43 0` |
| `fig_risk_coverage.pdf` | `270.592 x 199.081 pts` | `3.758 in` | Off target | Type 3: `DejaVuSans` obj `15 0`, `DejaVuSerif` obj `20 0` |
| `fig_study_overview.pdf` | `1350 x 510 pts` | `18.750 in` | Off target | TrueType: `Arial-BoldMT`, `ArialMT`; Type 3: `[none]` objs `8 0`, `10 0`, `13 0`, `36 0`, `37 0`, `116 0`, `183 0` |

## Corrections to master-spec statements

- The statement `ALL PDFs ship Type 3 fonts` is correct at the file level, but not every font in every PDF is Type 3. The cairo/SVG-derived files (`fig_study_overview.pdf`, `fig_method_cfm.pdf`, `fig_method_condition_variants.pdf`) mix embedded TrueType Arial subsets with `[none]` Type 3 glyph fonts. Fixing only Matplotlib `pdf.fonttype` will not eliminate all Type 3 fonts.
- `fig_study_overview.pdf` is a cairo/SVG-derived PDF (`Producer: cairo 1.18.0`) with page size `1350 x 510 pts`, not the Matplotlib output implied by `make_figures.py`. Its current title and colors come from `figures/fig_study_overview.svg`.
- The exact current purple in `fig_study_overview.pdf` is `#7560a8`, not `#9467bd`. The exact current panel colors are `#2d6ca6`, `#7560a8`, `#1b5e20`, and `#b15a2b`.
- `fig_geometry_ablation.pdf` already has a compliant double-column width of `515.52 pt`; its remaining problems are Type 3 fonts and visual layout, not width.
- `fig_reliability.pdf` is `247.606 pt` wide, not exactly `252 pt`; it is close to a single-column width but still fails an exact-width gate.
- `fig_method_condition_variants.pdf` was not listed in the summarized per-figure grades but is a major global outlier: `1125 x 420 pts`, cairo/SVG-derived, with Type 3 `[none]` font objects `8 0` and `63 0`.

## Missed global issues

- `savefig.bbox = "tight"` and per-figure `bbox_inches="tight"` are changing final page widths unpredictably. This is why nominal Matplotlib figure sizes such as `figsize=(3.4, 3.2)` become `304.248 pt` instead of a controlled `252 pt`.
- LaTeX inclusion widths are inconsistent and compound the problem: examples include `width=\linewidth` for `fig_study_overview.pdf` and `fig_bimodal.pdf`, `width=0.9\linewidth` for `fig_point_ranking.pdf` and `fig_peraxis.pdf`, `width=0.96\linewidth` for `fig_method_cfm.pdf`, and `width=0.86\linewidth` for `fig_reliability.pdf`.
- Several figures are near but not at target widths (`fig_reliability.pdf` `247.606 pt`, `fig_error_spread.pdf` `241.693 pt`, `fig_crps.pdf` `230.633 pt`). These should not be accepted as "close enough" if the CI gate is exact.
- The current palette has more colorblind/grayscale problems than the listed banned colors. Specific gaps:
  - `#1b5e20` vs `#3d3d3a` in `fig_point_ranking.pdf` and `fig_peraxis.pdf` are both dark and are not distinguishable enough without labels/hatches.
  - `#9467bd` at alpha `0.30` in `fig_bimodal.pdf` becomes a pale low-contrast sample cloud.
  - `#8a847b` gray bars are used as a catch-all for many baselines, so method identity is mostly position/order rather than visual encoding.
  - `#2d6ca6` and `#5a8fc0` are both blue-family colors used across the paper; they should not encode distinct semantic classes unless paired with marker/line/hatch differences.
- Mathtext is being used for plain labels such as `$y$` and `$k$-NN`, causing additional `DejaVuSans-Oblique` Type 3 font objects and inconsistent letterforms.
- Legends are frequently inside data regions (`fig_bimodal.pdf`, `fig_peraxis.pdf`), creating occlusion or excessive salience even when the master spec only calls out one bar overlap.

## Augmented global_actions list

Add these concrete actions to the global remediation plan:

1. Add a non-Matplotlib export path for SVG/cairo figures. `fig_study_overview.pdf`, `fig_method_cfm.pdf`, and `fig_method_condition_variants.pdf` must be rebuilt or converted so `pdffonts` reports zero `[none]` Type 3 fonts; Matplotlib rcParams alone will not fix them.
2. Remove `savefig.bbox = "tight"` from final publication exports. Use exact `figsize=(3.5, ...)` or `figsize=(7.16, ...)`, fixed margins, and `bbox_inches=None`; then assert `pdfinfo` width is exactly `252 pt` or `515.52 pt`.
3. Standardize LaTeX inclusion to `\includegraphics[width=\columnwidth]` for `252 pt` figures and `\includegraphics[width=\textwidth]` for `515.52 pt` figures. Do not use per-figure fractions such as `0.86\linewidth`, `0.9\linewidth`, `0.94\linewidth`, or `0.96\linewidth` for final figures.
4. Add a CI font gate that fails if any `pdffonts figures/*.pdf` row contains `Type 3`, including `[none]` Type 3 rows from cairo/SVG output.
5. Add a CI width gate that fails unless `pdfinfo` page width is in `{252, 515.5, 515.52}` within a small tolerance such as `0.05 pt`.
6. Add an effective-font-size gate: compute final LaTeX scale from PDF page width and inclusion width, and fail if any source text class or Matplotlib text size would render below `6 pt`.
7. For bar charts, require redundant encoding: direct numeric labels for headline bars, hatches for methods, and reference lines drawn behind bars with `zorder` below patches.
8. For paired comparison panels such as `fig_bimodal.pdf`, require matched axis limits or an explicit inset/zoom box with scale annotation. The current bimodal x-span ratio is approximately `5.744x`.
9. Move legends outside axes or reserve explicit legend bands. This applies immediately to `fig_bimodal.pdf` and `fig_peraxis.pdf`.
10. Replace color-only method identity with an Okabe-Ito palette plus marker/hatch/linestyle mapping, then run a grayscale render check on every figure.
