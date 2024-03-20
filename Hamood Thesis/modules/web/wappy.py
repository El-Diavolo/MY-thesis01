# wappy.py
import subprocess
import os
import json

def extract_and_run(urls_file, output_dir='results/techstack'):
    """
    Runs tech stack detection on URLs extracted from a JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(urls_file, 'r') as file:
        data = json.load(file)

    for url, details in data.get('online', {}).items():
        if details.get('status_code') in [200, 302]:
            output_file = os.path.join(output_dir, f"{url.replace('https://', '').replace('http://', '').replace('/', '_')}.json")
            command = ['wappy', '-f', url]

            try:
                result = subprocess.run(command, check=True, capture_output=True, text=True)
                # Assuming the CLI tool 'wappy' outputs JSON directly to stdout
                with open(output_file, 'w') as f:
                    f.write(result.stdout)
                print(f"Tech stack detection completed for {url}. Results saved to {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error detecting tech stack for {url}: {e}")

def run_tech_stack_detection(hosts_dir='results/hosts', output_dir='results/techstack'):
    """
    Detects tech stacks for URLs based on online status and specific status codes from JSON files.
    """
    for filename in os.listdir(hosts_dir):
        if filename.endswith('.json'):
            extract_and_run(os.path.join(hosts_dir, filename), output_dir)
