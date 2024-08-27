import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import groupby
import random

# Função para dividir dados em meses e salvar em arquivo separado
def dividir_e_salvar_dados(arquivo):
    dados = np.load(arquivo, allow_pickle=True)
    dias_por_mes = len(dados) // 12
    meses = [dados[i*dias_por_mes:(i+1)*dias_por_mes] for i in range(12)]
    np.save('meses.npy', meses)

# Função para carregar dados de um mês específico
def carregar_dados_mes(arquivo, mes):
    meses = np.load(arquivo, allow_pickle=True)
    dados_mes = meses[mes - 1]
    return pd.DataFrame(dados_mes, columns=['MineradorID'])

# Função para gerar gráfico de poder computacional por dia
def gerar_grafico(df, mes):
    poder_computacional = df['MineradorID'].value_counts()
    poder_computacional.plot(kind='bar', figsize=(10, 6))
    plt.title(f'Poder Computacional dos Mineradores no Mês {mes}')
    plt.xlabel('MineradorID')
    plt.ylabel('Contagem de Minerações')
    plt.show()

# Função para determinar o minerador mais poderoso e suas minerações consecutivas
def determinar_mp_e_minerações(df):
    poder_computacional = df['MineradorID'].value_counts()
    mp = poder_computacional.idxmax()
    mp_minerações = df[df['MineradorID'] == mp].copy()
    mp_minerações['Dia'] = np.arange(1, len(mp_minerações) + 1)
    sequencias_mp = [len(list(g)) for k, g in groupby(mp_minerações['Dia'].diff().fillna(1).ne(1).cumsum())]
    max_sequencia_mp = max(sequencias_mp) if sequencias_mp else 0
    return mp, max_sequencia_mp, mp_minerações

# Função para mostrar mineração sequencial por dia
def mostrar_dias_mineração_sequencial(df):
    print("\nMinerações sequenciais por minerador:")
    for minerador, group in df.groupby('MineradorID'):
        dias = group.index + 1
        sequencias = [list(g) for k, g in groupby(dias)]
        print(f"Minerador {minerador}:")
        for seq in sequencias:
            if seq:
                print(f"  - Início no dia {seq[0]} por {len(seq)} dia(s) consecutivo(s)")

# Função para realizar permutações e calcular p-value
def calcular_p_value(dados, mes, mp, max_sequencia_mp, n_permutações=1000):
    df = pd.DataFrame(dados, columns=['MineradorID'])
    sequencias_perm = []
    for _ in range(n_permutações):
        permutacao = np.random.permutation(df['MineradorID'])
        df_perm = pd.DataFrame(permutacao, columns=['MineradorID'])
        _, perm_max_sequencia_mp, _ = determinar_mp_e_minerações(df_perm)
        sequencias_perm.append(perm_max_sequencia_mp)
    sequencias_perm = np.array(sequencias_perm)
    p_value = np.sum(sequencias_perm >= max_sequencia_mp) / n_permutações
    return p_value

# Main
def main():
    # Caminho do arquivo original com dados de um ano
    arquivo_original = 'block_integer_array.npy'  # Substitua pelo caminho correto do arquivo

    # Dividir e salvar os dados em meses
    dividir_e_salvar_dados(arquivo_original)
    
    # Solicitar o mês de aniversário ao usuário
    mes = int(input("Digite o mês do seu aniversário (1-12): "))

    # Verificar se o mês é válido
    if mes < 1 or mes > 12:
        print("Mês inválido. Por favor, escolha um mês entre 1 e 12.")
        return

    # Carregar dados do mês específico
    df = carregar_dados_mes('meses.npy', mes)

    # Gerar gráfico
    gerar_grafico(df, mes)
    
    # Mostrar dias com mineração sequencial por minerador
    mostrar_dias_mineração_sequencial(df)

    # Determinar MP e contar as minerações consecutivas
    mp, max_sequencia_mp, mp_minerações = determinar_mp_e_minerações(df)
    print(f"\nO minerador mais poderoso (MP) do mês {mes} é o ID {mp}.")
    print(f"Maior sequência de minerações consecutivas do MP: {max_sequencia_mp}.")
    
    # Calcular p-value
    dados_completos = np.load(arquivo_original, allow_pickle=True)
    p_value = calcular_p_value(dados_completos, mes, mp, max_sequencia_mp)
    print(f"p-value: {p_value}")

if __name__ == "__main__":
    main()
