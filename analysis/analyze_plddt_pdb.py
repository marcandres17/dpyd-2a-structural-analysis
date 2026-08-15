#!/usr/bin/env python3
"""
Per-residue pLDDT analysis for AlphaFold DB PDB files
========================================================

Same purpose as analyze_plddt.py, but adapted for the .pdb format
(as opposed to .cif). AlphaFold DB stores pLDDT in the B-factor
column of the standard PDB ATOM records, in a fixed-width format
rather than the whitespace-separated columns used in mmCIF.

Usage:
    python3 analyze_plddt_pdb.py DPYD_reference.pdb
"""

import argparse
from pathlib import Path


def parse_pdb_plddt(filepath):
    """
    Parses a standard PDB file (AlphaFold DB format) and returns
    a dictionary {residue_number: pLDDT} using each residue's CA atom.

    PDB ATOM record fixed-width columns (0-indexed):
        columns 0-5:   record name ("ATOM  ")
        columns 12-15: atom name
        columns 17-19: residue name
        columns 22-25: residue sequence number
        columns 60-65: B-factor (pLDDT, for AlphaFold models)
    """
    residue_plddt = {}
    residue_name = {}

    with open(filepath) as f:
        for line in f:
            if not line.startswith("ATOM"):
                continue

            atom_name = line[12:16].strip()
            comp_id = line[17:20].strip()
            auth_seq_id = int(line[22:26].strip())
            b_factor = float(line[60:66].strip())

            if atom_name == "CA":
                residue_plddt[auth_seq_id] = b_factor
                residue_name[auth_seq_id] = comp_id

    return residue_plddt, residue_name


def summarize_global(residue_plddt, label=""):
    values = list(residue_plddt.values())
    avg = sum(values) / len(values)

    very_high = sum(1 for v in values if v > 90)
    high = sum(1 for v in values if 70 < v <= 90)
    low = sum(1 for v in values if 50 < v <= 70)
    very_low = sum(1 for v in values if v <= 50)

    print(f"\n{'='*60}")
    print(f"GLOBAL SUMMARY {label}")
    print(f"{'='*60}")
    print(f"Total residues:        {len(residue_plddt)}")
    print(f"Average pLDDT:         {avg:.2f}")
    print(f"  >90  (very high):    {very_high} residues")
    print(f"  70-90 (high):        {high} residues")
    print(f"  50-70 (low):         {low} residues")
    print(f"  <=50 (very low):     {very_low} residues")

    return avg


def analyze_critical_zone(residue_plddt, residue_name, zone_start, zone_end,
                           highlight_positions=None, label=""):
    highlight_positions = highlight_positions or []

    print(f"\n{'-'*60}")
    print(f"CRITICAL ZONE {label}: residues {zone_start}-{zone_end}")
    print(f"{'-'*60}")
    print(f"{'Residue':<10}{'Amino acid':<15}{'pLDDT':<10}")

    zone_values = []
    for res_num in sorted(residue_plddt.keys()):
        if zone_start <= res_num <= zone_end:
            plddt = residue_plddt[res_num]
            zone_values.append(plddt)
            marker = " <-- position of interest" if res_num in highlight_positions else ""
            print(f"{res_num:<10}{residue_name[res_num]:<15}{plddt:<10.2f}{marker}")

    if zone_values:
        avg_zone = sum(zone_values) / len(zone_values)
        min_zone = min(zone_values)
        print(f"\nAverage pLDDT in zone:  {avg_zone:.2f}")
        print(f"Minimum pLDDT in zone:  {min_zone:.2f}")
        return avg_zone, min_zone
    return None, None


def main():
    parser = argparse.ArgumentParser(
        description="Analyzes per-residue pLDDT from AlphaFold DB PDB files"
    )
    parser.add_argument("pdb_file", type=Path)
    parser.add_argument("--zone-start", type=int, default=570)
    parser.add_argument("--zone-end", type=int, default=600)
    parser.add_argument("--highlight", type=int, nargs="*", default=[575, 580, 581, 671])
    args = parser.parse_args()

    residue_plddt, residue_name = parse_pdb_plddt(args.pdb_file)
    summarize_global(residue_plddt, label=f"— {args.pdb_file.stem}")
    analyze_critical_zone(
        residue_plddt, residue_name,
        args.zone_start, args.zone_end,
        highlight_positions=args.highlight,
        label=f"— {args.pdb_file.stem}"
    )

    if 671 in residue_plddt:
        print(f"\nActive site Cys671 pLDDT: {residue_plddt[671]:.2f}")


if __name__ == "__main__":
    main()
