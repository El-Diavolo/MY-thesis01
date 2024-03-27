import httpx
import asyncio
import os
import json

async def check_subdomain(client, subdomain, results):
    try:
        response = await client.get(f"https://{subdomain}")
        print(f"{subdomain} - {response.status_code}")
        results['online'][subdomain] = {'status_code': response.status_code}
    except httpx.RequestError as e:
        print(f"Error checking {subdomain}: {e}")
        results['offline'][subdomain] = {'error': str(e)}

async def run_checks(subdomains):
    results = {'online': {}, 'offline': {}}
    timeout = httpx.Timeout(50.0, connect=50.0, read=50.0, write=50.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        tasks = [check_subdomain(client, subdomain, results) for subdomain in subdomains]
        await asyncio.gather(*tasks)
    
    return results

def get_subdomains_from_directory(subdomains_dir='results/subdomains'):
    subdomains = []
    for filename in os.listdir(subdomains_dir):
        filepath = os.path.join(subdomains_dir, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                subdomains.extend(file.read().splitlines())
    return list(set(subdomains))

def run_httpx(target_domain, results_base_dir='/home/eldiablo/Hamood-thesis/Hamood Thesis/results'):
    subdomains = get_subdomains_from_directory(os.path.join(results_base_dir, 'subdomains'))
    results = asyncio.run(run_checks(subdomains))
    
    results_dir = os.path.join(results_base_dir, 'hosts')  # Ensuring the correct output directory is used
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Using target_domain in the file name for specificity
    results_file_name = f"{target_domain}_httpx_results.json"
    results_file_path = os.path.join(results_dir, results_file_name)
    with open(results_file_path, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    print(f"Results saved to {results_file_path}")
