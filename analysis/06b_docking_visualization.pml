# analysis/06b_docking_visualization.pml
#
# Visualizes the best docking pose (mode 1, highest predicted affinity)
# for 5-FU against both the reference and variant structures, in the
# context of the full protein. Checks whether the ligand converges on
# the same spatial region in both cases.
#
# Requires that individual poses have already been extracted with:
#   obabel docking_reference_out.pdbqt -O ligand_pose_reference.pdb -f 1 -l 1
#   obabel docking_variant_out.pdbqt   -O ligand_pose_variant.pdb   -f 1 -l 1

load ../data/structures/DPYD_reference.pdb, reference
load ../data/structures/DPYD_variant_aligned.pdb, variant
load ligand_pose_reference.pdb, ligand_ref
load ligand_pose_variant.pdb, ligand_var

hide everything

show cartoon, reference or variant
color gray70, reference
color wheat, variant
set cartoon_transparency, 0.6, reference
set cartoon_transparency, 0.6, variant

select active_site_ref, reference and resi 671
select active_site_var, variant and resi 616

show sticks, active_site_ref or active_site_var
color green, active_site_ref
color limegreen, active_site_var
label active_site_ref and name CA, "Cys671"
label active_site_var and name CA, "Cys616 (var)"

show sticks, ligand_ref or ligand_var
color magenta, ligand_ref
color cyan, ligand_var
set stick_radius, 0.25, ligand_ref or ligand_var

python
from pymol import cmd

model_lig_ref = cmd.get_model("ligand_ref")
model_lig_var = cmd.get_model("ligand_var")

def centroid(model):
    xs = [a.coord[0] for a in model.atom]
    ys = [a.coord[1] for a in model.atom]
    zs = [a.coord[2] for a in model.atom]
    return (sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs))

lig_ref_center = centroid(model_lig_ref)
lig_var_center = centroid(model_lig_var)

as_ref_coord = cmd.get_model("active_site_ref and name CA").atom[0].coord
as_var_coord = cmd.get_model("active_site_var and name CA").atom[0].coord

def dist(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2) ** 0.5

d_ref = dist(lig_ref_center, as_ref_coord)
d_var = dist(lig_var_center, as_var_coord)

print("=== Ligand centroid to active site distance ===")
print("Reference: {:.2f} A".format(d_ref))
print("Variant:   {:.2f} A".format(d_var))

d_between_poses = dist(lig_ref_center, lig_var_center)
print("Distance between reference pose and variant pose: {:.2f} A".format(d_between_poses))
python end

bg_color white
set ray_opaque_background, 0
set label_size, 18
orient reference or variant
zoom (active_site_ref or active_site_var or ligand_ref or ligand_var), 6
ray 1400, 1000
png ../figures/06b_docking_poses_comparison.png, dpi=300

print "Done."
