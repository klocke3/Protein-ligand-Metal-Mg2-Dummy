import sys

def read_pdb(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines

def write_pdb(file_path, lines):
    with open(file_path, 'w') as f:
        f.writelines(lines)

def extract_all_mg_coordinates(pdb_lines):
    mg_coords = []
    for line in pdb_lines:
        if (line.startswith("ATOM") or line.startswith("HETATM")) and (" MG " in line or " Mg " in line):
            try:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                mg_coords.append((x, y, z))
            except ValueError:
                pass
    return mg_coords

def get_next_residue_number(pdb_lines):
    """Encontra o maior número de resíduo e retorna o próximo disponível."""
    last_residue_number = 0
    for line in pdb_lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            try:
                residue_number = int(line[22:26].strip())  # Colunas 23-26
                last_residue_number = max(last_residue_number, residue_number)
            except ValueError:
                pass
    return last_residue_number + 1

def generate_dummy_atoms(x, y, z, mmg_residue_number):
    """Gera átomos fictícios para substituir Mg com a numeração correta do resíduo."""
    offsets = [
        (0.9, 0.0, 0.0),  # D2
        (0.0, 0.0, -0.9), # D3
        (-0.9, 0.0, 0.0), # D4
        (0.0, -0.9, 0.0), # D5
        (0.0, 0.9, 0.0),  # D6
        (0.0, 0.0, 0.9),  # D1
    ]

    atoms = [("X1", x, y, z)] + [(f"D{i+2}", x+dx, y+dy, z+dz) for i, (dx, dy, dz) in enumerate(offsets)]
    
    pdb_lines = []
    pdb_lines.append("TERM\n")

    for i, (atom, ax, ay, az) in enumerate(atoms, start=1):
        pdb_lines.append(
            f"ATOM  {i:5d} {atom:<4} MMG {mmg_residue_number:5d}    {ax:8.3f}{ay:8.3f}{az:8.3f}  1.00 38.35          {'XY' if atom == 'X1' else 'Dd'}\n"
        ) 

    pdb_lines.append("CONECT    1    2    3    4    5    6    7\n")
    for i in range(2, 8):
        pdb_lines.append(f"CONECT    {i:<4} 1\n")

    pdb_lines.append("END\n")
    return pdb_lines

def replace_mg_with_dummy(input_pdb, output_pdb):
    pdb_lines = read_pdb(input_pdb)
    mg_coords_list = extract_all_mg_coordinates(pdb_lines)

    if not mg_coords_list:
        print("Nenhum Mg encontrado no arquivo.")
        sys.exit(1)

    # Remove todos os Mg e linhas antigas de TER/END
    new_pdb_lines = [line for line in pdb_lines if not ((line.startswith("ATOM") or line.startswith("HETATM")) and " MG " in line)]
    new_pdb_lines = [line for line in new_pdb_lines if not (line.startswith("TER") or line.startswith("END"))]

    # Número inicial para novos resíduos
    next_residue = get_next_residue_number(pdb_lines)

    for i, (x, y, z) in enumerate(mg_coords_list):
        dummy_atoms = generate_dummy_atoms(x, y, z, next_residue + i)
        new_pdb_lines.extend(dummy_atoms)

    write_pdb(output_pdb, new_pdb_lines)
    print(f"Arquivo salvo como {output_pdb}")

if __name__ == "__main__":
    if len(sys.argv) != 5 or sys.argv[1] != "-p" or sys.argv[3] != "-o":
        print("Uso: python convert.py -p <input_pdb> -o <output_pdb>")
        sys.exit(1)
    
    input_pdb = sys.argv[2]
    output_pdb = sys.argv[4]
    replace_mg_with_dummy(input_pdb, output_pdb)
