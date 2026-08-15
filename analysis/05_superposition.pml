# analysis/05_superposition.pml
#
# Global structural superposition of the reference and variant DPYD
# structures. The align command performs sequence alignment first, then
# uses that residue correspondence to superpose the 3D coordinates and
# report the resulting global RMSD.

load ../data/structures/DPYD_reference.pdb, reference
load ../data/structures/DPYD_variant.pdb, variant

align variant, reference

# Save the aligned variant to disk in the reference's coordinate frame.
# This is required for any downstream step that needs both structures
# in a shared coordinate system (e.g. active-site distance measurement,
# docking box definition).
save ../data/structures/DPYD_variant_aligned.pdb, variant

color skyblue, reference
color orange, variant

hide everything
show cartoon

bg_color white
set ray_opaque_background, 0
ray 1200, 900
png ../figures/05_superposition.png, dpi=300
