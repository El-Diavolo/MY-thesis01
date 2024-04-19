import subprocess
import os

def run_katana(target_domain, output_dir="results/katana"):
    os.makedirs(output_dir, exist_ok=True)
    url = f"http://{target_domain}"
    output_file_path = os.path.join(output_dir, f"katana_results.txt")
    
    print(f"Running Katana on {url}")
    command = ["katana", "-u", url, "-output", output_file_path]

    try:
        subprocess.run(command, check=True)
        print(f"Katana crawling completed for {url}, results saved to {output_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Katana failed for {url}: {str(e)}")

def run_gau(target_domain, output_dir="results/katana"):
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, "gau_results.txt")

    print(f"Running gau on {target_domain}")
    command = ["gau", target_domain, "--o", output_file_path]

    try:
        subprocess.run(command, check=True)
        print(f"gau crawling completed for {target_domain}, results saved to {output_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"gau failed for {target_domain}: {str(e)}")

def deduplicate_urls(katana_file, gau_file, output_file):
    command = ["uro", "-i", katana_file, "-i", gau_file, "-o", output_file]

    try:
        subprocess.run(command, check=True)
        print(f"URLs deduplicated and saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to deduplicate URLs: {str(e)}")

if __name__ == "__main__":
    target_domain = input("Enter the target domain (e.g., example.com): ")
    katana_output = "results/katana/katana_results.txt"
    gau_output = "results/katana/gau_results.txt"
    final_output = "results/katana/final_deduplicated_urls.txt"

    run_katana(target_domain)
    run_gau(target_domain)
    deduplicate_urls(katana_output, gau_output, final_output)
