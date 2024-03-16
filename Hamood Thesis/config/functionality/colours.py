"""
https://docs.python.org/3/library/logging.html#levels
https://docs.python.org/3/library/logging.html#logging.debug
"""


from rich.style import Style
from rich.console import Console
from rich.prompt import Prompt


console = Console(
    color_system="auto",
    record=True
)

style = Style()
prompt = Prompt()


def success(function):
    console.print(f"[+] {function}", style="green")


def server_prompt():
    return console.input("[grey54]ACHERON :bird:[/grey54]> ")


def quit_input():
    return prompt.ask(":warning:\nExit Program?",
                      choices=["yes", "no"], default="no")


def client_msg_recv(nickname, message):
    console.print(f"{nickname}: {message}", style="hot_pink3")


def bot_msg_recv():
    pass


def process(function):
    console.print(f"[*] {function}", style="yellow")


def separator():
    console.print("".center(80, "="), style="medium_violet_red")
