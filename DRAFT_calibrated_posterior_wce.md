# DRAFT — Calibrated Posterior WCE Localization (simulation paper)

> **Status:** scaffold / skeleton with real content where it exists. NOT a finished paper.
> **Provenance discipline:** Every quantitative number is pulled from a named findings/report
> file and cited inline as `[src: <file>]`. Numbers not found in the sources are marked
> `[VERIFY]` and must NOT be treated as established. All numbers are **full-wave CST simulation**,
> not measured/physical-phantom data — flagged loudly throughout.
> **Created:** 2026-06-02. **Owner:** Subramaniam Murugesan.

---

## 1. Working title + abstract

### Working title (candidates — all carry "simulation" / "full-wave")

- **Primary:** *"A Calibrated Posterior for Wireless Capsule Endoscope Localization at a Four-Receiver MICS-Band Budget: A Full-Wave Simulation Study"*
- Alt A: *"Conditional Flow Matching Yields the First Calibrated Position Posterior for WCE RF Localization (Full-Wave CST Simulation)"*
- Alt B: *"Uncertainty-First WCE Localization at 0.4 GHz with Four Receivers: A Full-Wave Simulation Benchmark of Calibrated Generative Posteriors"*

### Abstract (skeleton; first sentence locks sim + calibration, no point-SOTA language)

> **This is a full-wave electromagnetic (CST) simulation study; we report no measured-phantom
> or in-vivo results.** We study wireless capsule endoscope (WCE) localization at a deployment-
> realistic budget — four body-surface receivers operating in the 0.4 GHz MICS band — and ask
> not "how accurate is the point estimate?" but "can the system report *calibrated* confidence in
> where the capsule is?" Using full-wave CST simulation on a corrected cuboid phantom geometry
> (V4_fix2; receivers on the ±x/±z vertical side walls, no y-face coverage) and a strictly
> position-grouped 5-fold cross-validation protocol, we benchmark a conditional flow-matching
> (CFM) posterior against a deterministic regression backbone and a panel of probabilistic and
> classical baselines. The central result is a *calibration* result: the clean CFM posterior is
> the only method that simultaneously (i) pays no point-accuracy tax relative to the deterministic
> backbone [src: Finding - UQ bake-off calibration; Finding - CFM vs all methods (rich 180-D)],
> (ii) achieves near-nominal coverage *from its own samples* without any conformal patch
> (cov50/90/95 = 0.766 / 0.935 / 0.944) [src: Finding - UQ bake-off calibration], and (iii)
> exhibits real error-vs-spread discrimination (Spearman ρ = 0.601) [src: Finding - UQ bake-off
> calibration]. We further show that posterior *modality* tracks forward-operator invertibility:
> on a mirror-symmetric receiver array the CFM posterior is genuinely bimodal (mirror-capture
> 0.497, 72.1% of high-|y| points flagged bimodal) where competing methods only widen or collapse
> [src: Finding - physics-modality correspondence], and that the same posterior width tracks the
> orientation-induced uncertainty of an unknown, tumbling capsule pose (ρ ≈ 0.85–0.91) [src:
> Finding - orientation-marginal uncertainty; Finding - orientation intelligence (5-pose)]. An
> honest feature-deployability ablation locates the single-tone, magnitude-only deployable floor
> at ~1.5 cm and shows the sub-cm regime requires phase-coherent receivers [src: Finding - feature
> deployability ablation]. **We make no claim to state-of-the-art point accuracy**: at this
> hardware budget real-phantom systems are more accurate, and we declare the sim-vs-real and
> frequency-band confounds explicitly. The contribution is the *first calibrated position posterior
> for WCE RF localization at the four-receiver MICS budget*. Simulation-only is standard practice
> in this subfield [Yoshitake 2022; Wisanmongkol 2024; Ye 2014; Nadimi 2014; Pourhomayoun 2014;
> Hiyoshi 2019]; a physical-phantom companion is identified as the next evidence gate.

---

## 2. Contribution box (two-tier)

