# Step 1 — Database Exploration

## UniProt entry: Q12882 (DPYD_HUMAN)

| Field | Value |
|---|---|
| Protein name | Dihydropyrimidine dehydrogenase [NADP(+)] |
| Gene | DPYD |
| Organism | Homo sapiens |
| Status | UniProtKB reviewed (Swiss-Prot) |
| Length | 1025 amino acids |
| Protein existence | Evidence at protein level |
| Annotation score | 5/5 |

## Functional annotation (Feature Viewer)

Confirmed directly from UniProt's binding-site and active-site annotations
(all "By Similarity" — inferred from homologous, experimentally
characterized proteins rather than direct experimental evidence in human
DPD):

| Feature | Position(s) | Description |
|---|---|---|
| Binding site | 668–670 | substrate |
| **Active site** | **671** | **Proton acceptor (Cys671)** |
| Binding site | 709 | FMN |
| Binding site | 736–737 | substrate |
| Binding site | 767 | FMN |
| Binding site | 793–795 | FMN |

This confirms and refines what the literature review (Step 2) had already
established: the catalytic residue is Cys671, but the substrate-binding
pocket extends across residues 668–670 as well, immediately upstream of the
catalytic cysteine. The docking search box (centered on Cys671, 20×20×20 Å)
covers this adjacent region by virtue of its size and proximity, but this is
worth stating explicitly for methodological precision.

## Domain annotation

UniProt's domain track (Family & Domains) identifies three 4Fe-4S
ferredoxin-type domains:

| Domain | Position |
|---|---|
| 4Fe-4S ferredoxin-type 1 | 69–100 |
| 4Fe-4S ferredoxin-type 2 | 944–976 |
| 4Fe-4S ferredoxin-type 3 | 978–1007 |

These correspond to the iron-sulfur cluster-binding regions responsible for
electron transfer between DPD's two active sites (the NADPH/FAD site and the
pyrimidine/FMN site), consistent with the two-active-site, ~60 Å-apart
architecture described in the literature (Moran et al.).

## Sequence splicing track

The Feature Viewer's "SEQUENCE SPLICING" track shows alternative splicing
annotation spanning roughly residues 400 to the C-terminus of the protein.
This indicates that the region containing exon 14 (residues 581–635) sits
within a part of DPYD that is broadly subject to alternative splicing at the
genomic level, not an isolated or unusual splice event.

## RCSB-PDB / AlphaFold DB structure entry: AF_AFQ12882F1

| Field | Value |
|---|---|
| Entry type | Computed Structure Model (no experimental structure exists for human DPD) |
| Source | AlphaFold DB |
| Released | 2021-07-01 |
| Last modified | 2025-08-01 |
| Version | v6 (coordinates unchanged from v4; only the version label was updated) |
| Global symmetry | Asymmetric — C1 |
| Global stoichiometry | Monomer — A1 |
| **pLDDT (global)** | **96.14** |

Per-residue confidence distribution (RCSB-PDB display):

| Confidence band | Residues |
|---|---|
| Very high (pLDDT > 90) | 969 |
| Confident (70 < pLDDT ≤ 90) | 43 |
| Low (50 < pLDDT ≤ 70) | 9 |
| Very low (pLDDT ≤ 50) | 4 |

**Conclusion**: no experimental structure of human DPD exists in the PDB.
The reference structure used throughout this project is a computed model,
explicitly labeled as such by RCSB-PDB, with per-residue confidence
verified before use.

## AlphaFold DB (v6, alphafold.ebi.ac.uk) — cross-check

A second confidence summary was retrieved directly from the AlphaFold DB
entry page to confirm the RCSB-PDB figures independently:

| Field | Value |
|---|---|
| Average pLDDT | 96.12 (Very high) |
| Very high | 94.5% |
| High | 4.2% |
| Low | 0.9% |
| Very low | 0.4% |
| Experimental structures in PDB | None |
| Entries in AFDB | 3 |

The two sources (RCSB-PDB and AlphaFold DB) agree closely (96.14 vs. 96.12
average pLDDT), which was used as a sanity check before proceeding.

## Ensembl transcript and exon 14 coordinates

MANE Select transcript: **NM_000110.4 / ENST00000370192.8**

Exon 14 record (Ensembl Exons view):

| Field | Value |
|---|---|
| Exon rank | 14 |
| Exon ID | ENSE00001067066 |
| Genomic start | 97,450,223 |
| Genomic end | 97,450,059 |
| CDS length | 165 nucleotides |

165 nt ÷ 3 = 55 amino acids exactly, consistent with the clinically reported
55-residue truncation caused by DPYD*2A. This nucleotide record was
translated and matched against the UniProt reference sequence to locate the
exact residue range removed (see `analysis/02_variant_mechanism.md` and
`analysis/03_sequence_generation.py`).

## Summary of what this step determined

1. No experimental structure of human DPD exists — AlphaFold DB's computed
   model is the only available 3D structure, and its confidence was
   verified as very high (96.14 average pLDDT) before use as the reference.
2. The catalytic active site (Cys671) and its immediately adjacent
   substrate-binding residues (668–670) were confirmed directly from
   UniProt's own annotation, not assumed from literature alone.
3. The exon 14 genomic coordinates and CDS length were obtained from
   Ensembl and used to precisely locate and remove the 55 affected residues
   from the reference sequence, rather than approximating their position.
