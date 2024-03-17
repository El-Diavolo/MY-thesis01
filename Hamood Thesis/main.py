import sys
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# Assuming these functions are defined in the imported modules
from modules.web import find_subdomains, read_subdomains_and_run_ffuf , run_httpx
from modules.network import scan_common_ports

# Paths configuration
wordlist_path = '/workspaces/MY-thesis01/Hamood Thesis/test/testwordlist.txt'
hosts_path = "/workspaces/MY-thesis01/Hamood Thesis/results/hosts"
results_dir = "/workspaces/MY-thesis01/Hamood Thesis/results/directories"

def main(target_domain):
    print('Starting scans for:', target_domain)
    
    # Define tasks to run concurrently
    tasks = [scan_common_ports, find_subdomains]
    
    # Use ThreadPoolExecutor to execute multiple tasks concurrently
    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        # Dictionary to hold future tasks
        future_task = {executor.submit(task, target_domain): task for task in tasks}
        
        for future in as_completed(future_task):
            task = future_task[future]
            try:
                data = future.result()
            except Exception as exc:
                print(f'{task.__name__} generated an exception: {exc}')
            else:
                print(f'{task.__name__} completed with result: {data}')
    
    # After concurrent tasks, proceed with other tasks that depend on their results
    run_httpx(target_domain)
    read_subdomains_and_run_ffuf(target_domain,hosts_path, wordlist_path, results_dir)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py [target-domain]")
        sys.exit(1)
    
    target_domain = sys.argv[1]
    main(target_domain)