> **CONTRIBUTION (read both tiers together).**
>
> **(A) What we do NOT claim.** We are *not* the most accurate point estimator at the four-receiver
> MICS-band budget. Real-phantom RSSI systems at 2.45 GHz report better point accuracy (Hasnain
> 2026: 1.69 cm 3D RMSE; Hasnain 2024: 2.38 cm RMSE, real ASTM/heterogeneous phantoms) [src: WCE
> comparator audit], and our numbers are full-wave **simulation**, at a ~6× lower frequency, under
> a stricter (position-grouped) protocol. We do not contest the point-accuracy leaderboard.
>
> **(B) What we DO claim — and it is point-tax-free.** We present the **first calibrated position
> posterior for WCE RF localization at the four-receiver MICS budget**. The clean CFM posterior is
> calibrated *from its own samples* (cov90 = 0.935, ρ_err-spread = 0.601) [src: Finding - UQ bake-off
> calibration] while costing essentially nothing in point accuracy: clean CFM 3D MAE 0.354 cm vs
> deterministic-backbone 0.340 cm on the combined N=3935 rich set — a tie within seed noise — and
> CFM significantly beats all 10 classical baselines on the same position-paired folds [src: Finding
> - CFM vs all methods (rich 180-D); rich_unified_benchmark.md]. Posterior *modality* tracks
> forward-operator invertibility (bimodal where the array leaves y unobservable, unimodal where it
> does not) [src: Finding - physics-modality correspondence], and the posterior width carries the
> aleatoric uncertainty of unknown capsule orientation [src: Finding - orientation-marginal
> uncertainty]. To our knowledge no prior WCE-RF method reports empirical multi-level coverage under
> position-grouped CV; the one Bayesian precedent (Nadimi 2014) reports RMSE-vs-CRLB on parametric
> path-loss simulation, with no empirical coverage [src: Nadimi 2014 paper note].

---

## 3. Section skeleton

### 3.1 Introduction
- WCE clinical context: capsule travels the GI tract; physicians need to *act* on findings, and
  acting safely requires knowing not just where the capsule probably is but *how confident* that
  estimate is. (Clinical-threshold framing borrowed from prior literature — Yoshitake 2022, Hasnain
  2024 use a ~4 cm threshold; **no clinician feedback incorporated yet** [src: Finding - Operating
  point at 50% coverage].)
- The field is essentially 100% point estimators. Frame the gap: many 4-Rx methods report sub-3 cm
  point accuracy, none report calibrated empirical coverage at this budget [src: Uncertainty as the
  selling angle].
- Thesis of the paper: **calibration, not point accuracy, is the contribution.** State two-tier
  claim (§2) up front.
- Deployable hardware budget = 4 receivers, 0.4 GHz MICS narrowband (401–406 MHz) — regulatory-
  relevant implant band [src: WCE comparator audit (PHAROS reference row)].
- Simulation-only scope declared in the first paragraph; precedent list (Yoshitake 2022;
  Wisanmongkol 2024; Ye 2014 CRLB; Nadimi 2014 Bayesian RSS; Pourhomayoun 2014; Hiyoshi 2019).

### 3.2 Related work
- **WCE RF localization landscape** — point estimators dominate. Pull the comparator rows from §5.
- **Bayesian / probabilistic prior art** — Nadimi 2014 is the closest: Rayleigh-fading + Gamma-PLE
  likelihood, Gaussian anchor priors, 1.6 mm RMSE in 1000 Monte-Carlo trials with 5 anchors, but
  *parametric path-loss simulation only* and *RMSE-vs-CRLB with no empirical coverage* [src: Nadimi
  2014 paper note]. Our novelty wording is therefore: not "first Bayesian" but **"first
  flow-matching/generative posterior" and "first with empirical multi-level coverage under
  position-grouped CV."**
- **CRLB / theoretical bounds** — Ye 2014, Hany SPLD-WCL (CRLB on path-loss). These are analytical
  lower bounds, not empirical coverage claims [src: Uncertainty as the selling angle].
- **Generative posterior methods elsewhere** — Lei 2025 (full-posterior outdoor wireless
  localization) is the one paper arguing the same case in a different domain [src: Uncertainty as
  the selling angle]. CFM / flow-matching posterior estimation lineage (FMPE/SBI). [VERIFY exact
  CFM-method citations to add — CARD, CFM, FMPE references live in MEMORY/novelty audit, confirm
  before writing.]
- **Simulation-only precedent in this subfield** — Yoshitake 2022, Wisanmongkol 2024, Pourhomayoun
  2014, Hiyoshi 2019, Nadimi 2014, Ye 2014 are all sim or sim-dominant; establishes that a
  sim-first paper is normal here.

