import subprocess
import json

subdomainfolder = "/workspaces/MY-thesis01/Hamood Thesis/results/subdomains/"
def find_subdomains(domain):
    results = set()
    # Sublist3r
    print("[*] Starting subdomain enumeration with Sublist3r...")
    sublist3r_output_file = f"{subdomainfolder}subdomains_sublist3r.txt"
    subprocess.call(["sublist3r", "-d", domain, "-o", sublist3r_output_file])
    # Read the output from the file
    try:
        with open(sublist3r_output_file, "r") as file:
            for line in file:
                results.add(line.strip())
    except FileNotFoundError:
        print("Sublist3r did not generate an output file.")
        return None
    
    return results
    
    
    
