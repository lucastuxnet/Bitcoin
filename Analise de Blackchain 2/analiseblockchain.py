import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para obter o histórico de transações de um endereço de Bitcoin
def get_address_transactions(address):
    # API do blockcypher (você pode usar outras como blockchair)
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/full"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['txs']  # retorna todas as transações do endereço
    else:
        raise Exception("Erro ao acessar os dados da API")

# Função para calcular o saldo ao longo das transações
def calculate_balance(transactions, address):
    balance = 0
    balance_history = []
    dates = []
    
    for tx in transactions:
        # Calcule o valor líquido das entradas e saídas
        net_value = sum(output['value'] for output in tx['outputs'] if address in output.get('addresses', [])) \
                    - sum(input['output_value'] for input in tx['inputs'] if address in input.get('addresses', []))
        balance += net_value
        balance_history.append(balance)
        dates.append(tx['confirmed'])
    
    return balance_history, dates

# Função para calcular o índice de Gini das transações
def gini(transactions):
    values = [tx['outputs'][0]['value'] for tx in transactions if 'outputs' in tx]
    sorted_values = np.sort(values)
    n = len(values)
    cumulative_values = np.cumsum(sorted_values)
    gini_index = (2 * np.sum(cumulative_values) / (n * np.sum(sorted_values))) - (n + 1) / n
    return gini_index

# Função para verificar a conformidade das transações com a Lei de Benford
def benford_law(transactions):
    first_digits = [int(str(tx['outputs'][0]['value'])[0]) for tx in transactions if tx['outputs'][0]['value'] > 0]
    counts = np.bincount(first_digits)[1:]  # Contar o número de ocorrências de cada dígito de 1 a 9
    total = len(first_digits)
    
    benford_distribution = np.log10(1 + 1 / np.arange(1, 10))
    
    # Plotar a distribuição observada versus a Lei de Benford
    plt.bar(np.arange(1, 10), counts / total, alpha=0.7, label="Transações")
    plt.plot(np.arange(1, 10), benford_distribution, 'r-', lw=2, label="Lei de Benford")
    plt.xlabel("Primeiro Dígito")
    plt.ylabel("Frequência")
    plt.legend()
    plt.title("Distribuição de Benford nas Transações")
    plt.show()

# Função principal que executa todas as análises
def main():
    address = "1JHH1pmHujcVa1aXjRrA13BJ13iCfgfBqj"
    
    # Obter transações do endereço
    print("Obtendo transações...")
    transactions = get_address_transactions(address)
    
    # 1. Analisar histórico de saldo
    print("Calculando histórico de saldo...")
    balance_history, dates = calculate_balance(transactions, address)
    
    plt.plot(dates, balance_history)
    plt.title("Histórico de saldo do endereço")
    plt.xlabel("Data")
    plt.ylabel("Saldo (Satoshis)")
    plt.xticks(rotation=45)
    plt.show()
    
    # 2. Calcular o índice de Gini
    print("Calculando índice de Gini...")
    gini_index = gini(transactions)
    print(f"Índice de Gini das transações: {gini_index}")
    
    # 3. Analisar distribuição de Benford
    print("Analisando a distribuição de Benford...")
    benford_law(transactions)

if __name__ == "__main__":
    main()
