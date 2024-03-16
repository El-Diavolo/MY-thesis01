import subprocess
import os


def run_ffuf(subdomain,wordlist ,results_dir):
    os.makedirs(results_dir, exist_ok=True)
    result_file = f'{results_dir}/{subdomain.replace(":", "_").replace("/", "_")}_ffuf.json'
    
    command = [
        'ffuf',
        '-w', wordlist,
        '-u', f'https://{subdomain}/FUZZ',
        '-fc', '401,403,500',
        '-o', result_file,
        '-of', 'json'
    ]

    # Execute the ffuf command
    process = subprocess.run(command, capture_output=True, text=True)
    
    # Handle errors
    if process.returncode != 0:
        print(f"Error running ffuf on {subdomain}: {process.stderr}")
    else:
        print(f"Successfully executed ffuf on {subdomain}. Output saved to {result_file}")

    return process.stdout

def read_subdomains_and_run_ffuf(directory_path, wordlist_path , results_dir):
    for filename in os.listdir(directory_path):
        full_path = os.path.join(directory_path, filename)
        if os.path.isfile(full_path) and full_path.endswith('.txt'):
            with open(full_path, 'r') as file:
                subdomains = file.read().splitlines()
                for subdomain in subdomains:
                    print(f"Running ffuf on {subdomain}")
                    run_ffuf(subdomain, wordlist_path , results_dir)
    return ()

def main():
    run_ffuf()
    read_subdomains_and_run_ffuf()

    