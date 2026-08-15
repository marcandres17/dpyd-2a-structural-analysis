# Step 2 — Variant Mechanism: DPYD*2A

## Formal identification

| Field | Value |
|---|---|
| Star allele name | DPYD*2A |
| HGVS coding notation | c.1905+1G>A |
| dbSNP ID | rs3918290 |
| Type | Single Nucleotide Polymorphism (SNP) |
| Location | Splice donor site, intron 14 |

## Why "SNP" needs qualification

DPYD*2A is, at the nucleotide level, a single base substitution (G>A) — in
that strict sense it is correctly described as a SNP. However, its location
is critical: the change falls in an intronic splice donor site, one
nucleotide after the boundary of coding exon 14, not within any exon. It
does not change a codon or substitute one amino acid for another.

## Mechanism

1. The G>A substitution disrupts the canonical splice donor sequence at the
   intron 14 boundary.
2. This causes the spliceosome to skip exon 14 entirely during pre-mRNA
   processing.
3. Skipping exon 14 removes 165 nucleotides (a precise multiple of 3) from
   the mature transcript, corresponding to exactly 55 amino acids from the
   translated protein.
4. Because 165 is evenly divisible by 3, the reading frame downstream of
   the deletion is preserved (no frameshift, no premature stop codon
   introduced elsewhere) — the protein is shortened by exactly one clean
   in-frame segment rather than being scrambled downstream.
5. The resulting protein is reported in the literature as catalytically
   inactive.

## Consequence for this project's design

Because the variant removes an entire in-frame segment rather than
substituting a single residue, the correct way to model it computationally
is not to change one letter in the reference FASTA — it is to **delete the
55 corresponding residues entirely** from the sequence before structure
prediction. This is what `analysis/03_sequence_generation.py` does, using
the exon 14 boundaries located via Ensembl (see
`analysis/01_database_exploration.md`).

## Verified deletion coordinates

| | Reference (Q12882) |
|---|---|
| Exon 14 protein segment | `DIVTNVSPRIIRGTTSGPMYGPGQSSFLNIELISEKTAAYWCQSVTELKADFPDN` |
| Start (1-indexed) | residue 581 |
| End (1-indexed) | residue 635 |
| Length | 55 amino acids |
| Reference protein length | 1025 aa |
| Variant protein length (after deletion) | 970 aa |

## References

- Original variant characterization and clinical consequence: literature
  and CPIC/PharmGKB dosing guidelines (see `results/07_discussion.md` for
  full clinical context and citations).
- Exon coordinates: Ensembl, transcript ENST00000370192.8 (MANE Select),
  exon ENSE00001067066.
