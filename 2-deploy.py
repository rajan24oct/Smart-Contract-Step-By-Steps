import json
from solc import compile_files
from web3 import Web3

sols = ['contract.sol']

compliled_contract = compile_files(sols)

abi = compliled_contract['contract.sol:shipmentRecords']['abi']
bytecode = compliled_contract['contract.sol:shipmentRecords']['bin']

w3 = Web3(Web3.HTTPProvider('http://35.240.174.241:8545'))
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[1]})
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)


with open('data.json', 'w') as outfile:
    data = {
        "abi": abi,
        "contract_address": tx_receipt['contractAddress']
    }
    json.dump(data, outfile, indent=4, sort_keys=True)

print("CONTRACT ADDRESS")
print(tx_receipt['contractAddress'])
print("==============================END====================================")
