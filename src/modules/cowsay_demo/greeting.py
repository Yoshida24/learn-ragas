from modules.message_demo.message import (
    build_greet_message,
    build_default_greet_message_from_env,
)
import cowsay


def greet_to(your_name: str) -> None:
    """_summary_

    Args:
        your_name (str): _description_
    """
    greet = build_greet_message(your_name=your_name)
    cowsay.cow(greet)


def greet_from_env() -> None:
    """_summary_

    Args:
        your_name (str): _description_
    """
    greet = build_default_greet_message_from_env()
    cowsay.cow(greet)
