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

def get_next_atom_number(pdb_lines):
    last_atom_number = 0
    for line in pdb_lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            try:
                atom_number = int(line[6:11].strip())
                last_atom_number = max(last_atom_number, atom_number)
            except ValueError:
                pass
    return last_atom_number + 1

def get_next_residue_number(pdb_lines):
    last_residue_number = 0
    for line in pdb_lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            try:
                residue_number = int(line[22:26].strip())
                last_residue_number = max(last_residue_number, residue_number)
            except ValueError:
                pass
    return last_residue_number + 1

def generate_multiple_mmg_blocks(coords, starting_atom_number=1, starting_residue_number=1000):
    pdb_lines = []
    atom_counter = starting_atom_number
    residue_counter = starting_residue_number

    offsets = [
        (0.9, 0.0, 0.0),
        (0.0, 0.0, -0.9),
        (-0.9, 0.0, 0.0),
        (0.0, -0.9, 0.0),
        (0.0, 0.9, 0.0),
        (0.0, 0.0, 0.9),
    ]

    for (x, y, z) in coords:
        atoms = [("X1", x, y, z)] + [(f"D{i+2}", x+dx, y+dy, z+dz) for i, (dx, dy, dz) in enumerate(offsets)]
        pdb_lines.append("TERM\n")

        current_indices = []

        for atom_name, ax, ay, az in atoms:
            pdb_lines.append(
                f"HETATM{atom_counter:5d} {atom_name:<4} MMG {residue_counter:5d}    "
                f"{ax:8.3f}{ay:8.3f}{az:8.3f}  1.00 38.35          {'XY' if atom_name == 'X1' else 'Dd'}\n"
            )
            current_indices.append(atom_counter)
            atom_counter += 1

        conect_line = f"CONECT{current_indices[0]:5d}" + ''.join(f"{idx:5d}" for idx in current_indices[1:]) + "\n"
        pdb_lines.append(conect_line)
        for idx in current_indices[1:]:
            pdb_lines.append(f"CONECT{idx:5d}{current_indices[0]:5d}\n")

        residue_counter += 1

    pdb_lines.append("END\n")
    return pdb_lines

def replace_mg_with_dummy(input_pdb, output_pdb):
    pdb_lines = read_pdb(input_pdb)
    mg_coords_list = extract_all_mg_coordinates(pdb_lines)

    if not mg_coords_list:
        print("Nenhum Mg encontrado no arquivo.")
        sys.exit(1)

    new_pdb_lines = [line for line in pdb_lines if not ((line.startswith("ATOM") or line.startswith("HETATM")) and " MG " in line)]
    new_pdb_lines = [line for line in new_pdb_lines if not (line.startswith("TER") or line.startswith("END"))]

    next_atom = get_next_atom_number(pdb_lines)
    next_residue = get_next_residue_number(pdb_lines)

    dummy_blocks = generate_multiple_mmg_blocks(mg_coords_list, starting_atom_number=next_atom, starting_residue_number=next_residue)
    new_pdb_lines.extend(dummy_blocks)

    write_pdb(output_pdb, new_pdb_lines)
    print(f"Arquivo salvo como {output_pdb}")

if __name__ == "__main__":
    if len(sys.argv) != 5 or sys.argv[1] != "-p" or sys.argv[3] != "-o":
        print("Uso: python convert.py -p <input_pdb> -o <output_pdb>")
        sys.exit(1)

    input_pdb = sys.argv[2]
    output_pdb = sys.argv[4]
    replace_mg_with_dummy(input_pdb, output_pdb)

