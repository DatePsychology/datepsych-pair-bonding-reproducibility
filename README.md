# Promiscuity, Pair Bonding, and the Limits of Genetic Explanations — Reproducibility Materials

**Code, published-statistic reconstructions, source checks, and five figures** accompanying a [methodological review](https://datepsych.substack.com/p/promiscuity-pair-bonding-and-the) of Date Psychology's [“The Meme of Promiscuity and Pair Bonding”](https://datepsychology.com/the-meme-of-promiscuity-and-pair-bonding/) (originally published 2022).

**Scope.** This repository reproduces the figures and a small set of numerical checks from **published, rounded summary statistics**. It is **not** an independent replication using participants' raw data, a new meta-analysis, or a causal estimation of the effect of sexual history on relationship outcomes. The original investigators' raw datasets and model code are not included. Where published numbers come from the companion review's source audit, the linked publication and table/figure are given explicitly.

## Files

| File | Description |
| --- | --- |
| `reproduce_pair_bonding_figures_v1.py` | Single Python script that reads the CSVs, checks key input values, reproduces Figures 1–5, and writes the numerical report. |
| `harden_heritability_inputs.csv` | The **18 h² and c² percentages** displayed in the portion of Harden (2014), Table 1 reproduced by Date Psychology, with original study, phenotype and sex labels. |
| `kahn_london_probit_inputs.csv` | Four published probit coefficients and standard errors, sample sizes, model type, and source-table locations from Kahn & London (1991). |
| `smith_wolfinger_add_health_inputs.csv` | Three exponentiated model estimates from Smith & Wolfinger (2024), Table 4, Model 3, later-marrying sample. |
| `armstrong_orgasm_inputs.csv` | Four percentages reported by Armstrong et al. (2012), Figure 1, separated by event context. |
| `source_claims_audit.csv` | Brief source-to-claim verification ledger for central **non-chart** findings as well as the plotted findings. |
| `reconstruction_results_v1.txt` | Expected numeric summary, including counts, reconstructed intervals, and precision comparisons. |
| `figure_1_causal_paths.png` | **Conceptual, hypothetical** causal-pathway diagram (not an estimate from data). |
| `figure_2_harden_audit.png` | Display of the 18 published h² entries; highlights values outside the claimed 30–60% range. |
| `figure_3_kahn_uncertainty.png` | Four probit point estimates with **approximate normal-theory** 95% intervals calculated from published standard errors. |
| `figure_4_add_health.png` | Published adjusted relative estimates for zero, 1–8, and 9+ approximated premarital nonspousal partners; **no confidence intervals plotted**. |
| `figure_5_armstrong.png` | Published female orgasm percentages by hookup/relationship context. |
| `requirements.txt` | Minimal Python dependencies. |
| `.gitignore` | Ignores transient Python/cache files. |

## Reproduce calculations and charts

Use Python **3.10 or newer**:

```bash
python -m pip install -r requirements.txt
python reproduce_pair_bonding_figures_v1.py
```

This overwrites the five root-level PNGs and `reconstruction_results_v1.txt`. To preserve the checked-in artifacts, choose a separate destination:

```bash
python reproduce_pair_bonding_figures_v1.py --output-dir regenerated
```

The script reads the four CSVs from its own directory and writes images and the results file to the chosen destination. It validates expected input row counts and some central numerical transcriptions before drawing. No network access or primary-study PDFs are needed.

### Expected checkpoints

- Harden: **18** displayed h² estimates; **four below 30%**, **13 between 30% and 60% inclusive**, **one above 60%**; range **0–65%**. For the risky-sexual-behavior row, h² = **34%** and c² = **28%**.
- Kahn & London, first 5 years: ordinary probit **−0.601 (SE 0.078)**; bivariate probit **−0.511 (SE 0.514)**. Approximate intervals are **[−0.754, −0.448]** and **[−1.518, 0.496]**.
- Kahn & London, years 5–10: ordinary probit **−0.402 (SE 0.098)**; bivariate probit **−0.274 (SE 0.842)**. Approximate intervals are **[−0.594, −0.210]** and **[−1.924, 1.376]**.
- Bivariate/ordinary SE ratios: approximately **6.59×** and **8.59×**, respectively.
- Smith & Wolfinger: **1.00 / 1.64 / 3.20** for the three comparison groups in the specified model (later-marrying sample, **N = 3,506**).
- Armstrong: **11% / 16% / 34% / 67%**, in the order shown in the CSV.

These checkpoints are results of transcriptions or elementary arithmetic; they should **not** be treated as newly estimated effects.

## Figure-by-figure methods and limitations

### Figure 1 — Hypothesized causal pathways

An original explanatory diagram of possible links among pre-existing differences, social context, experiences, and later relationship outcomes. The arrows are **hypothetical**; their existence, strength, direction, and relative causal contributions have not been established by the diagram.

### Figure 2 — Harden heritability table audit

The entries are the **18 rows displayed in the image reproduced by the Date Psychology essay**, drawn from Harden's Table 1 (continued). We do not pool or average the entries: the outcomes include partner counts but also sexual attitudes, age at first attempts to conceive, age at first birth, births by age 20, and teenage pregnancy. Treating all of them as interchangeable measures of “promiscuity” would be misleading.

The **53%** entry correctly belongs to **Rodgers et al. (2001), women, age at first proception**; the **21%** entry belongs to **Kirk et al. (2001), women, age at first birth**. These labels were checked against the reproduced original table. h² and c² are different model-estimated variance components; neither is an individual-level percentage of predetermined behavior. Differences between rows do not imply an overall mean effect.

### Figure 3 — Kahn & London (1991) probit reconstruction

For each of two periods (first five years, years 5–10), the script uses the reported coefficient and standard error for **virgin at marriage relative to not virgin**. It computes an **approximate normal 95% interval** by coefficient ± 1.96 × SE. The ordinary-probit estimates are from Table 3, Models 3 and 6; the bivariate-probit estimates are from Table 4. The coefficient scale is **probit, not percent difference, risk ratio, or divorce probability**.

The loss of significance in the bivariate models is driven largely by the greatly increased standard errors, not a point estimate near zero. The model-based adjustment depends on assumptions about unobserved selection and distributional form. The residual-error correlations reported by Kahn & London (−0.054 and −0.079) were statistically nonsignificant. Neither significance loss nor those estimates establishes selection as the true causal explanation or proves a causal sexual-experience effect. The study concerns **virginity at marriage among historical cohorts of U.S. women**, not cumulative partner count.

### Figure 4 — Smith & Wolfinger (2024), Add Health

These are **exponentiated coefficients from the fully adjusted Table 4 Model 3**, not individual probabilities of divorce. The paper labels them odds ratios; the event-history model uses a complementary log-log specification, so its interpretation requires care. The chart **does not plot uncertainty intervals** and should not be read as an inference about the precision of differences among groups.

The later-marrying sample (N = 3,506) uses an **approximate** count of premarital **nonspousal** partners up to Wave III, with one possible eventual spouse subtracted. The 0 / 1–8 / 9+ thresholds were informed by exploratory model comparisons. The estimates are observational associations conditional on sample inclusion and covariates, **not causal effects**. Divorce is not a direct assay of neurological attachment capacity.

### Figure 5 — Armstrong, England & Fogarty (2012)

Percentages describe women's **reported orgasms in sexual events** across first hookups, second or third hookups, later hookups with the same partner, and relationship sex in a college sample. They are **not** percentages of women, cannot be generalized without qualification to all casual sex, and do not measure oxytocin-induced bonding or its permanence.

## Selected primary sources

- [Date Psychology (2022), “The Meme of Promiscuity and Pair Bonding”](https://datepsychology.com/the-meme-of-promiscuity-and-pair-bonding/).
- [Harden (2014), *Genetic Influences on Adolescent Sexual Behavior*, Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC3893311/).
- [Kahn & London (1991), *Premarital Sex and the Risk of Divorce*, Tables 3–4](https://doi.org/10.2307/352992).
- [Smith & Wolfinger (2024), *Re-Examining the Link Between Premarital Sex and Divorce*, Table 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC10989935/).
- [Armstrong, England & Fogarty (2012), *Accounting for Women's Orgasm and Sexual Enjoyment in College Hookups and Relationships*, Figure 1](https://doi.org/10.1177/0003122412445802).
- [Cherkas et al. (2004), *Genetic Influences on Female Infidelity and Number of Sexual Partners in Humans*](https://doi.org/10.1375/twin.7.6.649).
- [Eisenberg et al. (2010), *Assortative Human Pair-Bonding for Partner Ancestry and Allelic Variation of DRD4*](https://doi.org/10.1093/scan/nsp026).
- [Horwitz et al. (2016), *Understanding the Role of Mate Selection Processes in Couples' Pair-Bonding Behavior*](https://doi.org/10.1007/s10519-015-9766-y).
- [Williams et al. (1994), *Oxytocin Administered Centrally Facilitates Formation of a Partner Preference in Female Prairie Voles*](https://doi.org/10.1111/j.1365-2826.1994.tb00579.x).

See `source_claims_audit.csv` for additional checks and links. The companion article has the longer reference list and context.

## What this repository does **not** reproduce

- Raw-data analyses, weighting, imputation, model selection, or statistical code of any cited research team.
- Confidence intervals not reported or derived in the companion article (notably **no invented Add Health intervals**).
- A causal effect of sexual history on later attachment, divorce, infidelity, or neurological systems.
- A numerical decomposition of genetic selection versus experience or other confounding.
- Every qualitative assertion in the accompanying long-form essay; the `source_claims_audit.csv` is a concise claim ledger, not a comprehensive systematic review.

The full Kahn & London and Horwitz papers were accessed for the companion audit, but **their copyrighted PDFs are not redistributed**. Likewise, no original webpages, images copied from the papers, or participant-level data are included. The five PNGs were drawn specifically for the companion review from transcribed statistics or original conceptual artwork.

## Reproducibility note

On the preparation environment, the standalone script regenerated **all five published images pixel-for-pixel identically** to the verified article figure files. Other Python/matplotlib versions or operating systems may produce minor differences in font rendering or pixel positions without affecting the numbers or interpretation.
