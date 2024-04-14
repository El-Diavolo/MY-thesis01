import logging
import sys
import os
from rich.logging import RichHandler

debug_path = "logs/debug_logs.log"
if not os.path.exists(debug_path):
    with open(debug_path, 'w'): pass  

logging.basicConfig(
    level="NOTSET", 
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True),
        # logging.StreamHandler(sys.stdout),
        logging.FileHandler(debug_path, mode='a'),
    ],
)

log = logging.getLogger("rich")


def error(function):
    log.error(f"[red on grey]{function}[/red on grey]", extra={"markup": True})


def exception_error(function):
    log.exception(f"[red on grey]{function}[/red on grey]", extra={"markup": True})


def info(function):
    log.info(f"[cornflower_blue]{function}[/cornflower_blue]", extra={"markup": True})
    