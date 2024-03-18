import subprocess
import os

def find_subdomains(domain, output_folder="/workspaces/MY-thesis01/Hamood Thesis/results/subdomains/"):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    print("[*] Starting subdomain enumeration with Sublist3r...")
    sublist3r_output_file = os.path.join(output_folder, f"subdomains_sublist3r_{domain.replace('.', '_')}.txt")
    command = ["sublist3r", "-d", domain, "-o", sublist3r_output_file]
    
    try:
        # Execute Sublist3r silently
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[+] Sublist3r output saved to {sublist3r_output_file}")
        
        # Read and return the subdomains from the output file
        with open(sublist3r_output_file, 'r') as file:
            subdomains = [line.strip() for line in file.readlines() if line.strip()]
            return subdomains
    except subprocess.CalledProcessError as e:
        print(f"Error running Sublist3r: {e}")
        return []
    except FileNotFoundError:
        print("Sublist3r output file not found.")
        return []

