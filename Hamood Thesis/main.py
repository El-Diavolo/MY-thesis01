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
    run_tech_stack_detection
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

    initial_tasks = [
        ('Scan Common Ports', scan_common_ports, target_domain),
        ('Find Subdomains', find_subdomains, target_domain),
        ('Shodan Search', shodan_search, api_key, target_domain)
    ]

    additional_tasks = [
        ('Read Subdomains and Run FFUF', read_subdomains_and_run_ffuf, target_domain, hosts_path, wordlist_path, results_dir),
        ('Run Tech Stack Detection', run_tech_stack_detection, hosts_path, results_dir)
        # ('Run Nuclei Scan', run_nuclei_scan, hosts_path, results_dir) # Uncomment if needed
    ]

    total_tasks = len(initial_tasks) + len(additional_tasks)
    tasks_done = 0

    # Execute initial tasks concurrently
    with ThreadPoolExecutor() as executor:
        future_to_task = {}
        for i, task_info in enumerate(initial_tasks, 1):
            print(f'Task {i}/{total_tasks} "{task_info[0]}" started.')
            future = executor.submit(task_info[1], *task_info[2:])
            future_to_task[future] = (i, task_info[0])

        for future in as_completed(future_to_task):
            i, task_name = future_to_task[future]
            try:
                future.result()
                print(f'Task {i}/{total_tasks} "{task_name}" completed.')
                tasks_done += 1
            except Exception as exc:
                print(f'Task {i}/{total_tasks} "{task_name}" generated an exception: {exc}')

    # Execute additional tasks concurrently
    
    ('Run HTTPx', run_httpx, target_domain)
    with ThreadPoolExecutor() as executor:
        future_to_task = {}
        for i, task_info in enumerate(additional_tasks, tasks_done + 1):
            print(f'Task {i}/{total_tasks} "{task_info[0]}" started.')
            future = executor.submit(task_info[1], *task_info[2:])
            future_to_task[future] = (i, task_info[0])

        for future in as_completed(future_to_task):
            i, task_name = future_to_task[future]
            try:
                future.result()
                print(f'Task {i}/{total_tasks} "{task_name}" completed.')
            except Exception as exc:
                print(f'Task {i}/{total_tasks} "{task_name}" generated an exception: {exc}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py [target-domain]")
        sys.exit(1)
    
    target_domain = sys.argv[1]
    main(target_domain)
