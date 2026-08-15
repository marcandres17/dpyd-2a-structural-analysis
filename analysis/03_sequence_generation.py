#!/usr/bin/env python3
"""
Step 3 — Generate the DPYD*2A variant sequence
=================================================

DPYD*2A (c.1905+1G>A) is a splice-donor SNP that causes skipping of exon 14
(Ensembl exon ENSE00001067066, transcript ENST00000370192.8). This removes
165 nucleotides (55 codons) in-frame from the mature transcript, with no
downstream frameshift.

This script:
    1. Translates the exon 14 nucleotide record (from Ensembl) to confirm
       its length and amino acid sequence.
    2. Locates that 55-aa segment within the UniProt reference sequence.
    3. Removes it to generate the DPYD*2A variant protein sequence.
    4. Writes both sequences to FASTA files for downstream use
       (AlphaFold structure prediction, PyMOL analysis, etc).

Requires: biopython (pip install biopython --break-system-packages)
"""

from Bio.Seq import Seq
from Bio import SeqIO
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "sequences"

# ── Exon 14 nucleotide record (Ensembl, ENSE00001067066) ───────────────────
EXON14_NUCLEOTIDES = (
    "GACATTGTGACAAATGTTTCCCCCAGAATCATCCGGGGAACCACCTCTGGCCCCATGTAT"
    "GGCCCTGGACAAAGCTCCTTTCTGAATATTGAGCTCATCAGTGAGAAAACGGCTGCATAT"
    "TGGTGTCAAAGTGTCACTGAACTAAAGGCTGACTTTCCAGACAAC"
)


def translate_exon14():
    """Translate the exon 14 CDS to confirm the 55-aa segment it encodes."""
    seq = Seq(EXON14_NUCLEOTIDES)
    protein = str(seq.translate())

    assert len(EXON14_NUCLEOTIDES) == 165, (
        f"Expected 165 nt (55 codons), got {len(EXON14_NUCLEOTIDES)}"
    )
    assert len(protein) == 55, f"Expected 55 aa, got {len(protein)}"
    assert "*" not in protein, "Unexpected stop codon in exon 14 translation"

    return protein


def load_reference_sequence():
    """Load the UniProt Q12882 reference FASTA."""
    ref_path = DATA_DIR / "DPYD_reference.fasta"
    record = SeqIO.read(ref_path, "fasta")
    return str(record.seq)


def generate_variant(full_seq, exon14_protein):
    """
    Locate the exon 14 segment within the full reference sequence and
    remove it to produce the DPYD*2A variant sequence.
    """
    idx = full_seq.find(exon14_protein)
    if idx == -1:
        raise ValueError(
            "Exon 14 segment not found in reference sequence — "
            "check that DPYD_reference.fasta matches UniProt Q12882."
        )

    start_1indexed = idx + 1
    end_1indexed = idx + len(exon14_protein)

    variant_seq = full_seq[:idx] + full_seq[idx + len(exon14_protein):]

    return variant_seq, start_1indexed, end_1indexed


def write_fasta(sequence, path, header):
    with open(path, "w") as f:
        f.write(f">{header}\n")
        for i in range(0, len(sequence), 60):
            f.write(sequence[i:i + 60] + "\n")


def main():
    print("=== Step 3: Generating DPYD*2A variant sequence ===\n")

    exon14_protein = translate_exon14()
    print(f"Exon 14 translation ({len(exon14_protein)} aa):")
    print(f"  {exon14_protein}\n")

    full_seq = load_reference_sequence()
    print(f"Reference sequence loaded: {len(full_seq)} aa\n")

    variant_seq, start, end = generate_variant(full_seq, exon14_protein)

    print("Match found:")
    print(f"  Position (1-indexed): residue {start} to {end}")
    print(f"  Reference length:  {len(full_seq)} aa")
    print(f"  Variant length:    {len(variant_seq)} aa")
    print(f"  Difference:        {len(full_seq) - len(variant_seq)} aa "
          f"(expected: 55)\n")

    assert len(full_seq) - len(variant_seq) == 55, "Unexpected length difference"

    variant_path = DATA_DIR / "DPYD_variant.fasta"
    write_fasta(
        variant_seq,
        variant_path,
        header="DPYD_2A_variant|exon14_deleted|UniProt_Q12882_derived"
    )
    print(f"Variant FASTA written to: {variant_path}")


if __name__ == "__main__":
    main()
