# Step 7 — Final Discussion

## Research question recap

How does the DPYD*2A loss-of-function variant (c.1905+1G>A, rs3918290)
structurally alter dihydropyrimidine dehydrogenase (DPYD), and is that
structural change consistent with the severe 5-fluorouracil (5-FU)
toxicity described in clinical practice?

## The four lines of evidence

This project combined four independent computational analyses, each drawing
on a distinct source of evidence, to address the question:

| # | Analysis | Result | What it measures |
|---|----------|--------|-------------------|
| 1 | Per-residue pLDDT (5 AF3 models) | Drop from 98→42-50 at positions 574-579 in the variant; reference maintains >93 across the same zone | AlphaFold's confidence — absence of an evolutionary template for the artificial junction |
| 2 | Zone-specific RMSD | 6.670 Å in zone 570-600 vs. 0.338 Å across the rest of the protein | Localized vs. global conformational distortion |
| 3 | 3D active-site distance | 9.71 Å between the closest point of the critical zone (Thr575) and Cys671 | Real spatial proximity, not linear sequence distance |
| 4 | AutoDock Vina docking | −5.4 (ref.) vs. −4.8 kcal/mol (var.); wider spread among alternative modes; reoriented pose | Functional consequence on ligand binding |

None of these four lines of evidence would be conclusive alone. Together,
they form an internally consistent picture: exon 14 deletion introduces a
real, variant-specific structural distortion, localized to a region close
enough to the catalytic site to plausibly influence its geometry — without
producing global structural collapse or complete exclusion of the ligand.

## Biological interpretation

The most important finding here is not "the variant breaks the protein" —
the data do not support that. It is more precise: **the rest of the
protein, outside the deletion junction, retains essentially the same fold
as the reference** (RMSD 0.338 Å). The detected structural impact is
concentrated almost entirely at the artificial junction created by the
absence of the 55 exon-14 residues, and extends far enough in space (9.71
Å) to approach the mobile catalytic loop (Ser670–Cys671–His673) described
in the literature as responsible for positioning the active site and
gating access to the FMN cofactor during catalysis.

UniProt's own binding-site annotation for Q12882 (Feature Viewer,
confirmed directly rather than assumed from literature) places the
substrate-binding pocket at residues 668–670, immediately adjacent to the
Cys671 catalytic residue (annotated "Proton acceptor"), with additional
FMN-binding residues further downstream (709, 767, 793–795). The docking
search box, centered on Cys671, covers this adjacent pocket by virtue of
its size and the residues' proximity — worth stating explicitly as a
methodological detail rather than leaving implicit.

Docking suggests this local distortion does not prevent 5-FU from binding
near the active site, but does appear to affect the quality of that
binding: slightly reduced affinity, a reoriented pose, and greater
uncertainty in Vina's search (reflected in the spread among alternative
modes). This is a modest difference in magnitude — not dramatic — and
should be presented as such.

## Clinical context: why this matters beyond the computer

DPD catalyzes the initial, rate-limiting step in pyrimidine catabolism and
inactivates 80–90% of administered 5-fluorouracil. Individuals carrying at
least one copy of a non-functional DPYD variant — such as DPYD*2A
(c.1905+1G>A), the variant studied here — have reduced or absent enzyme
activity, leading to toxic drug accumulation rather than normal clearance.

Current clinical guidelines (CPIC, Dutch Pharmacogenetics Working Group)
translate DPYD genotype into an "activity score": intermediate metabolizers
(activity score 1–1.5, typically heterozygous for a null-function variant
like *2A) receive a 50% starting-dose reduction, while poor metabolizers
(activity score 0–0.5) should avoid fluoropyrimidines entirely. This
genotype-guided dosing is not a minor adjustment — a multicenter
implementation report found hospitalization among variant carriers fell
from 64% to 25% with genotype-guided dosing, without compromising
antitumor efficacy.

This is not a topic of purely historical or academic relevance: the FDA
updated all 5-FU product labels in 2024 to highlight DPD-deficiency risk,
and in October 2025 updated capecitabine labels to a boxed warning
explicitly requiring DPYD testing before treatment. Pre-treatment DPYD
genotyping is already standard of care recommended by ESMO in Europe and
increasingly required by regulators in the United States.

## What this analysis does and does not show

**What this analysis DOES show**: a localized structural distortion,
reproducible across 5 independent AlphaFold3 predictions, geometrically
close to the catalytic site, with a measurable — though modest —
consequence on 5-FU binding affinity and pose as predicted by docking.

**What this analysis does NOT show**: that this is the dominant mechanism
of DPYD*2A's clinical toxicity. The literature indicates that c.1905+1G>A
acts by disrupting a splice site, which in a real cell likely results in
degradation of the aberrant transcript via nonsense-mediated decay, or in
a truncated protein that never folds or assembles functionally with its
cofactors (FAD, FMN, Fe₄S₄ clusters — entirely absent from the AlphaFold
structures used here). This project models a more limited, more optimistic
scenario: it assumes the truncated protein manages to fold stably
(supported by the high pLDDT across the rest of the sequence) and asks
what would happen to its substrate-binding capacity in that case. It is
one piece of the mechanism, not a complete reconstruction of why DPYD*2A
causes clinical toxicity.

## Methodological limitations

- **Absence of cofactors**: neither the reference nor the variant
  structure includes FAD, FMN, or the Fe₄S₄ clusters required for DPD's
  real catalytic activity. The evaluated binding pocket may not fully
  reflect the geometry of the catalytically activated enzyme.
- **Rigid-receptor docking**: AutoDock Vina does not model receptor
  side-chain flexibility during the search, a relevant simplification
  given that the active site itself depends on a documented mobile loop.
- **Static structures**: AlphaFold predicts a single conformation; it does
  not capture the real conformational dynamics of the protein in
  solution, particularly relevant for an active site known to oscillate
  between "open" and "closed" states.
- **Small sample size in the critical zone**: the zone RMSD calculation
  relied on a reduced number of atoms after the alignment algorithm's
  filtering (11 of 31 originally selected), limiting the statistical
  robustness of that specific value, though it is consistent with the
  other three lines of evidence.
- **A single allele modeled**: the analysis represents the effect of one
  copy of the variant at the isolated-protein level; it does not model the
  compound heterozygous/homozygous phenotype that determines a patient's
  actual clinical classification (intermediate vs. poor metabolizer).
- **AF3 model selection**: of the 5 models generated by AlphaFold Server,
  the one with the best confidence specifically in the critical zone
  (model_2) was used, not the one with the best global ranking_score — a
  reasoned but somewhat subjective methodological decision.
- **Terms of use**: AlphaFold Server's output terms specify non-commercial
  use and advise against use in docking or screening tools. This project
  uses the predicted structures purely for educational, non-commercial
  structural comparison; that constraint is noted here explicitly.

## Conclusion

The four structural analyses performed — prediction confidence,
conformational deviation, geometric proximity to the active site, and
molecular docking — converge consistently on a real, though localized and
modest, structural impact associated with exon 14 deletion in DPYD*2A.
This computational finding is compatible with the clinically documented
reduction in enzyme activity for this variant, though it likely represents
only part of the complete loss-of-function mechanism, which in clinical
practice also involves transcript-level processes (NMD-mediated
degradation) not captured by this type of structural analysis.
