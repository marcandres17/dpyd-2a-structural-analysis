# analysis/06_active_site_distance.pml
#
# Measures the real 3D spatial distance (not linear sequence distance)
# between the catalytic residue Cys671 and the critical zone affected
# by exon 14 deletion (residues 570-600 in the reference).
#
# Run on the reference structure only, since it has reliable folding
# confidence in both regions (high pLDDT in 570-600 AND at position 671).

load ../data/structures/DPYD_reference.pdb, reference
load ../data/structures/DPYD_variant_aligned.pdb, variant

select active_site, reference and resi 671
select critical_zone, reference and resi 570-600

python
from pymol import cmd

model_as = cmd.get_model("active_site and name CA")
model_zone = cmd.get_model("critical_zone and name CA")

min_dist = float("inf")
min_pair = None

for atom_as in model_as.atom:
    for atom_zone in model_zone.atom:
        dx = atom_as.coord[0] - atom_zone.coord[0]
        dy = atom_as.coord[1] - atom_zone.coord[1]
        dz = atom_as.coord[2] - atom_zone.coord[2]
        dist = (dx**2 + dy**2 + dz**2) ** 0.5
        if dist < min_dist:
            min_dist = dist
            min_pair = (atom_as.resi, atom_zone.resi)

print("=== Minimum real distance (CA-CA) between Cys671 and the critical zone ===")
print("Closest residue in the critical zone: " + str(min_pair[1]))
print("Distance: {:.2f} A".format(min_dist))
python end

hide everything
show cartoon, reference
color gray80, reference

select active_site_display, reference and resi 671
show sticks, active_site_display
color green, active_site_display
label active_site_display and name CA, "Cys671 (active site)"

color red, reference and resi 570-600
label reference and resi 585 and name CA, "Critical zone (exon 14)"

bg_color white
set ray_opaque_background, 0
set label_size, 18
orient reference and (resi 671 or resi 570-600)
zoom reference and (resi 671 or resi 570-600), 8
ray 1200, 900
png ../figures/06_active_site_proximity.png, dpi=300

print "Done."
