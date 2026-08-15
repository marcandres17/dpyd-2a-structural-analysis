#!/usr/bin/env python3
"""
Per-residue pLDDT analysis for AlphaFold Server (AF3) CIF models
===================================================================

Extracts pLDDT (stored in the B_iso_or_equiv column of the CIF's
_atom_site block) for each residue, using the CA (alpha carbon) atom
as the representative atom for the residue.

Usage:
    python3 analyze_plddt.py file1.cif [file2.cif ...]

Example (compare all 5 models from an AlphaFold Server folder):
    python3 analyze_plddt.py fold_dpyd_2a_model_*.cif

What it does:
    1. Parses each CIF and extracts per-residue pLDDT
    2. Reports global (average) pLDDT and the confidence-range breakdown
    3. Analyzes in detail a configurable "critical zone" (by default,
       the residues around an artificial sequence junction)
    4. If more than one file is passed, prints a final comparison table
       to help decide which model to use
"""

import argparse
from pathlib import Path


def parse_cif_plddt(filepath):
    """
    Parses an AlphaFold CIF file and returns a dictionary
    {residue_number: pLDDT} using each residue's CA atom.
    """
    with open(filepath) as f:
        lines = f.readlines()

    start_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "_atom_site.pdbx_PDB_model_num":
            start_idx = i + 1
            break

    if start_idx is None:
        raise ValueError(
            f"Could not find the _atom_site block in {filepath}. "
            "Is this a valid AlphaFold CIF file?"
        )

    residue_plddt = {}
    residue_name = {}

    for line in lines[start_idx:]:
        line = line.strip()
        if not line or line.startswith("#"):
            break
        fields = line.split()
        if len(fields) < 18:
            break

        atom_name = fields[3]          # label_atom_id
        comp_id = fields[5]            # label_comp_id
        b_factor = float(fields[14])   # B_iso_or_equiv -> pLDDT
        auth_seq_id = int(fields[15])  # auth_seq_id -> residue number

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
        description="Analyzes per-residue pLDDT from AlphaFold CIF files"
    )
    parser.add_argument("cif_files", nargs="+", type=Path)
    parser.add_argument("--zone-start", type=int, default=570)
    parser.add_argument("--zone-end", type=int, default=600)
    parser.add_argument("--highlight", type=int, nargs="*", default=[579, 580, 581])
    args = parser.parse_args()

    comparison_table = []

    for cif_path in args.cif_files:
        if not cif_path.exists():
            print(f"WARNING: {cif_path} does not exist, skipping.")
            continue

        model_label = cif_path.stem

        residue_plddt, residue_name = parse_cif_plddt(cif_path)
        global_avg = summarize_global(residue_plddt, label=f"— {model_label}")
        zone_avg, zone_min = analyze_critical_zone(
            residue_plddt, residue_name,
            args.zone_start, args.zone_end,
            highlight_positions=args.highlight,
            label=f"— {model_label}"
        )

        comparison_table.append({
            "model": model_label,
            "plddt_global": global_avg,
            "plddt_zone": zone_avg,
            "plddt_zone_min": zone_min,
        })

    if len(comparison_table) > 1:
        print(f"\n{'='*70}")
        print("COMPARISON TABLE — use this to decide which model to keep")
        print(f"{'='*70}")
        print(f"{'Model':<25}{'Global pLDDT':<15}{'Zone pLDDT':<15}{'Zone min pLDDT':<15}")
        for row in sorted(comparison_table, key=lambda r: r["plddt_zone"] or 0, reverse=True):
            print(
                f"{row['model']:<25}"
                f"{row['plddt_global']:<15.2f}"
                f"{row['plddt_zone']:<15.2f}"
                f"{row['plddt_zone_min']:<15.2f}"
            )
        print(
            "\nRecommendation: prioritize the model with the best 'Zone pLDDT', "
            "not the best 'Global pLDDT' — the critical zone is what matters "
            "most for the structural comparison."
        )


if __name__ == "__main__":
    main()
