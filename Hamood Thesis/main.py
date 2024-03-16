""" Import modules from config/modules folder
- Import Tools
- Import Installer (main.py --install to run, use argparse)
- Have a menu to display tools, use RICH to create tables
- Output results from scanners to reports directory (for nmap do -oA)

https://docs.python.org/3/tutorial/modules.html
"""

from modules.web.sublist3r import find_subdomains
from config import setup, functionality
import subprocess
import sys
import os

WORDLISTS_DIR = "/usr/share/wordlists/dirb/"

def find_subdomains_with_sublist3r(target_domain):
    """
    Finds subdomains for the given target domain using Sublist3r.
    """
    if not target_domain:
        print("Usage: python3 main.py [target-domain]")
        return

    # Find subdomains using Sublist3r
    print(f"[*] Finding subdomains for {target_domain} using Sublist3r...")
    subdomains = find_subdomains(target_domain)
    if subdomains:
        print(f"Found subdomains for {target_domain}:")
        for subdomain in subdomains:
            print(subdomain)
    else:
        print(f"No subdomains found for {target_domain}.")


def main(target_domain):
    print('hlo')
    if not target_domain:
        print("Usage: python3 script.py [target-domain]")
    else:
        find_subdomains_with_sublist3r(target_domain)
        return

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py [target-domain]")
        sys.exit(1)
    target_domain = sys.argv[1]
    main(target_domain)

