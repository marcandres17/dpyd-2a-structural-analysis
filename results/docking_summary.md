# Docking Summary — AutoDock Vina

## Search box

Centered on Cys671 (reference structure coordinates), 20×20×20 Å,
identical for both reference and variant docking runs to ensure both
searches explore the same region of space.

```
center_x = 17.292
center_y = -3.626
center_z = -30.135
```

UniProt annotation (confirmed directly from the Q12882 Feature Viewer)
places the substrate-binding pocket at residues 668–670, immediately
adjacent to the Cys671 active site — within the coverage of this search
box given its size and the residues' proximity.

## Reference structure — binding modes

| Mode | Affinity (kcal/mol) | RMSD l.b. | RMSD u.b. |
|---|---|---|---|
| 1 | −5.4 | 0.000 | 0.000 |
| 2 | −5.2 | 2.523 | 3.042 |
| 3 | −5.2 | 7.017 | 7.636 |
| 4 | −5.1 | 3.157 | 3.529 |
| 5 | −5.1 | 3.169 | 3.863 |
| 6 | −5.0 | 2.568 | 2.950 |
| 7 | −4.8 | 5.008 | 5.382 |
| 8 | −4.8 | 4.602 | 5.293 |
| 9 | −4.8 | 2.515 | 2.866 |

## Variant structure — binding modes

| Mode | Affinity (kcal/mol) | RMSD l.b. | RMSD u.b. |
|---|---|---|---|
| 1 | −4.8 | 0.000 | 0.000 |
| 2 | −4.8 | 10.068 | 10.824 |
| 3 | −4.7 | 1.511 | 2.202 |
| 4 | −4.5 | 10.056 | 10.740 |
| 5 | −4.5 | 10.093 | 10.171 |
| 6 | −4.5 | 9.932 | 10.661 |
| 7 | −4.3 | 10.046 | 10.493 |
| 8 | −4.3 | 2.227 | 2.728 |
| 9 | −4.3 | 3.086 | 3.538 |

## Comparison

| | Reference | Variant | Difference |
|---|---|---|---|
| Best affinity (mode 1) | −5.4 kcal/mol | −4.8 kcal/mol | +0.6 kcal/mol (weaker in variant) |
| Ligand centroid to active site | 5.33 Å | 6.01 Å | +0.68 Å |
| Distance between the two best poses | 8.67 Å | — | — |
| Alternative mode spread | 2.5–7.6 Å from best mode | up to ~10 Å from best mode | notably wider in variant |

## Interpretation

More negative = more favorable binding. The 0.6 kcal/mol difference in
best-mode affinity is directionally consistent with a loss-of-affinity
hypothesis but is small — within the range where Vina's own reported
scoring error (~2–3 kcal/mol relative to experimental data) urges caution
against over-interpreting the magnitude alone.

The more informative signal is the spread among alternative modes: several
variant poses sit ~10 Å from the top mode, versus a comparatively tighter
2.5–7.6 Å spread in the reference. This suggests Vina finds a less
well-defined, less geometrically consistent pocket in the variant — the
ligand still binds near the active site in both cases (5.33 Å reference,
6.01 Å variant), but visual inspection of the top poses (see
`figures/06b_docking_poses_comparison.png`) shows a clearly reoriented
binding geometry in the variant relative to the reference, rather than
simple displacement.

Taken together, this is consistent with a locally distorted binding pocket
that still accommodates the ligand, rather than either (a) no structural
effect at all, or (b) complete exclusion of 5-FU from the active site.
