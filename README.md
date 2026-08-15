# Structural Impact of DPYD*2A on Dihydropyrimidine Dehydrogenase and Its Relevance to 5-Fluorouracil Toxicity

A structural bioinformatics project investigating whether a clinically
established loss-of-function splice-site variant in *DPYD* produces a
detectable structural signature in the predicted protein, and whether that
signature is consistent with the drug-binding defect underlying
fluoropyrimidine toxicity in cancer patients.

## Research question

How does the DPYD*2A variant (c.1905+1G>A, rs3918290) — a splice-site SNP
that causes skipping of exon 14 and loss of 55 amino acids — affect the
three-dimensional structure of dihydropyrimidine dehydrogenase (DPD), and is
that structural change consistent with the severe 5-fluorouracil (5-FU)
toxicity documented in clinical practice?

## Why this matters

DPD catalyzes the rate-limiting step in pyrimidine catabolism and inactivates
80–90% of administered 5-FU. Patients carrying a non-functional *DPYD*
allele such as *2A metabolize 5-FU poorly, leading to drug accumulation and
severe, sometimes fatal, toxicity. Current CPIC guidelines recommend a 50%
starting-dose reduction for intermediate metabolizers and complete avoidance
of fluoropyrimidines for poor metabolizers. Genotype-guided dosing has been
shown to reduce hospitalization rates among variant carriers from 64% to 25%
without compromising antitumor efficacy. The FDA strengthened DPD-deficiency
warnings on all 5-FU labels in 2024, and added a boxed warning to
capecitabine labels in October 2025 requiring *DPYD* testing before
treatment — this is an area of active, current clinical relevance, not a
settled historical topic.

## Project design

This project follows the classical structural proteomics workflow (database
exploration → sequence alignment → visualization → structural superposition
→ modeling → docking), unified under a single research question rather than
run as disconnected exercises. Four independent lines of computational
evidence were generated and compared:

| Step | Method | What it measures |
|---|---|---|
| 1 | UniProt / RCSB-PDB / AlphaFold DB exploration | Existing structural and functional annotation |
| 2 | Literature and PharmGKB/CPIC review | Precise molecular mechanism of the variant |
| 3 | Sequence engineering + pairwise alignment | Exact residues removed by exon 14 skipping |
| 4 | AlphaFold Server (5 independent models) | Per-residue prediction confidence (pLDDT) |
| 5 | PyMOL structural superposition | Global and zone-specific RMSD |
| 6 | 3D distance measurement | Spatial proximity of the affected region to the active site |
| 7 | AutoDock Vina docking | Predicted binding affinity and pose for 5-FU |

## Key findings

- The reference protein (AlphaFold DB, Q12882) shows very high confidence
  (average pLDDT 96.14) across the entire structure, including uniformly
  high confidence (>93) in the region spanning the exon 14 boundary.
- Across 5 independently generated AlphaFold3 models of the variant protein,
  pLDDT consistently and reproducibly drops to ~42–50 in the residues
  immediately flanking the artificial junction created by exon skipping —
  a signal absent from the reference.
- Zone-specific RMSD confirms the distortion is highly localized: 6.670 Å
  in the affected region (residues 570–600) versus 0.338 Å across the rest
  of the protein, meaning the deletion does not destabilize the global fold.
- The affected region comes within 9.71 Å (3D space, not linear sequence)
  of the catalytic active site (Cys671), a distance close enough to
  plausibly interfere with the mobile catalytic loop (Ser670–Cys671–His673)
  described in the literature.
- Docking with AutoDock Vina shows 5-FU still binds near the active site in
  both structures (5.33 Å reference, 6.01 Å variant), but with modestly
  reduced affinity in the variant (−4.8 vs. −5.4 kcal/mol), a reoriented
  binding pose, and substantially greater dispersion among alternative
  binding modes — consistent with a locally distorted, less well-defined
  binding pocket rather than complete exclusion of the ligand.

The full interpretation, including an honest discussion of what this
analysis does and does not demonstrate, is in
[`results/07_discussion.md`](results/07_discussion.md).

## Repository structure

