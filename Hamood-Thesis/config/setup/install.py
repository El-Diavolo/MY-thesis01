"""
Script to install the program
- Set up Virtual Environment
- Install requirements
- Check updates
- Update program

https://hackthology.com/how-to-write-self-updating-python-programs-using-pip-and-git.html
"""
import subprocess as sp
from getopt import getopt, GetoptError
from config.functionality import colours
from config.logging import logging


def install_util():
    """ Install the python program
    - Create venv if not exists
    - Install requirements.txt libraries
    """
    pass


def status_util():
    """ Check GitHub status
    - Detect changes
    - Inform user of updates if exists
    """
    pass


def update_util():
    """ Update program
    - If ran, run status_util
    - If status_util == True then update program
    """
    pass

