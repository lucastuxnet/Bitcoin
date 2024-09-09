import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Função para buscar transações de um endereço Bitcoin
def get_transactions(address):
    url = f'https://blockchain.info/rawaddr/{address}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['txs']
    else:
        print(f"Erro ao buscar transações: {response.status_code}")
        return []

# Função para calcular o saldo histórico de um endereço agrupado por dia
def calculate_balance_history(transactions):
    balance_history = []
    balance = 0
    balance_per_day = {}

    for tx in transactions:
        # Convertendo timestamp para data legível (dia-mês-ano)
        date = datetime.utcfromtimestamp(tx['time']).strftime('%d-%m-%Y')

        # Calculando o valor de cada transação
        value = sum(output['value'] for output in tx['out'] if 'addr' in output and output['addr'] == address)

        # Atualizando o saldo
        balance += value

        # Guardando o saldo no dicionário agrupado por dia
        if date in balance_per_day:
            balance_per_day[date] += balance
        else:
            balance_per_day[date] = balance

    # Convertendo o dicionário para uma lista de tuplas (data, saldo)
    for date, balance in balance_per_day.items():
        balance_history.append((date, balance))

    # Ordena pela data
    balance_history.sort(key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))

    return balance_history

# Função para calcular o índice de GINI
def calculate_gini(values):
    values = np.sort(values)
    n = len(values)
    cumulative_values = np.cumsum(values)
    gini_index = (2 / n) * (np.sum(np.arange(1, n+1) * values)) / np.sum(values) - (n + 1) / n
    return gini_index

# Função para aplicar a Lei de Benford
def benford_analysis(transactions):
    values = [int(str(sum(output['value'] for output in tx['out']))[0]) for tx in transactions]
    benford_dist = np.log10(1 + 1 / np.arange(1, 10))
    counts = np.bincount(values, minlength=10)[1:10]
    return counts / sum(counts), benford_dist

# Função para gerar gráfico do saldo histórico por dia
def plot_balance_history(balance_history):
    dates = [item[0] for item in balance_history]
    balances = [item[1] for item in balance_history]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, balances, label="Saldo Histórico")
    plt.xlabel('Data')
    plt.ylabel('Saldo (satoshi)')
    plt.title('Histórico do Saldo por Dia')
    plt.xticks(rotation=45, ha="right")  # Rotaciona as datas para melhor visualização
    plt.legend()
    plt.tight_layout()
    plt.show()

# Função para gerar gráfico do índice de GINI
def plot_gini(values):
    plt.figure(figsize=(10, 6))
    sns.histplot(values, kde=True, label="Distribuição de Transações")
    plt.title("Distribuição das Transações e GINI")
    plt.legend()
    plt.show()

# Função para gerar gráfico da Lei de Benford
def plot_benford(benford_counts, benford_expected):
    plt.figure(figsize=(10, 6))
    plt.bar(np.arange(1, 10), benford_counts, label="Distribuição Observada")
    plt.plot(np.arange(1, 10), benford_expected, 'r--', label="Distribuição Benford")
    plt.xlabel('Primeiro Dígito')
    plt.ylabel('Proporção')
    plt.title('Análise da Lei de Benford')
    plt.legend()
    plt.show()

# Endereço a ser analisado
address = '1JHH1pmHujcVa1aXjRrA13BJ13iCfgfBqj'

# Buscar transações
transactions = get_transactions(address)

# Análise do saldo por dia
balance_history = calculate_balance_history(transactions)

# Imprimir o histórico de saldo por dia
print("Histórico de Saldo por Dia (dd-mm-aaaa):")
for date, balance in balance_history:
    print(f"{date}: {balance} satoshis")

# Gerar gráfico de saldo por dia
plot_balance_history(balance_history)

# Análise de GINI das transações
transaction_values = [sum(output['value'] for output in tx['out']) for tx in transactions]
gini_index = calculate_gini(transaction_values)
print(f"Índice de GINI das transações: {gini_index:.4f}")

# Gráfico do índice de GINI
plot_gini(transaction_values)

# Análise de Benford das transações
benford_counts, benford_expected = benford_analysis(transactions)
print("Distribuição Benford das transações:", benford_counts)

# Gráfico da Lei de Benford
plot_benford(benford_counts, benford_expected)
