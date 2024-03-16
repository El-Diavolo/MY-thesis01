""" Import modules from config/modules folder
- Import Tools
- Import Installer (main.py --install to run, use argparse)
- Have a menu to display tools, use RICH to create tables
- Output results from scanners to reports directory (for nmap do -oA)

https://docs.python.org/3/tutorial/modules.html
"""

from modules.web import *

from config import setup, functionality
import subprocess
import sys
import os

##wordlist_path = '/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt'
wordlist_path = '/workspaces/MY-thesis01/Hamood Thesis/test/testwordlist.txt'
directory_path = "/workspaces/MY-thesis01/Hamood Thesis/results/subdomains"
results_dir = "/workspaces/MY-thesis01/Hamood Thesis/results/directories"

def main(target_domain):
    print('hlo')
    if not target_domain:
        print("Usage: python3 script.py [target-domain]")
    else:
        find_subdomains(target_domain)
        read_subdomains_and_run_ffuf(directory_path , wordlist_path ,results_dir)
        return

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py [target-domain]")
        sys.exit(1)
    target_domain = sys.argv[1]
    main(target_domain)

