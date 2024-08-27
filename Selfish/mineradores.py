import numpy as np

# Carregar o arquivo .npy
arquivo_npy = 'meses.npy'  # Substitua pelo caminho para o seu arquivo .npy
conteudo = np.load(arquivo_npy, allow_pickle=True)

# Verificar quantos IDs diferentes existem no arquivo
ids_unicos = np.unique(conteudo)
num_ids_unicos = len(ids_unicos)

# Mostrar os resultados
print(f"Total de IDs diferentes no arquivo: {num_ids_unicos}")
print(f"IDs diferentes: {ids_unicos}")
