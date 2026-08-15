# RMSD Summary

## Global superposition (reference vs. variant, model_2)

```
Match: assigning 970 x 1025 pairwise scores.
MatchAlign: aligning residues (970 vs 1025)...
ExecutiveAlign: 7381 atoms aligned.
ExecutiveRMS: 180 atoms rejected during cycle 1 (RMSD=2.36).
ExecutiveRMS: 342 atoms rejected during cycle 2 (RMSD=0.73).
ExecutiveRMS: 324 atoms rejected during cycle 3 (RMSD=0.44).
ExecutiveRMS: 168 atoms rejected during cycle 4 (RMSD=0.38).
ExecutiveRMS: 73 atoms rejected during cycle 5 (RMSD=0.36).
Executive: RMSD = 0.354 (6294 to 6294 atoms)
```

PyMOL's `align` command performs iterative outlier rejection: it aligns,
computes RMSD, discards the worst-fitting atoms, and repeats. The first
cycle's high RMSD (2.36 Å, 180 rejected atoms) is the signature of a
localized region that fits poorly — investigated directly below.

## Zone-specific RMSD

| Region | RMSD | Atoms used |
|---|---|---|
| **Critical zone** (570-600) | **6.670 Å** | 11 |
| **Rest of protein** (excluding 570-600) | **0.338 Å** | 848 |
| Global (unseparated) | 0.354 Å | 6294 |

Note: the critical-zone alignment used only 11 of the 31 originally
selected atoms — PyMOL's sequence-matching step discarded the rest as
unreliably paired between the two sequences within such a short, heavily
altered selection. This small sample size means the 6.670 Å figure should
be read directionally rather than treated as a highly precise estimate,
but it is consistent with the other three independent lines of evidence
(pLDDT, 3D distance, and docking).

## Interpretation

Nearly a 20-fold difference between the critical zone and the rest of the
protein confirms, quantitatively, what the pLDDT analysis suggested
indirectly: exon 14 deletion does not destabilize the global fold of DPYD.
The rest of the structure remains essentially superimposable on the
reference (0.338 Å — well within the range considered structurally
identical). The distortion is real, but tightly localized to the
artificial junction created by the deletion.

## Active-site distance (3D, not linear sequence)

| Measurement | Value |
|---|---|
| Cys671 (reference) to residue 600 (point measurement) | not used — see minimum below |
| Cys671 (reference) to closest atom in critical zone (Thr575, minimum) | **9.71 Å** |
| Cys671 (reference) to Cys616 (variant, aligned) — same catalytic residue in both structures | 3.13 Å |

Despite being 36 residues apart in linear sequence, the critical zone comes
within 9.71 Å of the catalytic active site in 3D space — close enough to
plausibly interfere with the geometry of the mobile catalytic loop
(Ser670–Cys671–His673) without making direct contact. The 3.13 Å distance
between the same catalytic residue in both structures (once properly
aligned to a shared coordinate frame) confirms the active site itself is
not directly distorted — consistent with its position outside the
high-RMSD zone.
