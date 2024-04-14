import subprocess
import os

def run_katana_on_domain(target_domain, output_dir="results/katana"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create a specific directory for the target domain to store results
    domain_output_dir = os.path.join(output_dir, f"katana_{target_domain.replace('.', '_').replace('/', '_')}.txt")
    os.makedirs(domain_output_dir, exist_ok=True)

    # Define URLs with HTTP and HTTPS protocols
    urls = [f"http://{target_domain}", f"https://{target_domain}"]

    for url in urls:
        print(f"Running Katana on {url}")
        command = ["katana", "-u", url, "-output", domain_output_dir]

        # Execute the command
        try:
            subprocess.run(command, check=True)
            print(f"Katana crawling completed for {url}")
        except subprocess.CalledProcessError as e:
            print(f"Katana failed for {url}: {str(e)}")

if __name__ == "__main__":
    target_domain = input("Enter the target domain (e.g., example.com): ")
    run_katana_on_domain(target_domain)