```
dpyd-project/
├── README.md                          # this file
├── requirements.txt
├── data/
│   ├── sequences/
│   │   ├── DPYD_reference.fasta        # UniProt Q12882, 1025 aa
│   │   ├── DPYD_variant.fasta          # exon 14 removed, 970 aa
│   │   └── exon14_nucleotide.txt       # Ensembl exon record used for the deletion
│   └── structures/
│       ├── DPYD_reference.pdb          # AlphaFold DB, model v4/v6
│       ├── DPYD_variant_model_0-4.cif  # 5 AlphaFold Server models
│       └── DPYD_variant_aligned.pdb    # variant, superposed onto reference frame
├── analysis/
│   ├── 01_database_exploration.md
│   ├── 02_variant_mechanism.md
│   ├── 03_sequence_generation.py
│   ├── analyze_plddt.py                # per-residue pLDDT, .cif files
│   ├── analyze_plddt_pdb.py            # per-residue pLDDT, .pdb files
│   ├── 05_superposition.pml
│   ├── 05b_zone_rmsd.pml
│   ├── 06_active_site_distance.pml
│   ├── 06b_docking_visualization.pml
│   ├── prepare_docking.sh              # ligand/receptor prep + Vina configs
│   └── config_reference.txt / config_variant.txt
├── figures/
│   ├── 05_superposition.png
│   ├── 05b_zone_comparison.png
│   ├── 06_active_site_proximity.png
│   └── 06b_docking_poses_comparison.png
└── results/
    ├── 01_database_exploration.md
    ├── plddt_comparison_table.md       # 5-model comparison, model selection rationale
    ├── rmsd_summary.md
    ├── docking_summary.md
    └── 07_discussion.md                # full final discussion
```

## Reproducing this analysis

### Environment

```bash
conda create -n proteomics python=3.10 -y
conda activate proteomics
conda install -c conda-forge -c bioconda -c schrodinger \
    biopython pymol-open-source autodock-vina openbabel -y
```

### Steps

1. Database exploration and variant mechanism research —
   see `analysis/01_database_exploration.md` and `analysis/02_variant_mechanism.md`.
2. Generate the variant sequence: `python analysis/03_sequence_generation.py`
3. Predict structures: reference downloaded from AlphaFold DB; variant
   predicted via [AlphaFold Server](https://alphafoldserver.com) (5 models).
4. Select the best model by zone-specific pLDDT (not global ranking_score):
   `python analysis/analyze_plddt.py data/structures/*.cif`
5. Superposition and zone RMSD: `pymol -cq analysis/05_superposition.pml`
   then `pymol -cq analysis/05b_zone_rmsd.pml`
   (this also produces the aligned variant structure needed by every
   later step)
6. Active-site distance: `pymol -cq analysis/06_active_site_distance.pml`
7. Docking: `bash analysis/prepare_docking.sh` then
   `vina --config analysis/config_reference.txt` and
   `vina --config analysis/config_variant.txt`
8. Docking pose visualization: `pymol -cq analysis/06b_docking_visualization.pml`

Note: this project does not include a standalone Step 4 visualization
script — the reference and variant structures are first rendered together
as part of the Step 5 superposition (`05_superposition.pml`), which is
where `figures/05_superposition.png` comes from.

## Limitations

- Neither structure includes DPD's required cofactors (FAD, FMN, four
  Fe₄S₄ clusters); the evaluated binding pocket may not fully represent the
  geometry of the catalytically activated enzyme.
- AutoDock Vina performs rigid-receptor docking; it does not model side-chain
  flexibility, which is particularly relevant given that the active site
  sits on a documented mobile loop.
- AlphaFold predicts a single static conformation and does not capture real
  conformational dynamics.
- The dominant clinical mechanism of DPYD*2A likely involves degradation of
  the aberrant transcript (nonsense-mediated decay) rather than — or in
  addition to — a stably folded, truncated protein with altered ligand
  binding. This project models the latter, more limited scenario.
- AlphaFold Server's output terms of use specify non-commercial use and
  advise against use in docking or screening tools; this project uses the
  predicted structures purely for educational, non-commercial structural
  comparison, and that constraint is noted here explicitly.

## Tools used

UniProt, RCSB-PDB, AlphaFold DB, AlphaFold Server, Biopython, PyMOL
(open-source), AutoDock Vina, Open Babel.

---

*This project was developed with the assistance of Claude Code.*
