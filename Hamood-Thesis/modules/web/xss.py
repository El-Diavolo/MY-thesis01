import subprocess
import os
import json

def run_katana(target_domain, output_dir):
    # Ensure the directory for Katana output exists
    os.makedirs(output_dir, exist_ok=True)
    katana_output_path = os.path.join(output_dir, target_domain.replace(".", "_").replace("/", "_"))

    # Run Katana with the target domain
    command = ["katana", "-u", f"http://{target_domain}", "-output", katana_output_path]
    try:
        subprocess.run(command, check=True)
        print(f"Katana successfully crawled {target_domain}")
        return katana_output_path
    except subprocess.CalledProcessError as e:
        print(f"Failed to run Katana on {target_domain}: {e}")
        return None



def run_xssvibe(katana_output, xss_output):
    # Navigate to the directory where xssvibes is located
    xssvibes_dir = "/opt/xss_vibes"  # Adjust this path to the actual installation directory of xssvibes
    os.chdir(xssvibes_dir)  # Change current directory to xssvibes directory

    command = ["python3", "main.py", "-f", katana_output, "-o", xss_output, "-t", "10"]

    # Execute the command and capture the output
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        output_lines = result.stdout.strip().split('\n')
        
        parsed_results = []
        for line in output_lines:
            if line:
                try:
                    # Attempt to parse each line as JSON
                    parsed_results.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {line} - {e}")
        
        # Only write to the file if there are valid results
        if parsed_results:
            with open(xss_output, 'w') as json_file:
                json.dump(parsed_results, json_file, indent=4)
            print(f"XSS vulnerabilities scanned and saved to {xss_output}")
        else:
            print(f"No valid JSON results to write to {xss_output}")
            
    except subprocess.CalledProcessError as e:
        print(f"Failed to run xssvibe: {e}")


def run_dalfox(katana_output, dalfox_output):
    command = ["dalfox", "file", katana_output, "-o", dalfox_output, "--custom-alert-value", "calfcrusher", "--waf-evasion", "-F"]
    try:
        subprocess.run(command, check=True)
        print(f"Dalfox successfully scanned and saved to {dalfox_output}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run Dalfox: {e}")

def extract_xssvibes_output(file_path):
    with open(file_path, 'r') as file:
        return [{"url": line.strip()} for line in file if line.strip()]

def extract_dalfox_output(file_path):
    results = []
    with open(file_path, 'r') as file:
        for line in file:
            if "[POC]" in line:
                parts = line.split(" ")
                for part in parts:
                    if part.startswith("http"):
                        results.append({"url": part})
                        break
    return results

def remove_duplicates(xssvibes_results, dalfox_results):
    all_results = xssvibes_results + dalfox_results
    unique_results = {each['url']: each for each in all_results}.values()
    return list(unique_results)

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def run_xss(target_domain):
    katana_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/katana"
    xss_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/xss"
    os.makedirs(xss_dir, exist_ok=True)

    katana_output = run_katana(target_domain, katana_dir)
    if katana_output:
        xssvibe_output_path = os.path.join(xss_dir, f"xssvibe_results_{target_domain}.txt")
        dalfox_output_path = os.path.join(xss_dir, f"dalfox_PoC_{target_domain}.txt")
        final_json_output = os.path.join(xss_dir, f"final_xss_results_{target_domain}.json")
        
        run_xssvibe(katana_output, xssvibe_output_path)
        run_dalfox(katana_output, dalfox_output_path)
        
        # Extract and combine results from output files
        xssvibes_results = extract_xssvibes_output(xssvibe_output_path)
        dalfox_results = extract_dalfox_output(dalfox_output_path)
        unique_results = remove_duplicates(xssvibes_results, dalfox_results)
        
        # Save combined results to JSON
        save_to_json(unique_results, final_json_output)
        print(f"Combined results saved to {final_json_output}")

if __name__ == "__main__":
    target_domain = "testphp.vulnweb.com"
    run_xss(target_domain)