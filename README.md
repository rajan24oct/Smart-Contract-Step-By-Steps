#
ETH Smart Contract Active Learning session

# Pre-Start

```
Welcome Note and Slide
Brief about blockchain
Brief about what we gonna do
```

## Getting ready with dev environment

```
Users will be getting link to the files and instruction in skype as chat messages


http://35.240.174.241:8080/
```

1. Logint to the system \(email id is login and password in small letter\)
2. Chnage the Password
3. Create a workspace based on block-chain stack

4. Wait for the workmkspae to get ready. Once Ready \(will take time\)

5. Brief about the workspace, its feauture, small tour

6. Create the project and start below

#####

```
https://raw.githubusercontent.com/rajan24oct/sc-steps/master/0-setup-solc.py
```

```
from solc import install_solc
install_solc('v0.4.21')

# cd $HOME
# Open the .bashrc file.

# export PATH=~/.py-solc/solc-v0.4.21/bin:$PATH
# export PATH=~/.py-solc/solc-v0.4.21/bin/:$PATH
```

```bash
export PATH=~/.py-solc/solc-v0.4.21/bin:$PATH
export PATH=~/.py-solc/solc-v0.4.21/bin/:$PATH
```

#### 1. Create Contract

```bash
https://raw.githubusercontent.com/rajan24oct/sc-steps/master/contract.sol
```

```
pragma solidity ^0.4.21;

contract shipmentRecords {

struct shipment {
string waybill;
string updated_at;
string location;
string status;
string notes;
}

// shipment object
// you can also declare it public to access it from outside contract
// https://solidity.readthedocs.io/en/v0.4.24/contracts.html#visibility-and-getters
shipment shipment_obj;


// set shipment public function
// This is similar to persisting object in db.
function setShipment(string waybill, string updated_at, string location, string status, string notes) public {
shipment_obj = shipment({
waybill : waybill, updated_at : updated_at, location : location, status : status, notes : notes

});
}

// get user public function
// This is similar to getting object from db.
function getShipment() public returns (string, string, string, string, string) {
return (
shipment_obj.waybill, shipment_obj.updated_at, shipment_obj.location, shipment_obj.status, shipment_obj.notes
);
}


}
```

#### 2. Compile Contract

```bash
https://raw.githubusercontent.com/rajan24oct/sc-steps/master/1-compile.py
```

```
from solc import compile_files

sols = ['contract.sol']

compliled_contract = compile_files(sols)

print("CONTRACT")
print(compliled_contract)
print("==============================END====================================")
```

#### 3. Deploy Contract

```bash
https://raw.githubusercontent.com/rajan24oct/sc-steps/master/2-deploy.py
```

```
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
```

```
http://35.240.174.241:5000
```

#### 4. Transact

```bash
https://raw.githubusercontent.com/rajan24oct/sc-steps/master/3-transact.py
```

```
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
```

#### 5. Extract Info

```bash
https://raw.githubusercontent.com/rajan24oct/sc-steps/master/4-extract.py
```

```
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

```

#### 6. Decode Info

```bash
https://raw.githubusercontent.com/rajan24oct/sc-steps/master/5-decode.py
```

```
import json

from web3 import Web3

ds = json.load(open('data.json', 'r'))

# w3 = Web3(Web3.HTTPProvider('http://35.240.174.241:8545'))
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

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

for row in data:
x = user.functions.getShipment().call(block_identifier=row['block_number'])
print(x)

```




