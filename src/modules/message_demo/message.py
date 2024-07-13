import os


def build_greet_message(your_name: str | None = None) -> str:
    """_summary_
    Args:
        your_name (str): _description_

    Returns:
        str: _description_
    """
    return f"Hello, {your_name}!"


def build_default_greet_message_from_env() -> str:
    """_summary_
    Args:
        your_name (str): _description_

    Returns:
        str: _description_
    """
    your_name = os.environ.get("YOUR_DEFAULT_NAME")
    return f"Hello, {your_name}!"
