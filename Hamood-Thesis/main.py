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
    run_gospider,
    run_crawler,
    run_xss,
    lfi_scan,
    sqli_scan
)
from modules.network import scan_common_ports

# Paths configuration
wordlist_path = 'test/testwordlist.txt'
hosts_path = "results/hosts"
results_dir = "results/directories"
subdomains_dir = 'results/subdomains'
katana_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/katana"
lfi_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/lfi"
payloads_lfi = "/opt/smalllfi.txt"
xss_dir = "results/xss"
sqli_dir = "results/sqli"

# API keys
from dotenv import load_dotenv
load_dotenv()
SHODAN_API_TOKEN = os.getenv("SHODAN_API_TOKEN")

def main(target_domain):
    print(f'Starting scans for: {target_domain}')

    # Phase 1: Concurrent execution of initial tasks
    Phase_1 = [
        ('Scan Common Ports', scan_common_ports, (target_domain,)),
        ('Find Subdomains', find_subdomains, (target_domain,)),
        ('Shodan Search', shodan_search, (SHODAN_API_TOKEN, target_domain)),
        #('gospider' , run_gospider, (target_domain,)),
        
        
    ]

    
    Phase_2 = [
                ('Run HTTPx', run_httpx, (subdomains_dir,)),
                ('katana' , run_crawler, (target_domain,))
                
    ]

    # Phase 3: Concurrent execution of additional tasks
    Phase_3 = [
        ('Read Subdomains and Run FFUF', read_subdomains_and_run_ffuf, (target_domain, hosts_path, wordlist_path, 'results/directories')),
        ('Run Tech Stack Detection', run_tech_stack_detection, (hosts_path, 'results/techstack')),
        #('Running Screenshotter', run_eyewitness, ('results/subdomains', 'results/screenshots')),
        #('Run Nuclei Scan', run_nuclei_scan, (hosts_path, 'results/nuclei')),
        
    ]


    Phase_4 = [
        ('Run LFI Scsan' , lfi_scan, (katana_dir, lfi_dir , payloads_lfi,)),
    ]
    
    Phase_5 = [
        ('Run Xss Scsan' , run_xss, ()),
    ]

    Phase_6 = [
        ('Run SQLI Scan' , sqli_scan, (target_domain,)),
    ]

    # Execute tasks
    execute_tasks(Phase_1, "Phase 1: Initial Tasks")
    execute_tasks(Phase_2, "Phase 2: HTTPx Task")
    execute_tasks(Phase_3, "Phase 3: crawling")
    execute_tasks(Phase_4, "Phase 4: LFI tests")
    execute_tasks(Phase_5, "Phase 5: Xss tests")
    execute_tasks(Phase_6, "Phase 6: SQLI tests")


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