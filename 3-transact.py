import json
from datetime import datetime
from random import randint, choice

from web3 import Web3

ds = json.load(open('data.json', 'r'))

w3 = Web3(Web3.HTTPProvider('http://35.240.174.241:8545'))
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
datastore = json.load(open('data.json', 'r'))

w3.eth.defaultAccount = w3.eth.accounts[1]
user = w3.eth.contract(address=ds['contract_address'], abi=ds['abi'])

awb = str(randint(1000000000,9999999999))
loc = choice(['Chennai', 'Banglore', 'Kuala Lumpur', 'Prague', 'CyberJaya', 'Bonn', 'Texas'])
status = choice(['DELIVERED', 'CREATED', 'PICKED', 'IN-TRANSIT', 'OUT OF DELIVERY', 'RETURNED', 'CUSTOM'])
notes = choice(['All Ok', 'Handle with care', 'surprise Gift'])

tx = user.functions.setShipment(awb, str(datetime.now()), loc, status, notes)
tx = tx.transact()
w3.eth.waitForTransactionReceipt(tx)
shipment_data = user.functions.getShipment().call()

print("SHIPMENT DATA")
print(shipment_data)
print("==============================END====================================")
