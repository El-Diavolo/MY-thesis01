""" Import modules from config/modules folder
- Import Tools
- Import Installer (main.py --install to run, use argparse)
- Have a menu to display tools, use RICH to create tables
- Output results from scanners to reports directory (for nmap do -oA)

https://docs.python.org/3/tutorial/modules.html
"""

import modules
from config import setup, functionality

print('HELLO')

run_scans()
