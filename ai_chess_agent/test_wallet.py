import streamlit as st
from wallet_connect import wallet_connect

st.header("Connect your Wallet")
address = wallet_connect(label="wallet", key="e9014cd42fa6f9eb318412afee47f1f7")
if address and address != "not":
    st.success(f"Connected: {address}")
else:
    st.warning("Please connect your wallet to continue.")