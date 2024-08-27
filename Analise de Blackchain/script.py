import requests

# URL da API para obter o último bloco da blockchain
url_last_block = "https://blockchain.info/latestblock"

# Faz a requisição para obter o último bloco
response_last_block = requests.get(url_last_block)
last_block_hash = response_last_block.json()['hash']

# URL da API para obter os detalhes do bloco pelo hash
url_block_details = f"https://blockchain.info/rawblock/{last_block_hash}"

# Faz a requisição para obter os detalhes do bloco
response_block_details = requests.get(url_block_details)
block_details = response_block_details.json()

# A transação de Coinbase é sempre a primeira transação no bloco
coinbase_transaction = block_details['tx'][0]

print("Transação de Coinbase:")
print(f"Hash: {coinbase_transaction['hash']}")

# Lista os endereços que receberam os Bitcoins minerados + taxas
print("\nEndereços que estão recebendo os Bitcoins minerados + taxas:")
for output in coinbase_transaction['out']:
    address = output.get('addr', 'Endereço não disponível')
    value = output['value'] / 10**8  # Converte de satoshis para bitcoins
    print(f"Endereço: {address}, Valor: {value} BTC")

# Itera sobre as transações do bloco (exceto a primeira, que é a Coinbase)
for transaction in block_details['tx'][1:]:
    tx_hash = transaction['hash']
    inputs = transaction['inputs']
    outputs = transaction['out']

    # Calcula a taxa da transação
    input_value = sum(inp['prev_out']['value'] for inp in inputs if 'prev_out' in inp)
    output_value = sum(out['value'] for out in outputs)
    fee = (input_value - output_value) / 10**8  # Converte de satoshis para bitcoins

    # Imprime os detalhes da transação
    print(f"\nTransação Hash: {tx_hash}")
    print(f"Taxa: {fee} BTC")
    print(f"Número de Entradas: {len(inputs)}")
    print(f"Número de Saídas: {len(outputs)}")

    for output in outputs:
        address = output.get('addr', 'Endereço não disponível')
        value = output['value'] / 10**8  # Converte de satoshis para bitcoins
        print(f"Endereço: {address}, Valor: {value} BTC")