### 3.3 CST geometry + dataset
- **Geometry:** corrected `V4_fix2` cuboid physical-tank topology. Four receivers on the vertical
  side walls (±x and ±z faces); **no y-face coverage** — top/floor bare [src: CUBOID_RESEARCH_QUESTIONS
  override 2026-05-28; rich_unified_benchmark.md]. Body dimensions L=273, W=278, H=380 mm,
  Antenna_shift=70 mm [src: CUBOID_RESEARCH_QUESTIONS override 2026-05-28].
- **Why this geometry:** prior assumption put a receiver pair on the floor/open-top direction; the
  corrected topology keeps all four receivers on vertical walls so the hard/bare axis is CST-y
  (physical vertical). Geometry exploration is closed [src: CUBOID_RESEARCH_QUESTIONS overrides].
- **Solver:** full-wave CST 2025, narrow 0.38–0.43 GHz fast frequency sweep (production); mesh-
  converged vs full-band within ~0.26 dB at 403 MHz [src: CUBOID_RESEARCH_QUESTIONS override
  2026-05-27 narrow-band].
- **Dataset:** combined Phase-1 + Phase-2 dense set, N = 3935 configs, 788 unique positions, 5
  poses/position (identity, z90, y90, y180, x90); 180-D rich feature vector (rssi_head 4,
  mag_multifreq 44, phase_cos 44, phase_sin 44, return_loss 44) [src: rich_unified_benchmark.md;
  Finding - orientation intelligence (5-pose)]. Documented gaps: b56 has a 15-config setup gap;
  b65 = 50 by design [src: rich_unified_benchmark.md].
- **Protocol:** position-grouped GroupKFold, 5 folds × seeds {1,2,3} = 15 fold·seed; train-only
  normalization; CFM-anchored saved test_idx (byte-identical across methods) [src:
  rich_unified_benchmark.md]. Position-grouped CV is the non-negotiable benchmark and is *stricter*
  than the point-wise random splits used by Hasnain/Yoshitake [src: Finding - feature deployability
  ablation honesty flags].
- **Loud caveat:** SIMULATION only; no measured phantom data anywhere in the dataset.

### 3.4 Method
- **Deterministic backbone (point reference).** Rich-feature MSE regression backbone; 3D MAE
  0.340 ± 0.04 cm (x 0.14 / y 0.17 / z 0.18) on N=3935 [src: rich_unified_benchmark.md; Finding -
  orientation intelligence honesty box]. Used as the point-accuracy reference, *not* a posterior
  source.
- **CFM posterior (the method).** Clean conditional flow matching — `--no-ot-cfm --ema-decay 0.999`,
  Euler integration, shared `RawRSSIVectorField` backbone, 200 eval samples/point [src: Finding -
  UQ bake-off calibration]. Lever-isolation note: minibatch OT-CFM on tiny position-grouped batches
  is the failed lever (contaminated CFM 5.27 cm); EMA is NOT the contaminant and is worth ≈0.2 cm +
  better coverage [src: Finding - UQ bake-off calibration; Finding - feature deployability ablation
  EMA ablation].
- **Posterior sampling + credible regions.** M-model × N-noise sampling → empirical posterior;
  marginal-box and Mahalanobis-ellipsoid credible regions at nominal 50/80/90/95% [src: Finding -
  orientation intelligence (5-pose); Uncertainty as the selling angle]. Operating-point /
  selective-rejection framing (defer least-confident fraction) [src: Finding - Operating point at
  50% coverage — note v3-superseded absolute numbers].
- **Orientation marginalization.** Orientation is a *nuisance variable integrated out*, not
  predicted; handled by backbone invariance (per-pose bias <0.05 cm/axis) + posterior width [src:
  Finding - orientation intelligence (5-pose); Finding - orientation-marginal uncertainty].

### 3.5 Baselines
- Deterministic backbone (point ref). Deep ensemble (5 members). MC-dropout (50 samples). MDN-diag
  and MDN-mix2 (200 samples). Split-conformal on the deterministic backbone. PosteriorFlow v1
  (anchor-prior CFM). [src: Finding - UQ bake-off calibration]
- Classical field (10): HistGradientBoosting, ExtraTrees, RandomForest, SVR, NGBoost, KNeighbors,
  MLPRegressor, AdaBoost, Ridge, GPR (fixed kernel, optimizer=None, alpha=1e-2). [src:
  rich_unified_benchmark.md]
