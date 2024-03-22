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

#api keys
api_key = 'rzmg0Qy3yK0Cuh6AJXiUtEzQaaByNdtY'

def main(target_domain):
    print(f'Starting scans for: {target_domain}')

    tasks_done = 0
    initial_tasks = [scan_common_ports, find_subdomains, shodan_search]
    additional_tasks = [run_nuclei_scan, read_subdomains_and_run_ffuf, run_tech_stack_detection]
    total_tasks = len(initial_tasks) + len(additional_tasks) + 1  # +1 for run_httpx

    # Initial tasks to run concurrently
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(task, target_domain): task for task in initial_tasks}
        futures[executor.submit(run_httpx, target_domain)] = run_httpx  # Adding run_httpx as an initial task

        for future in as_completed(futures):
            tasks_done += 1
            try:
                future.result()
                print(f'Task {tasks_done}/{total_tasks} is done')
            except Exception as exc:
                print(f'Task {tasks_done}/{total_tasks} generated an exception: {exc}')

    # Additional tasks to run concurrently after httpx
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(task, hosts_path, results_dir) if task != read_subdomains_and_run_ffuf
                   else executor.submit(task, target_domain, hosts_path, wordlist_path, results_dir)
                   for task in additional_tasks}

        for future in as_completed(futures):
            tasks_done += 1
            try:
                future.result()
                print(f'Task {tasks_done}/{total_tasks} is done')
            except Exception as exc:
                print(f'Task {tasks_done}/{total_tasks} generated an exception: {exc}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py [target-domain]")
        sys.exit(1)
    
    target_domain = sys.argv[1]
    main(target_domain)