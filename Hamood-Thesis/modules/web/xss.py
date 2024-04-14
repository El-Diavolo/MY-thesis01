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
        # Parse the output lines as needed, this is an example assuming each line is a valid JSON
        parsed_results = [json.loads(line) for line in output_lines if line]
        # Save the parsed results as JSON
        with open(xss_output, 'w') as json_file:
            json.dump(parsed_results, json_file, indent=4)
        print(f"XSS vulnerabilities scanned and saved to {xss_output}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run xssvibe: {e}")

def run_xss(target_domain):
    katana_dir = "/mnt/d/MY-thesis01/Hamood\ Thesis/results/katana"
    xss_dir = "/mnt/d/MY-thesis01/Hamood\ Thesis/results/xss"
    os.makedirs(xss_dir, exist_ok=True)

    # Run Katana and get the output path
    katana_output = run_katana(target_domain, katana_dir)
    if katana_output:
        # Define output path for XSSvibe results
        xss_output_path = os.path.join(xss_dir, f"xss_results_{target_domain}.json")
        # Run XSSvibe with the Katana output
        run_xssvibe(katana_output, xss_output_path)

if __name__ == "__main__":
    target_domain = "testphp.vulnweb.com"
    run_xss(target_domain)