- All on the SAME GroupKFold folds, SAME seeds; position-paired bootstrap over 788 unique positions
  for significance [src: rich_unified_benchmark.md].

### 3.6 Results
Each subsection's backing asset is in the ASSET-MAP (§4).

1. **Point accuracy (the table where we tie, not win the field-external race).**
   Clean CFM 0.354 cm [0.34, 0.37] ≈ det-backbone 0.340 cm (tie within seed noise); CFM
   significantly beats all 10 classical methods (every position-paired 95% CI excludes 0; best
   classical = HistGradientBoosting 0.779 cm, paired Δ +0.424 cm [0.405, 0.443]) [src:
   rich_unified_benchmark.md]. Per-axis CFM: y MAE 0.181 cm (was the whole error budget; now
   resolved on corrected geometry) [src: rich_unified_benchmark.md].
2. **UQ bake-off (the calibration headline).** Clean CFM is the only method clearing all three
   criteria — point (0.501 cm on N=1980 rich) + near-nominal own-sample coverage (cov50/90/95
   = 0.766/0.935/0.944) + discrimination (ρ 0.601). Deep ensemble: lowest MAE (0.359) + highest ρ
   (0.705) but *under-covers* (cov90 0.717, low-sample artifact). MDNs over-cover (cov90 ≈0.96–0.97,
   ρ≈0). Conformal calibrated *by construction* (ρ≈0). PosteriorFlow v1 under-covers (cov90 0.785,
   ρ 0.179). [src: Finding - UQ bake-off calibration]
3. **Phase-vs-bandwidth deployability (honest floor).** Phase, not bandwidth, is the lever. Single-
   tone magnitude-only deployable floor (S1): HistGB 1.55 cm / ExtraTrees 1.73 cm; CFM 1.519 cm,
   det 1.62 cm [src: Finding - feature deployability ablation]. Adding phase at one tone (S2) drops
   HistGB to 0.97 cm (−37%); legal MICS-band (402–405 MHz) coherent S3 reaches det 0.50 / CFM
   0.481 cm and matches full-rich; multi-freq magnitude-only (S4) buys ≈nothing [src: Finding -
   feature deployability ablation]. **Honest single-tone number to quote: ~1.5 cm (sim).** Sub-cm
   requires phase-coherent receivers.
4. **Posterior modality / geometric ambiguity.** On the mirror-symmetric old-cuboid array (all
   sensors at y=0), CFM posterior is genuinely bimodal (mirror_capture 0.497, frac_bimodal 0.721,
   BIC gap +26.8, joint cov90 0.946); MDN-mix2 covers but does not split (frac_bimodal 0.0014, BIC
   gap −16.4); ensemble collapses (joint cov90 0.017, mirror_capture 0.000). All three tie on point
   (~2.5 cm 3D — y unobservable by design here). On corrected V4_fix2 the same CFM is unimodal
   (mirror_capture 0.0). Cylinder negative control: y-mirror capture ≈0.02–0.035 (geometry-specific).
   [src: Finding - physics-modality correspondence]
5. **Orientation-marginal uncertainty.** Orientation moves the RF fingerprint more than relocating
   the capsule does (within-position-across-pose spread ratio ~1.17–1.22) [src: Finding -
   orientation intelligence (5-pose)]. Orientation handled by invariance (per-pose bias <0.05 cm/
   axis; y180 does not flip y) [src: Finding - orientation intelligence (5-pose)]. Posterior WIDTH
   tracks orientation-induced point spread: Spearman ρ 0.907/0.891/0.864 (x/y/z) on the single-seed
   N=396 run, ρ 0.748/0.826/0.828 (3D 0.847) on combined 3-seed N=788 [src: Finding -
   orientation-marginal uncertainty; Finding - orientation intelligence (5-pose)]. Marginal
   posterior is 1.2–1.36× wider than pose-conditioned and covers 100% of the per-pose cloud [src:
   Finding - orientation intelligence (5-pose)]. Diagnostic: pose is a 5-way classification (RF
   74.9%, chance 20%); out-of-plane z90/x90 perfectly separable, in-plane y-family
   {identity,y90,y180} RF-degenerate — the orientation-space mirror of the y-position blind spot
   [src: Finding - orientation intelligence (5-pose)].

