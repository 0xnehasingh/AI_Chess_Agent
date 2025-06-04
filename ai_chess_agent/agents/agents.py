from autogen import ConversableAgent, register_function
from typing import Any, Callable, Dict


def create_agent(
    name: str,
    system_message: str,
    config_list: list[dict[str, Any]],
    check_made_move: Callable[[str], bool] = None,
    is_game_master: bool = False,
) -> ConversableAgent:
    llm_config = {"config_list": config_list, "cache_seed": None} if not is_game_master else False
    agent = ConversableAgent(
        name=name,
        system_message=system_message if not is_game_master else None,
        llm_config=llm_config,
        is_termination_msg=check_made_move if is_game_master else None,
        default_auto_reply="Please make a move." if is_game_master else None,
        human_input_mode="NEVER" if is_game_master else None,
    )
    return agent 