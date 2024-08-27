# #############################################################################################################################
# Instruções
# Utilizando a API do blockchain.info (https://www.blockchain.com/explorer/api/blockchain_api) desenvolva um script para:
#
# Pegar o último bloco da blockchain
# Encontrar a transação de Coinbase: é a primeira transação do bloco...nao tem segredo
# Listar os endereços que estão recebendo os Bitcoins minerados + taxas
# Imprimir a taxa paga por cada transacao do bloco: lebrando que a primeira transação nao tem taxa!
# Imprimir o numero de entradas e o número de saidas de cada transacao 
#
################################################################################################################################

import requests

url_last_block = "https://blockchain.info/latestblock"
response_last_block = requests.get(url_last_block)
last_block_hash = response_last_block.json()['hash']
url_block_details = f"https://blockchain.info/rawblock/{last_block_hash}"
response_block_details = requests.get(url_block_details)
block_details = response_block_details.json()
coinbase_transaction = block_details['tx'][0]
print("Transação de Coinbase:")
print(f"Hash: {coinbase_transaction['hash']}")
print("\nEndereços que estão recebendo os Bitcoins minerados + taxas:")
for output in coinbase_transaction['out']:
    address = output.get('addr', 'Endereço não disponível')
    value = output['value'] / 10**8  
    print(f"Endereço: {address}, Valor: {value} BTC")

for transaction in block_details['tx'][1:]:
    tx_hash = transaction['hash']
    inputs = transaction['inputs']
    outputs = transaction['out']

    
    input_value = sum(inp['prev_out']['value'] for inp in inputs if 'prev_out' in inp)
    output_value = sum(out['value'] for out in outputs)
    fee = (input_value - output_value) / 10**8  
    print(f"\nTransação Hash: {tx_hash}")
    print(f"Taxa: {fee} BTC")
    print(f"Número de Entradas: {len(inputs)}")
    print(f"Número de Saídas: {len(outputs)}")

    for output in outputs:
        address = output.get('addr', 'Endereço não disponível')
        value = output['value'] / 10**8  
        print(f"Endereço: {address}, Valor: {value} BTC")
