# UploadArt.py
from web3 import Web3
from solcx import compile_standard
import json
import os

# Set up Web3 connection
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # Local Ganache instance
w3.eth.defaultAccount = w3.eth.accounts[0]

# Load contract ABI and bytecode
with open('ArtworkStore.json') as f:
    contract_data = json.load(f)
    abi = contract_data['abi']
    bytecode = contract_data['evm']['bytecode']['object']

# Deploy contract
def deploy_contract():
    ArtworkContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = ArtworkContract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt.contractAddress

# Upload artwork to the blockchain
def upload_artwork(contract_address, image_url, description):
    contract = w3.eth.contract(address=contract_address, abi=abi)
    tx_hash = contract.functions.uploadArtwork(image_url, description).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    print(f"Artwork uploaded to blockchain: {image_url}")

if __name__ == '__main__':
    contract_address = deploy_contract()
    upload_artwork(contract_address, "http://example.com/generated_artwork.png", "Generated by AI from a tweet.")