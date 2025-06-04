# 🎮 AI Chess Agents with Blockchain Betting

A sophisticated chess game platform where two AI agents play against each other using AutoGen, with integrated blockchain-based betting functionality. Watch as GPT-4 and Claude battle it out on the chess board while you place bets on the outcome!

![Chess Game](https://img.shields.io/badge/Chess-AI%20Agents-brightgreen)
![Blockchain](https://img.shields.io/badge/Ethereum-Betting-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-orange)

## 🌟 Features

### 🤖 Multi-Agent Architecture
- **Agent White**: LLM-powered strategic decision maker (OpenAI or Anthropic)
- **Agent Black**: LLM-powered tactical opponent (OpenAI or Anthropic)
- **Game Master**: Validation agent for move legality and game state management

### 🔒 Safety & Validation
- Robust move verification system
- Illegal move prevention
- Real-time board state monitoring
- Secure game progression control

### ♟️ Strategic Gameplay
- AI-powered position evaluation
- Deep tactical analysis
- Dynamic strategy adaptation
- Complete chess ruleset implementation

### 💰 Blockchain Betting System
- Place bets on either Agent White or Agent Black
- Ethereum-based smart contract (Sepolia testnet)
- Proportional payouts for winners
- Secure settlement mechanism

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key and/or Anthropic API key
- MetaMask wallet (for betting functionality)
- Sepolia testnet ETH (for betting functionality)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/chessgame.git
cd chessgame
```

2. Create and activate a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies
```bash
pip install -r ai_chess_agent/requirements.txt
```

4. Get your API keys
- Sign up for an [OpenAI account](https://platform.openai.com/) to get an API key
- Sign up for an [Anthropic account](https://www.anthropic.com/) to get an API key (optional)

## 🎮 Running the Application

### Chess Game
Run the Streamlit app:
```bash
cd ai_chess_agent
streamlit run ui/app.py
```

### Betting Interface
Run the betting interface:
```bash
cd ai_chess_agent
streamlit run ui/bet_app.py
```

## 🎯 How to Use

### Chess Game

<img width="1440" alt="Screenshot 2025-06-04 at 7 43 26 PM" src="https://github.com/user-attachments/assets/6a11b76e-ff6d-46ae-aa0e-f0853452cd01" />

<img width="1440" alt="Screenshot 2025-06-04 at 7 44 00 PM" src="https://github.com/user-attachments/assets/bac957a1-b866-4d4b-968e-ece118bc4b81" />

1. Enter your OpenAI and/or Anthropic API keys in the sidebar
2. Select which LLM to use for each agent (OpenAI or Anthropic)
3. Set the maximum number of turns for the game
4. Click "Start Game" to watch the AI agents play chess

### Placing Bets

<img width="1440" alt="Screenshot 2025-06-04 at 7 46 21 PM" src="https://github.com/user-attachments/assets/d909e542-8556-40b6-8352-530c39eae85b" />

<img width="1440" alt="Screenshot 2025-06-04 at 7 46 46 PM" src="https://github.com/user-attachments/assets/321e9cc6-5fa7-4fc6-b039-d220c514a450" />


1. Connect your MetaMask wallet to the betting interface
2. Enter the Game ID you want to bet on
3. Choose which agent to bet on (White or Black)
4. Enter the amount of ETH to stake
5. Click "Place Bet" and confirm the transaction in MetaMask

### Settling Bets (Owner Only)
1. Enter the Game ID to settle
2. Select which agent won the game
3. Click "Settle Game" and confirm the transaction in MetaMask

## 🏗️ Architecture

The project is structured as follows:

- `ui/` - Streamlit user interfaces
  - `app.py` - Main chess game UI
  - `bet_app.py` - Blockchain betting UI
- `core/` - Chess game logic
  - `game.py` - Move validation and board management
- `agents/` - AutoGen agent definitions
  - `agents.py` - Agent creation and configuration
- `blockchain.py` - Web3 integration for blockchain functionality
- `bet.sol` - Solidity smart contract for betting

## 🔗 Smart Contract

The betting functionality is powered by a custom Ethereum smart contract deployed on the Sepolia testnet. The contract allows users to:

1. Place bets on either Agent White or Agent Black
2. Receive proportional payouts when their chosen agent wins
3. Participate in a transparent, decentralized betting system

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [AutoGen](https://github.com/microsoft/autogen) for the multi-agent framework
- [python-chess](https://github.com/niklasf/python-chess) for chess logic
- [Streamlit](https://streamlit.io/) for the user interface
- [Web3.py](https://web3py.readthedocs.io/) for blockchain integration

