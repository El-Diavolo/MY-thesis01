# lfi_detection.py
import subprocess
import os
import json
import glob
import logging

def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger()

def filter_lfi_urls(input_file, lfi_file):
    with open(lfi_file, 'w') as output:
        command = ["gf", "lfi", input_file]
        subprocess.run(command, stdout=output)

def replace_fuzz(lfi_file):
    with open(lfi_file, 'r') as file:
        urls = [line.strip().replace('FUZZ', 'FUZZ') for line in file.readlines()]
    with open(lfi_file, 'w') as file:
        file.writelines(url + '\n' for url in urls)

def run_ffuf(lfi_file, results_file):
    results = []
    with open(lfi_file, 'r') as file:
        urls = file.read().splitlines()
    for url in urls:
        command = ["ffuf", "-u", url, "-mr", '"root:x"', "-w", "/opt/smalllfi.txt", "-r"]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            results.append(url)

    with open(results_file, 'w') as file:
        json.dump(results, file, indent=4)

def lfi_scan(katana_dir, lfi_dir, payloads_file):
    os.makedirs(lfi_dir, exist_ok=True)
    logger = setup_logger()
    for file_path in glob.glob(os.path.join(katana_dir, '*')):
        logger.info(f"Processing file: {file_path}")
        lfi_file_path = os.path.join(lfi_dir, 'urls.lfi')
        results_json_path = os.path.join(lfi_dir, 'lfi_results.json')
        filter_lfi_urls(file_path, lfi_file_path)
        replace_fuzz(lfi_file_path)
        run_ffuf(lfi_file_path, results_json_path)


if __name__ == "__main__":
    logger = setup_logger()
    katana_dir = "results/katana"  # Directory where Katana outputs are stored
    lfi_dir = "results/lfi"
    payloads_file = "/opt/smalllfi.txt"  # Ensure this file exists with suitable payloads
    
    lfi_scan(katana_dir, lfi_dir, payloads_file)