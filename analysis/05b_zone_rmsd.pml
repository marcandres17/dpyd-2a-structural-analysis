# analysis/05b_zone_rmsd.pml
#
# Calculates RMSD separately for:
#   (a) the critical zone (artificial junction created by exon 14 deletion)
#   (b) the rest of the protein (excluding that zone)
#
# This quantifies whether the mismatch observed during global alignment
# (rejected outlier atoms with high local RMSD) is concentrated
# specifically in the junction region, or spread across the structure.
#
# IMPORTANT: because the variant is 55 residues shorter than the
# reference, residue numbering AFTER position 580 does NOT match between
# the two structures. Separate selections are used for each object:
#   - In "reference": the critical zone is residues 570-600
#   - In "variant":   the same biological zone corresponds to residues
#                      570-580 (unshifted) + 526-545 (shifted -55)

load ../data/structures/DPYD_reference.pdb, reference
load ../data/structures/DPYD_variant.pdb, variant

align variant, reference

# ── Critical zone ────────────────────────────────────────────────────
select ref_zone, reference and resi 570-600 and name CA

select var_zone_part1, variant and resi 570-580 and name CA
select var_zone_part2, variant and resi 526-545 and name CA
select var_zone, var_zone_part1 or var_zone_part2

print "=== RMSD CRITICAL ZONE (exon junction) ==="
align var_zone, ref_zone

# ── Rest of the protein ──────────────────────────────────────────────
select ref_rest, reference and name CA and not (resi 570-600)
select var_rest_part1, variant and name CA and not (resi 570-580)
select var_rest, var_rest_part1 and not (resi 526-545)

print "=== RMSD REST OF PROTEIN (excluding critical zone) ==="
align var_rest, ref_rest

# ── Visualization ────────────────────────────────────────────────────
hide everything
show cartoon, reference or variant
color skyblue, reference
color orange, variant
color red, ref_zone
color red, var_zone

bg_color white
set ray_opaque_background, 0
orient
ray 1200, 900
png ../figures/05b_zone_comparison.png, dpi=300

print "Done. Compare the two RMSD values printed above."
