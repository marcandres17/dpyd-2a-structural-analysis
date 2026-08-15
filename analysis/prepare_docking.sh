#!/bin/bash
# analysis/prepare_docking.sh
#
# Prepares ligand and receptor files for AutoDock Vina, and generates
# the Vina configuration files for both the reference and variant
# structures, centered on the same active-site coordinates.
#
# Prerequisites:
#   - AutoDock Vina and Open Babel installed (conda install -c
#     conda-forge -c bioconda autodock-vina openbabel)
#   - data/structures/DPYD_reference.pdb and
#     data/structures/DPYD_variant_aligned.pdb already generated
#     (the latter via analysis/05_superposition.pml)
#   - Active-site coordinates obtained via PyMOL (see README) and
#     filled in below

set -euo pipefail

STRUCT_DIR="../data/structures"
CENTER_X=17.292
CENTER_Y=-3.626
CENTER_Z=-30.135

echo "=== Downloading and preparing 5-FU ligand ==="
wget -q "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/3385/SDF" -O 5FU.sdf
obabel 5FU.sdf -O 5FU.pdbqt --gen3d -h --partialcharge gasteiger

echo "=== Preparing receptor PDBQT files ==="
obabel "${STRUCT_DIR}/DPYD_reference.pdb" -O DPYD_reference.pdbqt -xr
obabel "${STRUCT_DIR}/DPYD_variant_aligned.pdb" -O DPYD_variant_aligned.pdbqt -xr

echo "=== Cleaning PDBQT headers (Open Babel copies PDB HEADER/TITLE lines ==="
echo "=== that Vina's parser rejects) ==="
grep -E "^(ATOM|HETATM|ROOT|ENDROOT|BRANCH|ENDBRANCH|TORSDOF|TER|END)" \
    DPYD_reference.pdbqt > DPYD_reference_clean.pdbqt
grep -E "^(ATOM|HETATM|ROOT|ENDROOT|BRANCH|ENDBRANCH|TORSDOF|TER|END)" \
    DPYD_variant_aligned.pdbqt > DPYD_variant_aligned_clean.pdbqt

echo "=== Writing Vina config files ==="
cat > config_reference.txt << EOF
receptor = DPYD_reference_clean.pdbqt
ligand = 5FU.pdbqt

center_x = ${CENTER_X}
center_y = ${CENTER_Y}
center_z = ${CENTER_Z}

size_x = 20
size_y = 20
size_z = 20

exhaustiveness = 8
num_modes = 9
out = docking_reference_out.pdbqt
log = docking_reference_log.txt
EOF

cat > config_variant.txt << EOF
receptor = DPYD_variant_aligned_clean.pdbqt
ligand = 5FU.pdbqt

center_x = ${CENTER_X}
center_y = ${CENTER_Y}
center_z = ${CENTER_Z}

size_x = 20
size_y = 20
size_z = 20

exhaustiveness = 8
num_modes = 9
out = docking_variant_out.pdbqt
log = docking_variant_log.txt
EOF

echo ""
echo "Setup complete. Run docking with:"
echo "  vina --config config_reference.txt"
echo "  vina --config config_variant.txt"
echo ""
echo "After docking, extract the best pose (mode 1) from each result with:"
echo "  obabel docking_reference_out.pdbqt -O ligand_pose_reference.pdb -f 1 -l 1"
echo "  obabel docking_variant_out.pdbqt   -O ligand_pose_variant.pdb   -f 1 -l 1"
