from json import loads

from web3 import Web3, HTTPProvider
from contract_adress import ContractAdress

web3 = Web3(HTTPProvider("http://127.0.0.1:8545", request_kwargs={"timeout": 60}))


def get_params(sender):
    return {"from": sender, "gasPrice": web3.eth.gasPrice, "gas": 6721975,
            "nonce": web3.eth.getTransactionCount(sender)}

# Read AppCoins Contract
with open("build/contracts/AppCoins.json", "r") as f_handler:
    contract_info = loads(f_handler.read())
    f_handler.close()

# Get AppCoins Contract
appcoins_contract = web3.eth.contract(ContractAdress.APPCOINS.value, abi=contract_info["abi"])

# Read Address Proxy Contract
with open("build/contracts/AddressProxy.json", "r") as f_handler:
    contract_info = loads(f_handler.read())
    f_handler.close()

# Get Address Proxy Contract
address_proxy_contract = web3.eth.contract(ContractAdress.ADRESSPROXY.value, abi=contract_info["abi"])


def print_balances_general(func, coin, call=False):
    i = 0
    for account in web3.eth.accounts:
        print(" - Account {}: {} {}".format(i, func(account).call() if call else func(account), coin))
        i += 1


def print_balances_ether():
    # Ether Balances
    print("\nEther Balances:")
    print_balances_general(web3.eth.getBalance, "ETH")


def print_balances_appcoins():
    # AppCoins Balances
    print("\nAppCoins Balances:")
    print_balances_general(appcoins_contract.functions.balanceOf, "APPC", True)


###### ADD ADDRESS ######
print("\n\n###### ADD ADDRESS ######")
print_balances_appcoins()

tx_params = address_proxy_contract.functions.addAddress("APPCOINS", ContractAdress.APPCOINS.value)\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("\nAddressProxy Add Adress:\n{}".format(web3.eth.getTransaction(txid)))

receipt = web3.eth.getTransactionReceipt(txid)
print("\nAddressProxy AddressCreated (Event):\n{}".format(
    address_proxy_contract.events.AddressCreated().processReceipt(receipt)))

print("\nAddressProxy AddressUpdated (Event):\n{}".format(
    address_proxy_contract.events.AddressUpdated().processReceipt(receipt)))

print_balances_appcoins()
print("\n###### END: ADD ADDRESS ######")
###### END: ADD ADDRESS ######

id = ""

###### GET IDS ######
print("\n\n###### GET IDS ######")

for elem in address_proxy_contract.functions.getAvailableIds().call():
    id = elem
    print(" - ID: {}".format(elem.decode("utf-8")))

print("\n###### END: GET IDS ######")
###### END: GET IDS ######

###### GET INFOS ######
print("\n\n###### GET INFOS ######")

print("ID: {}".format(id))
print("NAME: {}".format(address_proxy_contract.functions.getContractNameById(id).call()))
print("ADRESS: {}".format(address_proxy_contract.functions.getContractAddressById(id).call()))
print("CREATED TIME: {}".format(address_proxy_contract.functions.getContractCreatedTimeById(id).call()))
print("UPDATED TIME: {}".format(address_proxy_contract.functions.getContractUpdatedTimeById(id).call()))

print("\n###### END: GET INFOS ######")
###### END: GET INFOS ######