### 3.7 Discussion
- The contribution is the *phenomenon + faithful representation*: posterior modality tracks
  forward-operator invertibility, and only the generative flow follows the modality the geometry
  dictates [src: Finding - physics-modality correspondence].
- "Uncertainty is more clinically actionable than the marginal point-accuracy advantage at sub-cm
  levels" — pair the (lose-on-point) and (win-on-uncertainty) tables [src: Uncertainty as the
  selling angle].
- Data scaling: point error budges marginally with data, uncertainty quality scales materially
  (ρ_s +28%, AURC −10% on a +58% expansion) — geometry caps point error, data sharpens calibration
  [src: Finding - v4 vs v3 data scaling result; **note: those absolute numbers are v3-cuboid,
  superseded — cite only the *trend*, flagged**].
- Architecture saturation: 11× more CFM params → 19% worse; not an architecture problem [src:
  `wce-cfm/Concepts/Deep CFM regression.html` — confirm the 2.49→2.96 cm / 19% figure in-file
  before quoting].

### 3.8 Limitations + future work
- **SIMULATION ONLY.** No measured-phantom or in-vivo data. Real-data calibration is the named next
  gate (physical companion experiment) [src: Uncertainty as the selling angle; CUBOID_RESEARCH_QUESTIONS
  physical-rig overrides].
- **No y-face receivers** → y-axis observability is geometry-limited on the old geometry; corrected
  geometry resolves it in simulation but the asymmetry remains a hardware reality [src: Finding -
  403 MHz all-model y-axis collapse; y-axis is unobservable].
- **Phase requires phase-coherent receivers** — the sub-cm rich regime is not free on a simple
  single-tone magnitude MICS device; deployable magnitude-only floor ~1.5 cm [src: Finding - feature
  deployability ablation].
- **Only 5 axis-aligned poses** — invariance demonstrated for those 5 only; arbitrary tilt untested;
  the "orientation-marginal" is a 5-sample approximation, not a true SO(3) marginal. Denser-
  orientation sweep is specified [src: Finding - orientation-marginal uncertainty; Finding -
  orientation intelligence (5-pose)].
- **Bootstrap CIs pending** for det-vs-CFM tie and per-subset deployability rows [src: Finding -
  feature deployability ablation PENDING section].
- **No clinician feedback** on the operating-point threshold yet [src: Finding - Operating point at
  50% coverage].

---

## 4. ASSET-MAP — results subsection → backing artifact

