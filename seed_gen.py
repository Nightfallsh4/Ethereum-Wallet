from mnemonic import Mnemonic
from eth_account import Account
import os, time
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
from start import *
class Eth_Accounts():
    def __init__(self):
        pass

    def create_account(self):
        self.filename = str(input("Enter the name of the account you want to create- "))
        while True:
            self.password = str(input("Enter a password for your account- "))
            confirm_password = str(input("Re-enter your password to confirm- "))
            if self.password != confirm_password:
                print("The password entered and the confirmation is not the same\n\nEnter password again ")
                time.sleep(3)
            else:
                print("\nPassword set successfully!!\n")
                break
        Account.enable_unaudited_hdwallet_features()
        acct, self.mnemonic = Account.create_with_mnemonic()

        while True:
            print("New wallet created\n")
            print("Write down the seed phrases given below carefully \n(if you loose the seed phrases you'll loose all access to your crypto)\n")
            print("*"+self.mnemonic+"*"+"\n")
            c = str(input("Have you written down the seed phrases carefully and double checked? (Y/N)? - "))
            if c.lower() == 'y':
                os.system('clear')
                break

        #print(acct.key.hex())
        start()
        self.address = acct.address
        #print(self.address)
        self.salt = os.urandom(16)
        self.encrypted_private_key = encrypt_arb(message = acct.key, password=self.password, salt=self.salt)
        #print(self.encrypted_private_key)
        
        data = {"address":self.address, "salt":self.salt.hex(), "encrypted_private_key":self.encrypted_private_key.decode(),
        "cipher code":"kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=390000,)  \n key = base64.urlsafe_b64encode(kdf.derive(password.encode()))   \nf = Fernet(key)   \nf.decrypt(message)"}
        with open(f"{self.filename}.json", 'w') as f:
            json.dump(data, f)
        del acct
        del self.mnemonic
        print("\nNew wallet created and json keyfile is saved in the given wallet name\n")


    def restore_account(self):
        self.filename = str(input("Enter the name of the account you want to create- "))
        m = str(input("Enter mnemonic- "))
        while True:
            self.password = str(input("Enter a password for your account- "))
            confirm_password = str(input("Re-enter your password to confirm- "))
            if self.password != confirm_password:
                print("The password entered and the confirmation is not the same\n\nEnter password again ")
                time.sleep(3)
            else:
                print("\nPassword set successfully!!\n")
                break
        Account.enable_unaudited_hdwallet_features()
        acct = Account.from_mnemonic(m)
        self.address = acct.address
        #print(self.address)
        self.salt = os.urandom(16)
        self.encrypted_private_key = encrypt_arb(message = acct.key, password=self.password, salt=self.salt)
        #print(self.encrypted_private_key)
        
        data = {"address":self.address, "salt":self.salt.hex(), "encrypted_private_key":self.encrypted_private_key.decode(),
        "cipher code":"kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=390000,)  \n key = base64.urlsafe_b64encode(kdf.derive(password.encode()))   \nf = Fernet(key)   \nf.decrypt(message)"}
        with open(f"{self.filename}.json", 'w') as f:
            json.dump(data, f)
        os.system('clear')
        start()
        print("\nNew wallet created from mnemonic and json keyfile is saved in the given wallet name\n")
        del acct
        del m 


    def access_wallet(self):
        while True:
            name = str(input("Enter name of the wallet keyfile- "))
            filename = name +".json"
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
            except:
                print(f"No JSON file in the name of {filename} exists")
            else:
                break
        return data['address'], bytes(16).fromhex(data['salt']), data['encrypted_private_key'].encode()
        


def encrypt_arb(message, password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    #print("encryption key- ",key)
    f = Fernet(key)
    return f.encrypt(message)


def decrypt_arb(message, password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    #print("encryption key- ",key)
    f = Fernet(key)
    return f.decrypt(message).hex()
