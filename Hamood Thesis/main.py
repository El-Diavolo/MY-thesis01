""" Import modules from config/modules folder
- Import Tools
- Import Installer (main.py --install to run, use argparse)
- Have a menu to display tools, use RICH to create tables
- Output results from scanners to reports directory (for nmap do -oA)

https://docs.python.org/3/tutorial/modules.html
"""

import modules
from config import setup, functionality

print('hello')

def main(domain):
    # Get a list of subdomains using sublist3r
    subdomains = find_subdomains(domain)
    
    # Run ffuf on each subdomain
    for subdomain in subdomains:
        print(f"Fuzzing {subdomain}...")
        run_ffuf(subdomain)

if __name__ == "__main__":
    domain = "example.com"
    main(domain)

