import subprocess
import os

def find_subdomains(domain, output_folder="results/subdomains/"):
    os.makedirs(output_folder, exist_ok=True)

    print("[*] Starting subdomain enumeration with Sublist3r...")
    sublist3r_output_file = os.path.join(output_folder, f"subdomains_{domain.replace('.', '_')}.txt")
    command = ["sublist3r", "-d", domain, "-o", sublist3r_output_file]
    
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(sublist3r_output_file) and os.path.getsize(sublist3r_output_file) > 0:
            print(f"[+] Sublist3r output saved to {sublist3r_output_file}")
            with open(sublist3r_output_file, 'r') as file:
                subdomains = [line.strip() for line in file.readlines() if line.strip()]
        else:
            print(f"[!] No subdomains found for {domain}. Saving the domain itself as output.")
            with open(sublist3r_output_file, 'w') as file:
                file.write(domain + "\n")
            subdomains = [domain]
        
        return subdomains
    except subprocess.CalledProcessError as e:
        print(f"Error running Sublist3r: {e}")
        return []

