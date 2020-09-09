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

# Read AppCoinsIAB Contract
with open("build/contracts/AppCoinsIAB.json", "r") as f_handler:
    contract_info = loads(f_handler.read())
    f_handler.close()

# Get AppCoinsIAB Contract
appcoins_iab_contract = web3.eth.contract(ContractAdress.APPCOINSIAB.value, abi=contract_info["abi"])


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

###### APPROVE ######
print("\n\n###### APROVE ######")
print_balances_appcoins()

tx_params = appcoins_contract.functions.approve(ContractAdress.APPCOINSIAB.value, 10000)\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid))
print("\nAppCoins Approve:\n{}".format(web3.eth.getTransaction(txid)))

print_balances_appcoins()
print("\n###### END: APROVE ######")
###### END: APPROVE ######

###### BUY ######
print("\n\n###### BUY ######")
print_balances_appcoins()

tx_params = appcoins_iab_contract.functions.buy("packageName", "sku", 1000, appcoins_contract.address, web3.eth.accounts[1], web3.eth.accounts[2], web3.eth.accounts[3], bytes('PT', 'utf-8'))\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("\nAppCoins Transfer (Transaction):\n{}".format(web3.eth.getTransaction(txid)))

receipt = web3.eth.getTransactionReceipt(txid)
print("\nAppCoins Transfer (Event):\n{}".format(
    appcoins_contract.events.Transfer().processReceipt(receipt)))
print("\nAppCoins Buy (Event):\n{}".format(
    appcoins_iab_contract.events.Buy().processReceipt(receipt)))

print_balances_appcoins()
print("\n###### END: BUY ######")
###### END: BUY ######

###### INFORM SINGLE OFFCHAIN BUY ######
print("\n\n###### INFORM SINGLE OFFCHAIN BUY ######")
print_balances_appcoins()

tx_params = appcoins_iab_contract.functions.informOffChainBuy([web3.eth.accounts[0]],[txid])\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid))
print("\nAppCoins Transfer (Transaction):\n{}".format(web3.eth.getTransaction(txid)))

receipt = web3.eth.getTransactionReceipt(txid)
print("\nAppCoins OffChainBuy (Event):\n{}".format(
    appcoins_iab_contract.events.OffChainBuy().processReceipt(receipt)))

print_balances_appcoins()
print("\n###### END: INFORM SINGLE OFFCHAIN BUY ######")
###### END: INFORM SINGLE OFFCHAIN BUY ######


