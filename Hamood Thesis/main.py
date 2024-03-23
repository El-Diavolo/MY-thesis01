import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Assuming these functions are defined in the imported modules
from modules.web import (
    find_subdomains,
    read_subdomains_and_run_ffuf,
    run_httpx,
    shodan_search,
    run_nuclei_scan,
    run_tech_stack_detection,
    run_eyewitness
)
from modules.network import scan_common_ports

# Paths configuration
wordlist_path = '/workspaces/MY-thesis01/Hamood Thesis/test/testwordlist.txt'
hosts_path = "/workspaces/MY-thesis01/Hamood Thesis/results/hosts"
results_dir = "/workspaces/MY-thesis01/Hamood Thesis/results/directories"

# API keys
api_key = 'rzmg0Qy3yK0Cuh6AJXiUtEzQaaByNdtY'

def main(target_domain):
    print(f'Starting scans for: {target_domain}')

    task_list = [
        ('Scan Common Ports', scan_common_ports, target_domain),
        ('Find Subdomains', find_subdomains, target_domain),
        ('Shodan Search', shodan_search, (api_key, target_domain)),
        ('Run HTTPx', run_httpx, target_domain),
        ('Read Subdomains and Run FFUF', read_subdomains_and_run_ffuf, (target_domain, hosts_path, wordlist_path, results_dir)),
        ('Run Tech Stack Detection', run_tech_stack_detection, (hosts_path, 'results/techstack')),
        ('Running Screenshotter', run_eyewitness, (hosts_path, 'results/screenshots'))
        # Add 'Run Nuclei Scan' task if needed
    ]

    with ThreadPoolExecutor() as executor:
        futures_to_task = {executor.submit(task[1], *(task[2] if isinstance(task[2], tuple) else (task[2],))): task[0] for task in task_list}
        
        completed_tasks = 0
        for future in as_completed(futures_to_task):
            completed_tasks += 1
            task_name = futures_to_task[future]
            try:
                future.result()
                print(f'Task {completed_tasks}/{len(task_list)} "{task_name}" completed.')
            except Exception as exc:
                print(f'Task {completed_tasks}/{len(task_list)} "{task_name}" generated an exception: {exc}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py [target-domain]")
        sys.exit(1)
    
    target_domain = sys.argv[1]
    main(target_domain)