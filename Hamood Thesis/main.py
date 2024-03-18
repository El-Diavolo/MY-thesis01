import sys
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# Assuming these functions are defined in the imported modules
from modules.web import find_subdomains, read_subdomains_and_run_ffuf , run_httpx , shodan_search
from modules.network import scan_common_ports

# Paths configuration
wordlist_path = '/workspaces/MY-thesis01/Hamood Thesis/test/testwordlist.txt'
hosts_path = "/workspaces/MY-thesis01/Hamood Thesis/results/hosts"
results_dir = "/workspaces/MY-thesis01/Hamood Thesis/results/directories"

#api keys
api_key = 'rzmg0Qy3yK0Cuh6AJXiUtEzQaaByNdtY'

def main(target_domain):
    print('Starting scans for:', target_domain)

    # Use ThreadPoolExecutor to execute multiple tasks concurrently
    with ThreadPoolExecutor() as executor:
        # Submit tasks
        future_scan = executor.submit(scan_common_ports, target_domain)
        future_subdomains = executor.submit(find_subdomains, target_domain)
        future_shodan = executor.submit(shodan_search, api_key, target_domain)

        # As tasks complete, print their result
        for future in as_completed([future_scan, future_subdomains, future_shodan]):
            try:
                data = future.result()
                print(f'Task completed with result: {data}')
            except Exception as exc:
                print(f'Task generated an exception: {exc}')
    
    # After concurrent tasks, proceed with other tasks that depend on their results
    shodan_search(api_key,target_domain)
    run_httpx(target_domain)
    read_subdomains_and_run_ffuf(target_domain,hosts_path, wordlist_path, results_dir)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py [target-domain]")
        sys.exit(1)
    
    target_domain = sys.argv[1]
    main(target_domain)
