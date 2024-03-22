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

    # Define initial tasks
    initial_tasks = [
        ('Scan Common Ports', scan_common_ports(target_domain)),
        ('Find Subdomains', find_subdomains),
        ('Shodan Search', shodan_search)
    ]

    # Define additional tasks
    additional_tasks = [
        ('Read Subdomains and Run FFUF', read_subdomains_and_run_ffuf, (target_domain, hosts_path, wordlist_path, results_dir)),
        ('Run Tech Stack Detection', run_tech_stack_detection, (hosts_path, results_dir)),
        # Uncomment the following line if `run_nuclei_scan` is to be included
        # ('Run Nuclei Scan', run_nuclei_scan, (hosts_path, results_dir))
    ]

    total_tasks = len(initial_tasks) + len(additional_tasks) + 1  # +1 accounts for run_httpx
    tasks_done = 0

    # Execute initial tasks
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(task, target_domain if task != shodan_search else api_key, target_domain): name for name, task in initial_tasks}
        for future in as_completed(futures):
            tasks_done += 1
            task_name = futures[future]
            try:
                future.result()
                print(f'Task {tasks_done}/{total_tasks} "{task_name}" completed.')
            except Exception as exc:
                print(f'Task {tasks_done}/{total_tasks} "{task_name}" generated an exception: {exc}')

    # Execute HTTPx separately as a bridge task
    tasks_done += 1
    try:
        run_httpx(target_domain)
        print(f'Task {tasks_done}/{total_tasks} "Run HTTPx" completed.')
    except Exception as exc:
        print(f'Task {tasks_done}/{total_tasks} "Run HTTPx" generated an exception: {exc}')

    # Execute additional tasks
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(task, *args): name for name, task, args in additional_tasks}
        for future in as_completed(futures):
            tasks_done += 1
            task_name = futures[future]
            try:
                future.result()
                print(f'Task {tasks_done}/{total_tasks} "{task_name}" completed.')
            except Exception as exc:
                print(f'Task {tasks_done}/{total_tasks} "{task_name}" generated an exception: {exc}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py [target-domain]")
        sys.exit(1)
    
    target_domain = sys.argv[1]
    main(target_domain)
