# Ethereum-Wallet
An Ethereum wallet Created in python using Web3 library

This wallet is built to run in the linux terminal. 

It is a full fledged wallet which created new wallets, access existing wallets and restore wallets with mnemonic phrases.

It has been tested in the Ganache local testnet and Ropsten testnet of the Ethereum blockchain and works well in both the cases.

The private is never stored in an unencrypted form. And is encrypted before storing using AES encrption with 256 Bits keys derived from password using a key derivation function.