| Results subsection | Backing finding / report (cite this file) | Status |
|---|---|---|
| §3.6.1 Point accuracy (CFM vs det vs 10 classical, paired) | `wce-cfm/Findings/Finding - CFM vs all methods (rich 180-D, new geometry).html`; `reports/stage2_y_observability/rich_unified_benchmark.md`; JSON `experiments/rich_benchmark/unified_analysis.json` | **SOLID** (CFM/classical paired CIs exist; det has NO paired CI — preds not saved, reference row only) |
| §3.6.2 UQ bake-off (calibration headline) | `wce-cfm/Findings/Finding - UQ bake-off calibration.html`; JSONs `experiments/uq_bakeoff/cfm_uq_score_20260528_234224.json`, `uq_bakeoff_20260528_212652.json`, `uq_mdn_conformal_20260528_221143.json` | **SOLID** (15/15 folds, validated from raw JSON) |
| §3.6.3 Phase-vs-bandwidth deployability + ~1.5 cm floor | `wce-cfm/Findings/Finding - feature deployability ablation.html`; `experiments/feature_ablation/feature_ablation_trees_latest.json`; `experiments/uq_bakeoff/cfmfix_*.json` | **SOLID** (point/coverage means; **bootstrap CIs NEEDS MAKING**) |
| §3.6.4 Posterior modality / geometric ambiguity | `wce-cfm/Findings/Finding - physics-modality correspondence.html`; JSON `experiments/uq_bakeoff/ambiguous_bakeoff_full_20260529_033119.json` | **SOLID** (full run, validator-confirmed) |
| §3.6.5 Orientation-marginal uncertainty | `wce-cfm/Findings/Finding - orientation-marginal uncertainty.html`; `wce-cfm/Findings/Finding - orientation intelligence (5-pose).html`; JSON `experiments/uq_bakeoff/orientation_uncertainty.json` | **SOLID for the ρ-tracking + invariance claim**; **NEEDS MAKING:** true SO(3) marginal (only 5 poses; denser-orientation sweep spec'd, not run); single-seed for the high-ρ run |
| §3.6.4 y-axis collapse external validation (supporting) | `wce-cfm/Findings/Finding - 403 MHz all-model y-axis collapse.html` | **SOLID** (supervisor blind labels; v3/old geometry) |
| Table I — comparator/SOTA (external) | `wce-cfm/Concepts/WCE comparator audit.html`; `wce-cfm/Concepts/SOTA Comparison Table.html` | **SOLID for audited rows**; Yoshitake 2022 / Salchak / Khan / Hany17 / Oleksy = **PDF read NEEDS MAKING** |
| Discussion — data scaling trend | `wce-cfm/Findings/Finding - v4 vs v3 data scaling result.html` | **TREND SOLID, absolute numbers SUPERSEDED (v3 cuboid)** — cite trend only, flagged |
| Operating-point / selective rejection | `wce-cfm/Findings/Finding - Operating point at 50% coverage.html` | **SUPERSEDED v3 absolute numbers**; **NEEDS MAKING:** recompute operating points on corrected V4_fix2 |
| Fig. — credible-region calibration plots (cov vs nominal) | derived from UQ bake-off JSONs | **NEEDS MAKING** (figure) |
| Fig. — bimodal posterior on mirror-symmetric array | derived from ambiguous-bakeoff JSON | **NEEDS MAKING** (figure) |
| Fig. — phase-vs-bandwidth ablation bar chart | `experiments/feature_ablation/feature_ablation_trees_latest.json` | **NEEDS MAKING** (figure) |
| Fig. — geometry schematic (4 Rx on ±x/±z, bare y) | CST model / `Model/3D/anchorpoints.json` | **NEEDS MAKING** (figure) |
| Architecture-saturation row (Discussion) | `wce-cfm/Concepts/Deep CFM regression.html` | **SOLID file exists**; confirm the 2.49→2.96 cm / 19% figure in-file before quoting |

---

## 5. Comparator / SOTA table (assembled from WCE comparator audit)

> All point-error numbers are as reported by each source. **OURS is full-wave CST simulation.**
> Regime verdicts use the audit's labels: same-regime / near-regime / accuracy-tier-only /
> aspirational / do-not-cite. Source: `wce-cfm/Concepts/WCE comparator audit.html`.

| Work | Sim vs phantom | Frequency | #Sensors | Eval protocol | Point error | Regime verdict |
|---|---|---|---|---:|---|---|
| **THIS WORK (rich, sim)** | **Sim — full-wave CST** | **0.4 GHz MICS narrowband (401–406 MHz)** | **4 (±x/±z faces, no y)** | **Position-grouped 5-fold CV, 3 seeds** | **0.354 cm 3D (rich, phase+multifreq); ~1.5 cm single-tone mag-only floor** | reference |
| Yoshitake 2022 | Sim + EM phantom | 433.92 MHz | 4 (82×82 mm spiral) | No split / no CV, 78 sim + 78 phantom pts | 1.90 cm sim / 2.22 cm phantom | **same-regime** (closest 4-Rx low-freq) — *PDF unverified, do not cite as primary yet* |
| Hasnain 2026 | **Real phantom** (heterogeneous MHP) | 2.45 GHz ISM | 4 wearable | Point-wise random split, 3,300 pts | 1.69 cm 3D RMSE (XGBoost) | **near-regime** (best 4-Rx experimental; band + real-phantom + split differ) |
| Hasnain 2024 | **Real phantom** (ASTM saline) | 2.45 GHz ISM | 4 wearable | Point-wise random split, 11,400 pts | 2.38 cm RMSE (AdaBoost) | **near-regime** |
| Pourhomayoun 2014 | Sim (Monte Carlo, layered) | 406 MHz MICS | 4–16 (4-Rx point shown) | 500 MC runs at varying SNR | ~1.8 cm @ 4-Rx/0 dB (2D); <0.7 cm trajectory @ 16-Rx | **aspirational** (point) / RF-trajectory context (closest freq) |
| Hiyoshi 2019 | Sim only (FDTD) | 433.92 MHz | 5 spiral | No split, pass-rate on 792 pts | <40 mm @ 100%, <8 mm @ 80% | **near-regime** (closest freq) — algorithmic precedent, not accuracy benchmark |
| Nadimi 2014 | Sim (parametric path-loss) | MICS (note mentions MICS; exact sub-band [VERIFY from PDF]) | 5 anchors | 1000 Monte-Carlo trials, RMSE vs CRLB | 1.6 mm RMSE | Bayesian prior art (no empirical coverage) — *novelty-positioning row* |
| Wisanmongkol 2024 | Sim (CST + Laura voxel) | UWB 3.75–4.35 GHz | 7 (best 4 used) | Single split, ~39 samples, K tuned on test | 26.44 mm mean | **accuracy-tier-only** (do NOT call same-regime) |
| Hany 2023 / SPLD-WCL | Sim (parametric path-loss only) | UWB & MICS | 8–48 | path-loss model | 0.21 mm @48Rx; 6.83 mm SPLD-WCL | **do-not-cite-as-comparator** (idealized path-loss, not full-wave) |
| Barbi 2019 | Phantom + **in-vivo porcine** | UWB 3.1–5.1 GHz | 5–13 | 264 phantom grid pts + in-vivo | 0.72 cm 2D phantom / ~0.94 cm 3D in-vivo | **aspirational** (gold-standard physical validation; UWB/many-Rx) |
| Krishnan 2025 | Sim (UWB voxel) | UWB | varied (3 rows) | Chan TDoA | 1–4 mm [VERIFY from PDF] | **accuracy-tier-only** (TDoA, UWB, many Rx) |
| Salchak 2022 | **In-vivo porcine** | 2.45 GHz ISM | ~30 [VERIFY] | [VERIFY] | "<1 cm" [VERIFY from PDF] | **aspirational** (in-vivo) |
| Khan 2018 | Sim (full-wave FDTD+FEM) | [VERIFY] | multi (varies) | bounds + estimator analysis | ~3.4 cm [VERIFY from PDF] | **near-regime** (full-wave sim) |

**Honest regime verdicts (summary):**
- **No same-regime *and* PDF-verified comparator exists yet.** Yoshitake 2022 is the closest
  (4-Rx, 433 MHz, sim+phantom) but its PDF is unread — the single highest-value missing paper.
- **We do not win the point race against real-phantom 4-Rx systems** (Hasnain 2024/2026); we
  declare sim-vs-real + ~6× band difference + stricter protocol in the same sentence wherever the
  numbers appear [src: Finding - feature deployability ablation honesty flags].
- Path-loss-only sub-mm headlines (Hany family) are explicitly *not* comparators; cite as a
  cautionary regime-mismatch example.
- Error×Sensors is a sanity check only, never the headline — project guardrail [src: SOTA
  Comparison Table; Uncertainty as the selling angle].

---

## 6. Reviewer-2 objections + prepared answers

> Frame these as a rebuttal-readiness checklist. Each answer must trace to a cited source.

**O1. "Simulation only — why should I believe any of it?"**
> A: Sim-only is standard practice in this exact subfield (Yoshitake 2022, Wisanmongkol 2024, Ye
> 2014 CRLB, Nadimi 2014, Pourhomayoun 2014, Hiyoshi 2019 are all sim or sim-dominant). We use
> full-wave CST (not parametric path-loss), declare the caveat in the abstract's first sentence,
> and identify a physical-phantom companion as the explicit next gate. Our protocol (position-
> grouped CV) is *stricter* than the random splits these comparators use, so our numbers are
> conservatively measured. [src: WCE comparator audit; Finding - feature deployability ablation]

**O2. "You're not point-SOTA — Hasnain gets 1.69 cm on a real phantom."**
> A: Correct, and we say so in Tier A of the contribution box. We do not claim point-SOTA. The
> contribution is the *first calibrated posterior at this budget* — a different axis no 4-Rx method
> reports. Tier B: the posterior is point-tax-free (CFM 0.354 cm ties det-backbone 0.340 cm and
> beats all 10 classical baselines on the same folds). [src: Uncertainty as the selling angle;
> rich_unified_benchmark.md]

**O3. "Your rich features use phase — not deployable on a single-tone magnitude MICS device."**
> A: We agree and we ran the ablation. We report the honest single-tone magnitude-only deployable
> floor (~1.5 cm, S1) separately from the rich/coherent regime, and we state that phase requires
> phase-coherent receivers. Crucially: the full gain is recoverable inside the *legal* MICS band
> (402–405 MHz, S3 ≈ S5) — bandwidth is not the requirement, coherence is. [src: Finding - feature
> deployability ablation]

**O4. "Nadimi 2014 was already Bayesian — what's new?"**
> A: Nadimi reports RMSE-vs-CRLB on parametric path-loss simulation with *no empirical coverage*.
> Our claim is narrower and verifiable: **first flow-matching/generative posterior** and **first
> with empirical multi-level coverage (50/90/95%) under position-grouped CV** in WCE RF. We also
> show posterior *modality* (bimodality under geometric ambiguity) which a parametric Bayesian
> likelihood does not represent. [src: Nadimi 2014 paper note; Finding - physics-modality
> correspondence]

**O5. "Your calibration is just an over-wide posterior — easy to cover if you're conservative."**
> A: No — we report *discrimination*, not just coverage. The CFM posterior width ranks error at
> Spearman ρ = 0.601 (UQ bake-off) and tracks orientation-induced spread at ρ ≈ 0.85–0.91; methods
> that merely widen (MDN-diag/mix2) get cov90 ≈0.96 but ρ ≈ 0 and are flagged as over-covering.
> Conformal coverage (calibrated by construction, ρ ≈ 0) is explicitly *not* counted as earned. The
> CFM is the only method clearing point + coverage + discrimination together. [src: Finding - UQ
> bake-off calibration; Finding - orientation-marginal uncertainty]

**O6. "CFM ties the deterministic backbone on point accuracy — so why bother with the generative
model?"**
> A: Because the deterministic backbone has *no posterior* — it cannot be calibrated or ranked, and
> it cannot represent the bimodality that the geometry physically dictates. The point tie is the
> *selling point*: you get the calibrated posterior *for free* (no point-accuracy tax). The
> ensemble that beats CFM on raw MAE (0.359) under-covers badly (cov90 0.717) and so is not a usable
> uncertainty estimator. [src: Finding - UQ bake-off calibration; Finding - physics-modality
> correspondence]

---

## 7. Target venue class

> **Realistic NOW (simulation-only paper):**
> - IEEE conference in the EMBC / BodyNets / IEEE Sensors / EuCAP class — consistent with where the
>   sim comparators (Nadimi EMBC 2014, Ito IEICE, Pourhomayoun TBME) published. The project already
>   has a EuCAP 2026 abstract lineage [src: MEMORY EuCAP].
> - Methods/ML-for-health venue that accepts simulation-validated methods contributions where the
>   novelty is the *uncertainty framework*, not clinical validation.
> - Journal tier achievable now: IEEE Access / Sensors (MDPI) / IEEE J-ERM-class — sim-only is
>   accepted in this subfield (Hiyoshi, Wisanmongkol, Hany all sim in these venues).
>
> **AFTER the physical-phantom companion (higher tier):**
> - IEEE TBME / TBioCAS / T-AP / TMI-adjacent — the real-phantom + calibration story is a much
>   stronger journal contribution. Barbi 2019 (TAP, phantom + in-vivo) and Hasnain (real phantom)
>   are the bar.
> - The "calibrated posterior validated on real data under position-grouped CV" claim is the one
>   that unlocks the top-tier venue; flagged as the explicit future-work gate.
>
> **Recommendation:** submit the simulation paper now to a sim-accepting venue with the calibration
> contribution framed per §2; hold the top-tier journal for the physical companion.

---

## Appendix — superseded/caution number register (do NOT cite as current)

- v3 old-cuboid operating-point numbers (CFM 2.48→1.88 cm @50% coverage; CRPS 0.647; ρ +0.498) are
  **v3 cuboid, superseded** — only cite the *relative ordering / trend*, flagged. [src: Finding -
  Operating point at 50% coverage; Finding - v4 vs v3 data scaling result]
- Old flat cuboid CFM 3.31–3.42 cm and XGBoost 2.67 cm are old-geometry/old-feature; superseded by
  corrected V4_fix2. [src: CUBOID_RESEARCH_QUESTIONS overrides]
- MC-dropout NLL and CFM-contaminated rows are DISCARD/control-only. [src: Finding - UQ bake-off
  calibration]
- Smoke "oracle gaps" inside orientation scripts are harness artifacts — do NOT cite. [src: Finding
  - orientation intelligence (5-pose) honesty box]
