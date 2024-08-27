import numpy as np
import matplotlib.pyplot as plt
import random
import os

def carregar_arquivo_npy(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        return np.load(caminho_arquivo, allow_pickle=True)
    else:
        raise FileNotFoundError(f"O arquivo '{caminho_arquivo}' não foi encontrado.")
arquivo_npy = 'block_integer_array.npy'  
try:
    ids = carregar_arquivo_npy(arquivo_npy)
    meses = []
    for i in range(12):
        mes = []
        for j in range(30):
            dia = ids[(i * 30 + j) * 35: (i * 30 + j + 1) * 35]
            mes.append(dia)
        meses.append(mes)
    np.save('meses.npy', meses)
    mes_aniversario = int(input("Digite o mês do seu aniversário (1-12): ")) - 1
    meses = np.load('meses.npy', allow_pickle=True)
    mes_escolhido = meses[mes_aniversario]
    poder_computacional = {}
    for dia in mes_escolhido:
        for minerador in dia:
            if minerador in poder_computacional:
                poder_computacional[minerador] += 1
            else:
                poder_computacional[minerador] = 1
    total_poder = sum(poder_computacional.values())
    percentuais = {minerador: (poder / total_poder) * 100 for minerador, poder in poder_computacional.items()}
    print("Poder computacional total de cada usuário em porcentagem:")
    for minerador, percentual in percentuais.items():
        print(f"Minerador {minerador}: {percentual:.2f}%")
    MP = max(poder_computacional, key=poder_computacional.get)
    print(f"O minerador mais poderoso (MP) do mês é: {MP}")
    def contar_sequencias(mes, mp):
        max_sequencia = 0
        atual_sequencia = 0
        for dia in mes:
            for minerador in dia:
                if minerador == mp:
                    atual_sequencia += 1
                    if atual_sequencia > max_sequencia:
                        max_sequencia = atual_sequencia
                else:
                    atual_sequencia = 0
        return max_sequencia

    sequencia_mp = contar_sequencias(mes_escolhido, MP)
    print(f"Número de minerações em sequência do MP no mês: {sequencia_mp}")
    dias = np.arange(1, 31)
    poder_diario = {minerador: np.zeros(30) for minerador in set([m for d in mes_escolhido for m in d])}
    for dia_idx, dia in enumerate(mes_escolhido):
        for minerador in dia:
            poder_diario[minerador][dia_idx] += 1
    plt.figure(figsize=(14, 8))
    colors = plt.cm.tab20(np.linspace(0, 1, len(poder_diario)))
    for idx, (minerador, poder) in enumerate(poder_diario.items()):
        plt.plot(dias, poder, label=f'Minerador {minerador}', color=colors[idx])
    plt.xlabel('Dia')
    plt.ylabel('Poder Computacional')
    plt.title(f'Poder Computacional por Minerador por Dia no Mês {mes_aniversario + 1}')
    plt.legend()
    plt.show()
    sequencias_permutacoes = []
    for _ in range(1000):
        permutacao = np.random.permutation(ids)
        permutacao_mes = [permutacao[(mes_aniversario * 30 + i) * 35: (mes_aniversario * 30 + i + 1) * 35] for i in range(30)]
        sequencias_permutacoes.append(contar_sequencias(permutacao_mes, MP))
    posicao_mp = sum(1 for seq in sequencias_permutacoes if seq >= sequencia_mp)
    pvalue = posicao_mp / 1000
    print(f"Posição do MP na lista de 1000 permutações: {posicao_mp}")
    print(f"Valor p (p-value): {pvalue}")
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"Ocorreu um erro: {e}")
