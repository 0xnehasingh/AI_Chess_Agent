import json
import asyncio
from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from typing import Any

# Load contract ABI and address from a JSON file
async def load_contract(json_path: str, provider_url: str) -> Any:
    with open(json_path, 'r') as f:
        data = json.load(f)
    abi = data['abi']
    address = data['address']
    w3 = Web3(AsyncHTTPProvider(provider_url), modules={"eth": (AsyncEth,)}, middlewares=[])
    contract = w3.eth.contract(address=address, abi=abi)
    return w3, contract

# Place a bet (async)
async def place_bet(w3: Web3, contract: Any, account: str, private_key: str, game_id: int, on_white: bool, stake_eth: float) -> str:
    nonce = await w3.eth.get_transaction_count(account)
    tx = contract.functions.placeBet(game_id, on_white).build_transaction({
        'from': account,
        'value': w3.to_wei(stake_eth, 'ether'),
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': await w3.eth.gas_price
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = await w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

# Settle a game (async)
async def settle_game(w3: Web3, contract: Any, account: str, private_key: str, game_id: int, white_won: bool) -> str:
    nonce = await w3.eth.get_transaction_count(account)
    tx = contract.functions.settle(game_id, white_won).build_transaction({
        'from': account,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': await w3.eth.gas_price
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = await w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex() 