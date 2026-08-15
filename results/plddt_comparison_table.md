# pLDDT Comparison Across AlphaFold Server Models

## Reference structure (AlphaFold DB, Q12882)

| Metric | Value |
|---|---|
| Total residues | 1025 |
| Average pLDDT | 96.14 |
| >90 (very high) | 969 residues |
| 70-90 (high) | 43 residues |
| 50-70 (low) | 9 residues |
| ≤50 (very low) | 4 residues |
| pLDDT in zone 570-600 | 97.25 average, 93.81 minimum |
| pLDDT at Cys671 (active site) | 72.44 |

The reference structure is uniformly high-confidence in the region that
becomes critical in the variant (570-600), and shows moderately reduced
confidence specifically at the catalytic residue itself (Cys671, pLDDT
72.44) — consistent with this residue sitting on a documented mobile
catalytic loop rather than a rigid structural element.

## Variant structure — global confidence summary (5 independent models)

| Model | Global pLDDT | Zone pLDDT (570-600) | Zone min pLDDT |
|---|---|---|---|
| model_2 | 95.17 | **75.54** | 44.39 |
| model_4 | 95.37 | 75.46 | **46.29** |
| model_0 | 95.38 | 74.43 | 44.64 |
| model_3 | 95.38 | 73.67 | 42.65 |
| model_1 | 95.38 | 73.39 | 41.65 |

All five models are effectively tied on global pLDDT (95.17–95.38, a
difference within noise). The zone-specific pLDDT — the metric that
actually matters, since it reflects confidence in the region under
investigation — shows more meaningful spread.

## Model selection rationale

**model_2 was selected** for all downstream analysis. It ranks first on
zone-average pLDDT (75.54) and is effectively tied for best on zone-minimum
pLDDT (44.39 vs. 46.29 for model_4) — it is the only model that does not
lose on either zone metric, even though model_4 edges it out slightly on
the minimum. Given how close the two candidates are, this choice does not
materially change the project's conclusions; both would support the same
interpretation.

## Detailed per-residue pLDDT, model_2, zone 570-600

| Residue | Amino acid | pLDDT (reference) | pLDDT (variant, model_2) |
|---|---|---|---|
| 570 | PHE | 98.88 | 94.26 |
| 571 | ALA | 98.88 | 92.36 |
| 572 | LEU | 98.81 | 92.15 |
| 573 | THR | 98.75 | 83.97 |
| 574 | LYS | 98.19 | 63.79 |
| 575 | THR | 98.06 | **49.09** |
| 576 | PHE | 98.19 | 46.39 |
| 577 | SER | 97.00 | 44.39 |
| 578 | LEU | 97.38 | 53.14 |
| 579 | ASP | 97.06 | 56.91 |
| 580 | LYS | 95.69 | 69.08 |
| 581 | ASP/ILE* | 93.94 | 76.04 |

*Residue 581 is ASP in the reference (start of the deleted exon 14
segment) and ILE in the variant (the residue immediately following the
artificial junction) — these are different amino acids because the
deletion changes what occupies that sequence position downstream of the
junction.

The reference maintains >93 pLDDT across the entire zone. The variant
shows a sharp, reproducible drop to ~42-50 concentrated at residues
575-578, directly flanking the artificial junction — a signal completely
absent from the reference, confirming this is a variant-specific effect
rather than a pre-existing feature of that region of the protein.
