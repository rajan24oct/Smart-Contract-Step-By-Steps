import json

from web3 import Web3

ds = json.load(open('data.json', 'r'))

w3 = Web3(Web3.HTTPProvider('http://35.240.174.241:8545'))
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

w3.eth.defaultAccount = w3.eth.accounts[1]
user = w3.eth.contract(address=ds['contract_address'], abi=ds['abi'])

data = []

for i in range(w3.eth.blockNumber + 1):
    block = w3.eth.getBlock(i, full_transactions=True)

    for tx in block.transactions:
        tx_from = tx.get('from', '') if tx.get('from', '') else ''
        tx_to = tx.get('to', '') if tx.get('to', '') else ''

        if tx_from.lower() == ds['contract_address'].lower() or tx_to.lower() == ds['contract_address'].lower():
            ret = {
                'to': tx['to'],
                'from': tx['from'],
                'value': tx['value'],
                'gas': tx['gas'],
                'gas_price': tx['gasPrice'],
                'input': tx['input'],
                'hash': tx['hash'].hex(),
                'nonce': tx['nonce'],
                'block': tx['blockHash'].hex(),
                'block_number': tx['blockNumber'],
                'transaction_index': tx['transactionIndex'],
            }
            data.append(ret)

print(data)
