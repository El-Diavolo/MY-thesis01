import subprocess
import os
import json
import re

def parse_wappy_output_to_json(text_output):
    """
    Parses wappy's plain text output into a JSON-compatible dictionary.
    """
    tech_stack = {}
    for line in text_output.splitlines():
        # Assuming wappy's output format is like: "Technology : Detail [version: x.x.x]"
        match = re.search(r'(\w+)\s*:\s*(.*?)\s*\[version:\s*(.*?)\]', line)
        if match:
            tech, detail, version = match.groups()
            if tech not in tech_stack:
                tech_stack[tech] = []
            tech_stack[tech].append({'detail': detail, 'version': version or 'nil'})
    return tech_stack

def run_tech_stack_detection(hosts_dir='results/hosts', output_dir='results/techstack'):
    """
    Detects tech stacks for hosts based on online status and specific status codes from JSON files.
    Outputs the results into JSON files in the specified output directory.
    """
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(hosts_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(hosts_dir, filename)
            with open(filepath, 'r') as file:
                hosts_data = json.load(file)
                online_hosts = hosts_data.get('online', {})

                for host, details in online_hosts.items():
                    if details.get('status_code') in [200, 301]:
                        output_file = os.path.join(output_dir, f"{host.replace('https://', '').replace('http://', '').replace('/', '_')}_tech_stack.json")
                        command = ['wappy', '-u', host , '-wf' , output_file]  # Adjust command as needed
                        try:
                            result = subprocess.run(command, check=True, capture_output=True, text=True)
                            tech_stack_data = parse_wappy_output_to_json(result.stdout)
                            
                            output_file = os.path.join(output_dir, f"{host.replace('https://', '').replace('http://', '').replace('/', '_')}_tech_stack.json")
                            with open(output_file, 'w') as f:
                                json.dump(tech_stack_data, f, indent=4)
                            print(f"Tech stack detection completed for {host}. Results saved to {output_file}")
                        except subprocess.CalledProcessError as e:
                            print(f"Error detecting tech stack for {host}: {e}")

    compile_and_clean_tech_stacks(output_dir)

def compile_and_clean_tech_stacks(output_dir):
    """
    Compiles all tech stack detection results into a single JSON file and deletes the individual files.
    """
    compiled_results = {}
    
    for filename in os.listdir(output_dir):
        if filename.endswith('_tech_stack.json'):
            filepath = os.path.join(output_dir, filename)
            try:
                with open(filepath, 'r') as file:
                    try:
                        tech_stack_data = json.load(file)
                    except json.JSONDecodeError:
                        print(f"Skipping empty or invalid JSON file: {filename}")
                        continue  # Skip this file and move to the next one
                    host = filename.replace('_tech_stack.json', '').replace('_', '/')
                    compiled_results[host] = tech_stack_data
            finally:
                os.remove(filepath)  # Delete the file after processing or if an error occurred

    # Save the compiled results to a new JSON file
    compiled_filepath = os.path.join(output_dir, 'compiled_tech_stacks.json')
    with open(compiled_filepath, 'w') as file:
        json.dump(compiled_results, file, indent=4)
    print(f"Compiled tech stack detection results saved to {compiled_filepath}")



