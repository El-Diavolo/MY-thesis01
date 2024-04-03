import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


from modules.web import (
    find_subdomains,
    read_subdomains_and_run_ffuf,
    run_httpx,
    shodan_search,
    run_nuclei_scan,
    run_tech_stack_detection,
    run_eyewitness,
    run_gospider
)
from modules.network import scan_common_ports

# Paths configuration
wordlist_path = 'test/testwordlist.txt'
hosts_path = "results/hosts"
results_dir = "results/directories"
subdomains_dir = 'results/subdomains'

# API keys
api_key = 'rzmg0Qy3yK0Cuh6AJXiUtEzQaaByNdtY'

def main(target_domain):
    print(f'Starting scans for: {target_domain}')

    # Phase 1: Concurrent execution of initial tasks
    initial_tasks = [
        ('Scan Common Ports', scan_common_ports, (target_domain,)),
        ('Find Subdomains', find_subdomains, (target_domain,)),
        ('Shodan Search', shodan_search, (api_key, target_domain)),
        ('gospider' , run_gospider, (target_domain,))
    ]

    
    httpx_task = ('Run HTTPx', run_httpx, (subdomains_dir,))

    # Phase 3: Concurrent execution of additional tasks
    additional_tasks = [
        ('Read Subdomains and Run FFUF', read_subdomains_and_run_ffuf, (target_domain, hosts_path, wordlist_path, 'results/directories')),
        ('Run Tech Stack Detection', run_tech_stack_detection, (hosts_path, 'results/techstack')),
        #('Running Screenshotter', run_eyewitness, ('results/subdomains', 'results/screenshots')),
        #('Run Nuclei Scan', run_nuclei_scan, (hosts_path, 'results/nuclei'))
    ]

    # Execute tasks
    execute_tasks(initial_tasks, "Phase 1: Initial Tasks")
    execute_tasks([httpx_task], "Phase 2: HTTPx Task")
    execute_tasks(additional_tasks, "Phase 3: Additional Tasks")

def execute_tasks(tasks, phase_description):
    total_tasks = len(tasks)
    print(f'\n{phase_description} - Executing {total_tasks} tasks.')
    with ThreadPoolExecutor() as executor:
        futures_to_task = {executor.submit(task[1], *task[2]): task[0] for task in tasks}

        for i, future in enumerate(as_completed(futures_to_task), 1):
            task_name = futures_to_task[future]
            print(f'Task {i}/{total_tasks} "{task_name}" started.')
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