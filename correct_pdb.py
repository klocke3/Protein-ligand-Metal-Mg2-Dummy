from pdbfixer import PDBFixer
from openmm.app import PDBFile

fixer = PDBFixer("protein2.pdb")
PDBFile.writeFile(fixer.topology, fixer.positions, open("protein2_prepared.pdb", "w"))
