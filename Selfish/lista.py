import numpy as np

def ler_arquivo_npy(caminho_do_arquivo):
    try:
        dados = np.load(caminho_do_arquivo)
        print("Conteúdo do arquivo .npy:")
        print(dados)
    except Exception as e:
        print(f"Erro ao ler o arquivo .npy: {e}")

# Exemplo de uso
caminho_do_arquivo = '/home/lucas/Documentos/ufu/Bitcoin/Selfish/meses.npy'
ler_arquivo_npy(caminho_do_arquivo)