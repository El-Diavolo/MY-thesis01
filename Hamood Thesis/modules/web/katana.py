import subprocess
import os

def run_katana(subdomains_dir="results/subdomains", output_dir="results/katana"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through each file in the subdomains directory
    for filename in os.listdir(subdomains_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(subdomains_dir, filename)
            domain = filename.replace("subdomains_", "").replace(".txt", "")
            domain_output_dir = os.path.join(output_dir, domain)

            # Ensure individual domain output directory exists
            os.makedirs(domain_output_dir, exist_ok=True)

            print(f"Running Katana on subdomains from {filepath}")
            command = ["katana", "-list", filepath, "-output", domain_output_dir]

            # Execute the command
            try:
                subprocess.run(command, check=True)
                print(f"Katana crawling completed for {domain}")
            except subprocess.CalledProcessError as e:
                print(f"Katana failed for {domain}: {str(e)}")

if __name__ == "__main__":
    run_katana()
