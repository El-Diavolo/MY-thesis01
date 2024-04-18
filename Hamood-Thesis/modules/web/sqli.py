import subprocess
import os
import logging
import glob

def setup_logger():
    logger = logging.getLogger('SQLI_Detection')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logger

def filter_sqli_urls(input_file, sqli_file):
    logger = setup_logger()
    if not os.path.exists(input_file):
        logger.error(f"Input file {input_file} does not exist.")
        return False

    with open(sqli_file, 'w') as output:
        command = ["gf", "sqli", input_file]
        subprocess.run(command, stdout=output)

    if os.path.exists(sqli_file) and os.path.getsize(sqli_file) > 0:
        logger.info(f"SQLi URLs filtered and written to {sqli_file}")
        return True
    else:
        logger.error(f"Failed to create or write to {sqli_file}")
        return False

def run_sqlmap(sqli_file):
    logger = setup_logger()
    command = [
        "sqlmap", 
        "-m", sqli_file, 
        "--level", "5", 
        "--risk", "3", 
        "--batch", 
        "--dbs", 
        "--tamper", "between"
    ]

    try:
        subprocess.run(command)
        logger.info("sqlmap scan completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run sqlmap: {e}")

def sqli_scan(katana_dir, sqli_dir):
    logger = setup_logger()
    os.makedirs(sqli_dir, exist_ok=True)
    results_json_path = os.path.join(sqli_dir, 'sqli_results.json')
    all_results = []

    for file_path in glob.glob(os.path.join(katana_dir, '*')):
        logger.info(f"Processing file: {file_path}")
        sqli_file_path = os.path.join(sqli_dir, 'urls.sqli')
        if filter_sqli_urls(file_path, sqli_file_path):
            run_sqlmap(sqli_file_path)

    logger.info("All files processed for SQL Injection testing.")

if __name__ == "__main__":
    katana_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/katana"
    sqli_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/sqli"
    sqli_scan(katana_dir, sqli_dir)
