import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import chess
import chess.svg
from core.game import available_moves, execute_move
from agents.agents import create_agent
from autogen import register_function
from typing import Any

# --- Session State Initialization ---
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = None
if "anthropic_api_key" not in st.session_state:
    st.session_state.anthropic_api_key = None
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "made_move" not in st.session_state:
    st.session_state.made_move = False
if "board_svg" not in st.session_state:
    st.session_state.board_svg = None
if "move_history" not in st.session_state:
    st.session_state.move_history = []
if "max_turns" not in st.session_state:
    st.session_state.max_turns = 5

# --- Game Master Move Check ---
def check_made_move(msg: Any) -> bool:
    if st.session_state.made_move:
        st.session_state.made_move = False
        return True
    return False

# --- Streamlit Wrappers for Game Functions ---
def execute_move_streamlit(move: str) -> str:
    result = execute_move(st.session_state.board, move)
    board_svg = chess.svg.board(st.session_state.board, size=300)
    st.session_state.move_history.append(board_svg)
    st.session_state.made_move = True
    st.session_state.board_svg = board_svg
    return result

def available_moves_streamlit() -> str:
    return available_moves(st.session_state.board)

# --- Sidebar UI ---
llm_options = ["OpenAI", "Anthropic"]
white_llm = st.sidebar.selectbox("Agent White LLM", llm_options, key="white_llm")
black_llm = st.sidebar.selectbox("Agent Black LLM", llm_options, key="black_llm")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
anthropic_api_key = st.sidebar.text_input("Anthropic API Key", type="password")

if white_llm == "OpenAI" or black_llm == "OpenAI":
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("OpenAI API key saved!")
if white_llm == "Anthropic" or black_llm == "Anthropic":
    if anthropic_api_key:
        st.session_state.anthropic_api_key = anthropic_api_key
        st.sidebar.success("Anthropic API key saved!")

st.sidebar.info("""
For a complete chess game with potential checkmate, it would take max_turns > 200 approximately.
However, this will consume significant API credits and a lot of time.
For demo purposes, using 5-10 turns is recommended.
""")

max_turns_input = st.sidebar.number_input(
    "Enter the number of turns (max_turns):",
    min_value=1,
    max_value=1000,
    value=st.session_state.max_turns,
    step=1
)
if max_turns_input:
    st.session_state.max_turns = max_turns_input
    st.sidebar.success(f"Max turns of total chess moves set to {st.session_state.max_turns}!")

# --- Main Title ---
st.title("Chess with AutoGen Agents")

def get_llm_config(llm_name: str) -> list[dict]:
    if llm_name == "OpenAI":
        return [{"model": "gpt-4o-mini", "api_key": st.session_state.openai_api_key}]
    elif llm_name == "Anthropic":
        return [{
            "model": "claude-3-haiku-20240307",
            "api_key": st.session_state.anthropic_api_key,
            "base_url": "https://api.anthropic.com/v1/"
        }]
    else:
        return []

       

# --- Agent Setup and Game Logic ---
missing_keys = []
if (white_llm == "OpenAI" or black_llm == "OpenAI") and not st.session_state.openai_api_key:
    missing_keys.append("OpenAI")
if (white_llm == "Anthropic" or black_llm == "Anthropic") and not st.session_state.anthropic_api_key:
    missing_keys.append("Anthropic")

# Set Anthropic API key in environment if needed
if (white_llm == "Anthropic" or black_llm == "Anthropic") and st.session_state.anthropic_api_key:
    os.environ["ANTHROPIC_API_KEY"] = st.session_state.anthropic_api_key

if missing_keys:
    st.warning(f"Please enter the following API key(s) in the sidebar to start the game: {', '.join(missing_keys)}.")
    st.stop()
else:
    # Agent LLM configs
    agent_white_config_list = get_llm_config(white_llm)
    agent_black_config_list = get_llm_config(black_llm)

    # Create agents
    agent_white = create_agent(
        name="Agent_White",
        system_message=(
            "You are a professional chess player and you play as white. "
            "First call available_moves() to get the list of legal available moves. "
            "Then call execute_move(move) to make a move."
        ),
        config_list=agent_white_config_list,
    )
    agent_black = create_agent(
        name="Agent_Black",
        system_message=(
            "You are a professional chess player and you play as black. "
            "First call available_moves() to get the list of legal available moves. "
            "Then call execute_move(move) to make a move."
        ),
        config_list=agent_black_config_list,
    )
    game_master = create_agent(
        name="Game_Master",
        system_message="",
        config_list=[],
        check_made_move=check_made_move,
        is_game_master=True,
    )

    # Register functions for both agents
    for agent in [agent_white, agent_black]:
        register_function(
            execute_move_streamlit,
            caller=agent,
            executor=game_master,
            name="execute_move",
            description="Call this tool to make a move.",
        )
        register_function(
            available_moves_streamlit,
            caller=agent,
            executor=game_master,
            name="available_moves",
            description="Get legal moves.",
        )

    # Register nested chats for turn-taking
    agent_white.register_nested_chats(
        trigger=agent_black,
        chat_queue=[
            {
                "sender": game_master,
                "recipient": agent_white,
                "summary_method": "last_msg",
            }
        ],
    )
    agent_black.register_nested_chats(
        trigger=agent_white,
        chat_queue=[
            {
                "sender": game_master,
                "recipient": agent_black,
                "summary_method": "last_msg",
            }
        ],
    )

    # --- Info Section ---
    st.info(f"""
This chess game is played between two AG2 AI agents:
- **Agent White**: {white_llm} powered chess player controlling white pieces
- **Agent Black**: {black_llm} powered chess player controlling black pieces

The game is managed by a **Game Master** that:
- Validates all moves
- Updates the chess board
- Manages turn-taking between players
""")

    # --- Initial Board Display ---
    initial_board_svg = chess.svg.board(st.session_state.board, size=300)
    st.subheader("Initial Board")
    st.image(initial_board_svg)

    # --- Start Game Button ---
    if st.button("Start Game"):
        st.session_state.board.reset()
        st.session_state.made_move = False
        st.session_state.move_history = []
        st.session_state.board_svg = chess.svg.board(st.session_state.board, size=300)
        st.info(
            "The AI agents will now play against each other. Each agent will analyze the board, "
            "request legal moves from the Game Master (proxy agent), and make strategic decisions."
        )
        st.success(
            "You can view the interaction between the agents in the terminal output. "
            "After the turns between agents end, you get to view all the chess board moves displayed below!"
        )
        st.write("Game started! White's turn.")

        chat_result = agent_black.initiate_chat(
            recipient=agent_white,
            message="Let's play chess! You go first, it's your move.",
            max_turns=st.session_state.max_turns,
            summary_method="reflection_with_llm"
        )
        st.markdown(chat_result.summary)

        # Display the move history (boards for each move)
        st.subheader("Move History")
        for i, move_svg in enumerate(st.session_state.move_history):
            move_by = "Agent White" if i % 2 == 0 else "Agent Black"
            st.write(f"Move {i + 1} by {move_by}")
            st.image(move_svg)

    # --- Reset Game Button ---
    if st.button("Reset Game"):
        st.session_state.board.reset()
        st.session_state.made_move = False
        st.session_state.move_history = []
        st.session_state.board_svg = None
        st.write("Game reset! Click 'Start Game' to begin a new game.")