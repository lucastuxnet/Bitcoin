import numpy as np
import matplotlib.pyplot as plt
import random

def ler_ids_mineradores(caminho_do_arquivo):
    return np.load(caminho_do_arquivo)

def dividir_lista_em_meses(lista, num_meses=12):
    tamanho = len(lista) // num_meses
    return [lista[i*tamanho:(i+1)*tamanho] for i in range(num_meses)]

def escolher_mes_aniversario(mes):
    if 1 <= mes <= 12:
        return mes - 1
    else:
        raise ValueError("Mês inválido. Escolha um mês entre 1 e 12.")

def gerar_grafico_poder_computacional(dados, mes, top_n=None):
    dias = list(range(1, len(next(iter(dados.values()))) + 1))
    plt.figure(figsize=(10, 5))
    sorted_dados = sorted(dados.items(), key=lambda item: sum(item[1]), reverse=True)
    
    if top_n:
        sorted_dados = sorted_dados[:top_n]
    
    for minerador, poder in sorted_dados:
        plt.plot(dias, poder, label=minerador)
    
    title_suffix = f" (Top {top_n})" if top_n else ""
    plt.title(f"Poder Computacional dos Mineradores no Mês {mes + 1}{title_suffix}")
    plt.xlabel("Dia")
    plt.ylabel("Poder Computacional")
    plt.legend()
    plt.show()

def determinar_mp(dados):
    total_poder = {minerador: sum(poder) for minerador, poder in dados.items()}
    mp = max(total_poder, key=total_poder.get)
    return mp, total_poder[mp]

def contar_mineracoes_sequenciais(mp, dados):
    sequencias = 0
    max_sequencia = 0
    mineradores_sequenciais = []
    for poder in dados[mp]:
        if poder > 0:
            sequencias += 1
            mineradores_sequenciais.append(mp)
            if sequencias > max_sequencia:
                max_sequencia = sequencias
        else:
            sequencias = 0
    return max_sequencia, mineradores_sequenciais

def contar_mineracoes_sequenciais_por_minerador(dados):
    mineradores_sequenciais = {}
    for minerador, poderes in dados.items():
        sequencias = []
        atual_sequencia = 0
        for poder in poderes:
            if poder > 0:
                atual_sequencia += 1
            else:
                if atual_sequencia > 0:
                    sequencias.append(atual_sequencia)
                atual_sequencia = 0
        if atual_sequencia > 0:
            sequencias.append(atual_sequencia)
        mineradores_sequenciais[minerador] = sequencias
    return mineradores_sequenciais

def mostrar_quantidade_minerada_por_minerador(dados):
    quantidades = {minerador: sum(poder) for minerador, poder in dados.items()}
    for minerador, quantidade in quantidades.items():
        print(f"Minerador: {minerador}, Quantidade Minerada: {quantidade}")

def permutar_dados(dados):
    mineradores = list(dados.keys())
    permutacoes = []
    for _ in range(1000):
        permutacao = {}
        for minerador in mineradores:
            poderes = dados[minerador]
            poderes_permutados = np.random.permutation(poderes).tolist()
            permutacao[minerador] = poderes_permutados
        permutacoes.append(permutacao)
    return permutacoes

def calcular_pvalue(mp, sequencia_mp, permutacoes):
    contagem = 0
    for permutacao in permutacoes:
        sequencia_permutacao, _ = contar_mineracoes_sequenciais(mp, permutacao)
        if sequencia_permutacao >= sequencia_mp:
            contagem += 1
    pvalue = contagem / len(permutacoes)
    return pvalue

def main():
    # Passo 1: Ler a lista de IDs dos mineradores do arquivo .npy
    caminho_do_arquivo = input("Digite o caminho para o arquivo .npy com os IDs dos mineradores: ")
    ids_mineradores = ler_ids_mineradores(caminho_do_arquivo)

    # Passo 2: Dividir a lista em meses
    meses = dividir_lista_em_meses(ids_mineradores)

    # Passo 3: Escolher o mês do aniversário
    mes_aniversario = escolher_mes_aniversario(int(input("Digite o mês do seu aniversário (1-12): ")))

    # Simulação de dados de poder computacional por dia para cada minerador no mês do aniversário
    num_dias = 30  # Exemplo de um mês com 30 dias
    dados_mes = {minerador: np.random.randint(0, 100, num_dias).tolist() for minerador in meses[mes_aniversario]}

    # Passo 4: Gerar o gráfico com o poder computacional
    gerar_grafico_poder_computacional(dados_mes, mes_aniversario)

    # Passo 5: Determinar o MP do mês
    mp, poder_mp = determinar_mp(dados_mes)
    print(f"O minerador mais poderoso (MP) do mês é: {mp} com um poder total de {poder_mp}")

    # Passo 6: Gerar o gráfico com o poder computacional dos cinco maiores mineradores
    gerar_grafico_poder_computacional(dados_mes, mes_aniversario, top_n=5)

    # Passo 7: Mostrar todas as minerações sequenciais por minerador
    mineracoes_sequenciais = contar_mineracoes_sequenciais_por_minerador(dados_mes)
    for minerador, sequencias in mineracoes_sequenciais.items():
        print(f"Minerador: {minerador}, Minerações Sequenciais: {sequencias}")

    # Passo 8: Mostrar quantidade minerada por minerador
    mostrar_quantidade_minerada_por_minerador(dados_mes)

    # Passo 9: Contar as minerações em sequência do MP
    sequencia_mp, mineradores_sequenciais_mp = contar_mineracoes_sequenciais(mp, dados_mes)
    print(f"O MP {mp} teve {sequencia_mp} minerações em sequência no mês")

    # Passo 10: Gerar 1000 permutações da lista e contar as minerações em sequência do MP em cada permutação
    permutacoes = permutar_dados(dados_mes)

    # Passo 11: Determinar a posição do MP nesta lista de 1000 permutações (p-value)
    pvalue = calcular_pvalue(mp, sequencia_mp, permutacoes)
    print(f"O p-value para a sequência do MP {mp} é: {pvalue}")

if __name__ == "__main__":
    main()