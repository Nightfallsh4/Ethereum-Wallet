from web3 import Web3
from seed_gen import *
from start import *
import os, time

# url = "https://ropsten.infura.io/v3/xxxxxxxxxxxxxxxxxxxxx" Changing this url will make the program use the ropsten global testnet of ethereum
url = "HTTP://127.0.0.1:7545" #this is the ip address of the local testnet node
w3 = Web3(Web3.HTTPProvider(url))
#Asks to open existing wallet or create new wallet
while True:
    os.system('clear')
    start()
    print("To create new wallet press 'c'   To access existing wallet press 'a'     To restore wallet from mnemonic press 'r'\n")
    cmd = str(input("Enter you command- "))
    if cmd == "c":
        account = Eth_Accounts()
        account.create_account()
        time.sleep(5)
        os.system('clear')
    elif cmd == 'x':
        break
    elif cmd == 'r':
        account = Eth_Accounts()
        account.restore_account()
        print("Continue by normally accessing your wallet")
        time.sleep(5)
        os.system("clear")
    elif cmd == "a":
        account = Eth_Accounts()
        address, salt, encrypted_private_key = account.access_wallet()
        while True:
            balance = w3.eth.getBalance(address)
            os.system("clear")
            start()
            print("\n\nYour Account address- ", address)
            print("\n Your Ethereum Balance- ", w3.fromWei(balance, "ether"),"ETH\n")
            while True:
                cmd2 = str(input("To send ETH to an address press 's'   To go back press 'b' - "))
                print("\n")
                while True:
                    if cmd2 == 's':
                        try:
                            send_address = str(input("Enter the address you want to send to- "))
                            send_value = float(input("Enter the amount of ETH you want to send- "))
                        except:
                            print("Enter only numbers to send like 1.0 or 2.5")
                            continue
                        
                        if balance<send_value:
                            print(f"The amount you have enter is greater than the amount in your wallet\nYour balance is {balance}\n")
                            continue
                        nonce = w3.eth.getTransactionCount(address)
                        tx = {
                            "nonce": nonce,
                            "to":send_address,
                            "value": w3.toWei(send_value, "ether"),
                            "gas": 2000000,
                            "gasPrice": w3.toWei("50", "gwei")
                        }
                        password = str(input("Enter your password- "))
                        private_key = decrypt_arb(encrypted_private_key, password, salt)
                        signed_tx = w3.eth.account.signTransaction(tx, private_key)
                        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
                        del private_key
                        print()
                        print("Transaction Sent!!")
                        print("Transaction hash- ",w3.toHex(tx_hash),"\n")
                        time.sleep(5)
                        break
                    elif cmd2 == 'b':
                        break
                break
            if cmd2 == 'b':
                break
            

#if new wallet should ask for name of wallet and password 
    #create a wallet encrypted json keyfile with the address 
    #   and private key opened with spending password.
#if open existing wallet- should load the keyfile, 
    # decrypt the wallet using wallet password
    # and show balance with the address
#should be able to get input of transaction, sign and send transactions
