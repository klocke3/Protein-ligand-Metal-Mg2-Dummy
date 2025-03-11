import sys

def read_pdb(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines

def write_pdb(file_path, lines):
    with open(file_path, 'w') as f:
        f.writelines(lines)

def extract_mg_coordinates(pdb_lines):
    for line in pdb_lines:
        if (line.startswith("ATOM") or line.startswith("HETATM")) and (" MG " in line or "Mg" in line):
            parts = line.split()
            x, y, z = map(float, parts[6:9])
            return x, y, z
    return None

def generate_dummy_atoms(x, y, z):
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
    for i, (atom, ax, ay, az) in enumerate(atoms, start=1):
        pdb_lines.append(f"ATOM  {i:6}  {atom:<3} MMG     1  {ax:8.3f}{ay:8.3f}{az:8.3f}  1.00 38.35          {'XY' if atom == 'X1' else 'Dd'}\n")
    
    pdb_lines.append("CONECT    1    2    3    4    5    6    7\n")
    for i in range(2, 8):
        pdb_lines.append(f"CONECT    {i}    1\n")
    
    return pdb_lines

def replace_mg_with_dummy(input_pdb, output_pdb):
    pdb_lines = read_pdb(input_pdb)
    mg_coords = extract_mg_coordinates(pdb_lines)
    
    if mg_coords is None:
        print("Nenhum Mg encontrado no arquivo.")
        sys.exit(1)
    
    new_pdb_lines = [line for line in pdb_lines if not ((line.startswith("ATOM") or line.startswith("HETATM")) and " MG " in line)]
    new_pdb_lines = [line for line in new_pdb_lines if not (line.startswith("TER") or line.startswith("END"))]
    dummy_atoms = generate_dummy_atoms(*mg_coords)
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
