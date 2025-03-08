from pdbfixer import PDBFixer
from openmm.app import PDBFile

fixer = PDBFixer("corrigido2.pdb")
PDBFile.writeFile(fixer.topology, fixer.positions, open("corrigido3.pdb", "w"))