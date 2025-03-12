import argparse

# Função para extrair Mg de protein_minimised.pdb e preservar resíduos de prepared_protein2.pdb
def transfer_mg_and_preserve_residues(input_pdb, mg_pdb, output_pdb):
    # Abrir o arquivo de entrada (prepared_protein2.pdb) e o arquivo com os Mg (protein_minimised.pdb)
    with open(input_pdb, 'r') as infile, open(mg_pdb, 'r') as mgfile, open(output_pdb, 'w') as outfile:
        # Extrair os íons Mg de protein_minimised.pdb (arquivo com os íons Mg)
        heatm_mg = [line for line in mgfile if line.lower().startswith('hetatm') and 'mg' in line.lower()]
        
        # Voltar para o início do arquivo de proteínas preparadas e copiar as linhas para o arquivo de saída
        infile.seek(0)
        lines_to_keep = []
        
        # Lista para armazenar as linhas CONECT associadas a Mg
        conect_lines = []
        
        # Manter as linhas do PDB de proteínas preparadas
        for line in infile:
            # Verificar se é uma linha CONECT e se está associada a um átomo Mg ou hidrogênios
            if line.lower().startswith('conect'):
                # Manter as linhas CONECT associadas a hidrogênios ou Mg
                if any(mg in line.lower() for mg in ['mg']) or 'h' in line[12:16].strip().lower():
                    conect_lines.append(line)
            # Copiar as linhas de resíduos de proteínas (não HETATM Mg ou CONECT)
            elif not line.lower().startswith('hetatm') or 'mg' not in line.lower():
                lines_to_keep.append(line)

        # Escrever as linhas preservadas (resíduos da proteína)
        outfile.writelines(lines_to_keep)
        
        # Adicionar os íons Mg do arquivo protein_minimised.pdb
        outfile.writelines(heatm_mg)

        # Adicionar as linhas CONECT associadas a Mg ou hidrogênios
        outfile.writelines(conect_lines)

# Função principal para configurar e rodar o script
def main():
    # Definir os argumentos que serão passados pela linha de comando
    parser = argparse.ArgumentParser(description="Preservar resíduos de prepared_protein2 e transferir íons Mg de protein_minimised.")
    parser.add_argument("-p", "--input_pdb", required=True, help="Caminho para o arquivo PDB de entrada (prepared_protein2.pdb)")
    parser.add_argument("-m", "--mg_pdb", required=True, help="Caminho para o arquivo PDB com os íons Mg (protein_minimised.pdb)")
    parser.add_argument("-o", "--output_pdb", required=True, help="Caminho para o arquivo PDB de saída")

    # Parse os argumentos passados
    args = parser.parse_args()

    # Transferir os íons Mg e preservar os resíduos da proteína
    transfer_mg_and_preserve_residues(args.input_pdb, args.mg_pdb, args.output_pdb)

    print(f'Íons Mg foram transferidos para o arquivo {args.output_pdb}, preservando os resíduos da proteína.')

if __name__ == "__main__":
    main()
