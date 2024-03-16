import subprocess
import json

def find_subdomains(domain, output_folder="/workspaces/MY-thesis01/Hamood Thesis/results/subdomains/"):
    results = set()
    # Sublist3r
    print("[*] Starting subdomain enumeration with Sublist3r...")
    sublist3r_output_file = f"{output_folder}subdomains_sublist3r_{domain.replace('.', '_')}.txt"
    command = ["sublist3r", "-d", domain, "-o", sublist3r_output_file]
    
    try:
        subprocess.run(command, check=True)
        print(f"[+] Sublist3r output saved to {sublist3r_output_file}")
        
        with open(sublist3r_output_file, 'r') as file:
            subdomains = [line.strip() for line in file if line.strip()]
            return subdomains
    except subprocess.CalledProcessError as e:
        print(f"Error running Sublist3r: {e}")
    except FileNotFoundError:
        print("Sublist3r output file not found.")

    return []

def main():
    find_subdomains()
    
    
    
