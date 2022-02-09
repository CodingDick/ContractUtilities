import json
import argparse

#Third Party
from web3 import Web3
from web3.contract import Contract


#Load abi-Data Contract Interface
with open('./abi.json', 'r') as f:
    abi_data = json.load(f)

NODE_URL = 'https://speedy-nodes-nyc.moralis.io/6ece42cb4ab9cc0a84eb349f/polygon/mainnet'
#Establish web3js API with Contract
WEB3 = Web3(Web3.HTTPProvider(NODE_URL))
contract: Contract = None

def get_next_token(index):
    """ Returns the tokenID for an index"""
    return contract.functions.tokenByIndex(index).call()

def get_owner_of_token_id(token_id):
    """ Returns the owner address for a tokenId"""
    return contract.functions.ownerOf(token_id).call()

def get_current_supply():
    """ Returns the current supply"""
    return contract.functions.totalSupply().call()
    

def get_first_holders(max_holders):
    """Returns a List of distinct onwer addresses.\n
    Under condition to check max wanted holders and current supply.
    """
    index = 0 #Counter for current index
    current_supply = get_current_supply()
    found_owners = []
    #Loop through all tokens until we found max_holders or run out of token supply.
    while len(found_owners) < max_holders and index < current_supply:
        token_id = get_next_token(index)
        owner = get_owner_of_token_id(token_id)
        if owner not in found_owners:
            found_owners.append(owner)
        index += 1
    return found_owners

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get first X Holders')
    parser.add_argument("--contract-address", type=str)
    parser.add_argument("--amount-holders", type=int)
    args = parser.parse_args()
    contract = WEB3.eth.contract(address=Web3.toChecksumAddress(args.contract_address.lower()), abi=abi_data)
    holders = get_first_holders(args.amount_holders)
    for holder in holders:
        print(holder)