import subprocess
import json

def find_subdomains(domain):
    results = set()
    # Sublist3r
    print("[*] Starting subdomain enumeration with Sublist3r...")
    subprocess.call(["sublist3r", "-d", domain, "-o", "subdomains_sublist3r.txt"])
    # Read the output from the file
    try:
        with open("subdomains_sublist3r.txt", "r") as file:
            for line in file:
                results.add(line.strip())
    except FileNotFoundError:
        print("Sublist3r did not generate an output file.")
        return None
    
    return results
    
    
    
