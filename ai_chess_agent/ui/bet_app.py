import streamlit as st
import json
from web3 import Web3
from wallet_connect import wallet_connect

# Load contract ABI and address
CONTRACT_JSON_PATH = "./ui/BetManager.json"
PROVIDER_URL = "https://eth-sepolia.g.alchemy.com/v2/MS9pGRxd1Jh3rhVjyIkFzVfG1g3BcTk3"

@st.cache_resource
def load_contract():
    with open(CONTRACT_JSON_PATH, "r") as f:
        data = json.load(f)
    abi = data["abi"]
    address = data["address"]
    w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
    contract = w3.eth.contract(address=address, abi=abi)
    return w3, contract, address

w3, contract, contract_address = load_contract()

# --- Wallet Connect ---
st.header("Connect your Wallet")
address = wallet_connect(label="wallet", key="wallet")
if address and address != "not":
    st.success(f"Connected: {address}")
else:
    st.warning("Please connect your wallet to continue.")

# --- Place Bet UI ---
st.header("Place a Bet on Chess Game")
game_id = st.number_input("Game ID", min_value=0, step=1)
on_white = st.radio("Bet on", ["Agent White", "Agent Black"]) == "Agent White"
stake_eth = st.number_input("Stake (ETH)", min_value=0.01, step=0.01, format="%.2f")

if st.button("Place Bet", disabled=not (address and address != "not")):
    if not address or address == "not":
        st.error("Connect your wallet first.")
    else:
        try:
            # Build the transaction data for placeBet function
            tx_data = contract.functions.placeBet(game_id, on_white).build_transaction({
                "from": address,
                "value": w3.to_wei(stake_eth, "ether"),
                "nonce": w3.eth.get_transaction_count(address),
                "gas": 300000,
                "gasPrice": w3.eth.gas_price,
            })
            
            st.info("Transaction built successfully. Please use MetaMask to send this transaction:")
            st.json({
                "to": tx_data["to"],
                "value": tx_data["value"],
                "data": tx_data["data"],
                "gas": tx_data["gas"]
            })
            st.write("**Instructions:** Copy the above transaction details and paste them into MetaMask manually, or use the MetaMask extension to send the transaction.")
            
        except Exception as e:
            st.error(f"Error building transaction: {e}")

# --- Settle Game UI (Owner Only) ---
st.header("Settle Game (Owner Only)")
settle_game_id = st.number_input("Settle Game ID", min_value=0, step=1, key="settle_id")
white_won = st.radio("Which agent won?", ["Agent White", "Agent Black"]) == "Agent White"

if st.button("Settle Game", disabled=not (address and address != "not")):
    if not address or address == "not":
        st.error("Connect your wallet first.")
    else:
        try:
            # Build the transaction data for settle function
            tx_data = contract.functions.settle(settle_game_id, white_won).build_transaction({
                "from": address,
                "nonce": w3.eth.get_transaction_count(address),
                "gas": 300000,
                "gasPrice": w3.eth.gas_price,
            })
            
            st.info("Settlement transaction built successfully. Please use MetaMask to send this transaction:")
            st.json({
                "to": tx_data["to"],
                "data": tx_data["data"],
                "gas": tx_data["gas"]
            })
            st.write("**Instructions:** Copy the above transaction details and paste them into MetaMask manually, or use the MetaMask extension to send the transaction.")
            
        except Exception as e:
            st.error(f"Error building settlement transaction: {e}")

# --- Alternative: Manual Transaction Entry ---
st.header("Alternative: Manual Transaction")
st.write("If the wallet connect doesn't work, you can:")
st.write("1. Copy your wallet address and private key")
st.write("2. Use web3.py to send transactions directly")

manual_address = st.text_input("Wallet Address (for manual transactions)")
manual_private_key = st.text_input("Private Key (for manual transactions)", type="password")

if manual_address and manual_private_key:
    if st.button("Send Manual Bet Transaction"):
        try:
            # Build and sign transaction manually
            tx = contract.functions.placeBet(game_id, on_white).build_transaction({
                "from": manual_address,
                "value": w3.to_wei(stake_eth, "ether"),
                "nonce": w3.eth.get_transaction_count(manual_address),
                "gas": 300000,
                "gasPrice": w3.eth.gas_price,
            })
            signed_tx = w3.eth.account.sign_transaction(tx, manual_private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            st.success(f"Manual transaction sent! Hash: {tx_hash.hex()}")
        except Exception as e:
            st.error(f"Manual transaction failed: {e}") 