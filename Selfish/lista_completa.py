import numpy as np
import csv

# Carregar o arquivo .npy
arquivo_npy = 'meses.npy'  # Substitua pelo caminho para o seu arquivo .npy
conteudo = np.load(arquivo_npy, allow_pickle=True)

# Verificar se o conteúdo é um array multidimensional
if len(conteudo.shape) == 1:
    # Se for um array unidimensional
    dados = conteudo[:, None]  # Converte para uma matriz coluna
else:
    dados = conteudo

# Definir o nome do arquivo .csv
arquivo_csv = 'seu_arquivo.csv'  # Substitua pelo caminho e nome desejado para o arquivo .csv

# Salvar o conteúdo no arquivo .csv
with open(arquivo_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([f'Coluna {i+1}' for i in range(dados.shape[1])])  # Escrever o cabeçalho
    writer.writerows(dados)

print(f"Arquivo .csv salvo como {arquivo_csv}")
