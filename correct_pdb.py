from pdbfixer import PDBFixer
from openmm.app import PDBFile

fixer = PDBFixer("prepared_protein.pdb")
PDBFile.writeFile(fixer.topology, fixer.positions, open("protein_minimised.pdb", "w"))
