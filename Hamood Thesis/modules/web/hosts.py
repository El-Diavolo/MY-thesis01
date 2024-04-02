import httpx
import json
import os

def check_subdomain(subdomain, results):
    try:
        response = httpx.get(f"https://{subdomain}", timeout=20.0)
        print(f"{subdomain} - {response.status_code}")
        results['online'][subdomain] = {'status_code': response.status_code}
    except Exception as e:
        print(f"Error checking {subdomain}: {e}")
        results['offline'][subdomain] = {'error': str(e)}

def run_checks(subdomains):
    results = {'online': {}, 'offline': {}}
    for subdomain in subdomains:
        check_subdomain(subdomain, results)
    return results

def get_subdomains_from_file(subdomains_file):
    with open(subdomains_file, 'r') as file:
        subdomains = file.read().splitlines()
    return subdomains

def run_httpx(subdomains_file, results_dir='results/hosts'):
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    subdomains = get_subdomains_from_file(subdomains_file)
    results = run_checks(subdomains)

    domain = os.path.basename(subdomains_file).split('_')[2].replace(".txt", "")
    results_file_path = os.path.join(results_dir, f"{domain}_httpx_results.json")
    
    with open(results_file_path, 'w') as json_file:
        json.dump(results, json_file, indent=4)
    
    print(f"HTTPx results saved to {results_file_path}")

if __name__ == "__main__":
    target_domain = "backblaze.com"
    subdomains_file = f'results/subdomains/subdomains_{target_domain.replace(".", "_")}.txt'
    run_httpx(subdomains_file)
