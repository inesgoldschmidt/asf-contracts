# pip install web3==5.7.0
from json import loads

from web3 import Web3, HTTPProvider
from contract_adress import ContractAdress

web3 = Web3(HTTPProvider("http://127.0.0.1:8545", request_kwargs={"timeout": 60}))


def get_params(sender):
    return {"from": sender, "gasPrice": web3.eth.gasPrice, "gas": 6721975,
            "nonce": web3.eth.getTransactionCount(sender)}


# Read Contract
with open("build/contracts/AppCoins.json", "r") as f_handler:
    contract_info = loads(f_handler.read())
    f_handler.close()

# Get AppCoins Contract
appcoins_contract = web3.eth.contract(ContractAdress.APPCOINS.value, abi=contract_info["abi"])


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


###################
###### ETHER ######
###################

# print_balanches_ether()

# # Ether Transfer
# tx_params = {**get_params(web3.eth.accounts[0]), "to": web3.eth.accounts[1], "value": 1}
# txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
# print("\nEther Transfer (Transaction):\n{}".format(web3.eth.getTransaction(txid)))

# print_balances_ether()

########################
###### END: ETHER ######
########################


######################
###### APPCOINS ######
######################

###### TRANSFER ######
print_balances_appcoins()

tx_params = appcoins_contract.functions.transfer(web3.eth.accounts[1], 2)\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("\nAppCoins Transfer (Transaction):\n{}".format(web3.eth.getTransaction(txid)))

receipt = web3.eth.getTransactionReceipt(txid)
print("\nAppCoins Transfer (Event):\n{}".format(
    appcoins_contract.events.Transfer().processReceipt(receipt)))

print_balances_appcoins()
###### END: TRANSFER ######

print("Owner: {}".format(appcoins_contract.functions.owner().call()))
print("Total Supply: {}".format(appcoins_contract.functions.totalSupply().call()))
print("Decimals: {}".format(appcoins_contract.functions.decimals().call()))
print("Name: {}".format(appcoins_contract.functions.name().call().decode('utf8')))
print("Symbol: {}".format(appcoins_contract.functions.symbol().call().decode('utf8')))
i = 1
print("Balance of {}: {}".format(i, appcoins_contract.functions.balanceOf(web3.eth.accounts[i]).call()))

###### APPROVE ######
print("\n\n###### APROVE ######")
print_balances_appcoins()

tx_params = appcoins_contract.functions.approve(web3.eth.accounts[3], 100)\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("\nAppCoins Approve:\n{}".format(web3.eth.getTransaction(txid)))

print_balances_appcoins()
print("\n###### END: APROVE ######")
###### END: APPROVE ######

###### BURN ######
print("\n\n###### BURN ######")
print_balances_appcoins()

tx_params = appcoins_contract.functions.burn(50)\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("\nAppCoins Burn:\n{}".format(web3.eth.getTransaction(txid)))

receipt = web3.eth.getTransactionReceipt(txid)
print("\nAppCoins Burn (Event):\n{}".format(
    appcoins_contract.events.Burn().processReceipt(receipt)))

print_balances_appcoins()
print("\n###### END: BURN ######")
###### END: BURN ######

###### BURN FROM ######
print("\n\n###### BURN FROM ######")
print_balances_appcoins()

tx_params = appcoins_contract.functions.burnFrom(web3.eth.accounts[0], 48)\
    .buildTransaction(get_params(web3.eth.accounts[3]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("\nAppCoins Burn From:\n{}".format(web3.eth.getTransaction(txid)))

receipt = web3.eth.getTransactionReceipt(txid)
print("\nAppCoins Burn (Event):\n{}".format(
    appcoins_contract.events.Burn().processReceipt(receipt)))

print_balances_appcoins()
print("\n###### END: BURN FROM ######")
###### END: BURN FROM ######

###### TRANSFER FROM ######
print("\n\n###### TRANSFER FROM ######")
print_balances_appcoins()

tx_params = appcoins_contract.functions.transferFrom(web3.eth.accounts[0], web3.eth.accounts[3], 50)\
    .buildTransaction(get_params(web3.eth.accounts[3]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("\nAppCoins Transfer From:\n{}".format(web3.eth.getTransaction(txid)))

receipt = web3.eth.getTransactionReceipt(txid)
print("\nAppCoins Transfer (Event):\n{}".format(
    appcoins_contract.events.Transfer().processReceipt(receipt)))

print_balances_appcoins()
print("\n###### END: TRANSFER FROM ######")
###### END: TRANSFER FROM ######


###########################
###### END: APPCOINS ######
###########################
