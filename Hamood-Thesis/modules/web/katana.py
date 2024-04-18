import subprocess
import os

def run_katana(target_domain, output_dir="results/katana"):
    # Ensure the base output directory exists
    os.makedirs(output_dir, exist_ok=True)


    # Define URLs with HTTP and HTTPS protocols
    urls = [f"http://{target_domain}"]

    for url in urls:
        # Define the output file path for the results
        protocol_type = "http" if url.startswith("http:") else "https"
        output_file_path = os.path.join(output_dir, f"{protocol_type}_results.txt")
        
        print(f"Running Katana on {url}")
        command = ["katana", "-u", url,"-output", output_file_path]

        # Execute the command
        try:
            subprocess.run(command, check=True)
            print(f"Katana crawling completed for {url}, results saved to {output_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Katana failed for {url}: {str(e)}")

if __name__ == "__main__":
    target_domain = input("Enter the target domain (e.g., example.com): ")
    run_katana(target_domain)
