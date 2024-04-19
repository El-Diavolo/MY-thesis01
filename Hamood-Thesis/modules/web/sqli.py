import subprocess
import os
import logging
import glob
import urllib.parse

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
    
    logger.info(f"SQLi URLs filtered and written to {sqli_file}")
    return True

def deduplicate_urls(sqli_file):
    logger = setup_logger()
    unique_urls = set()

    with open(sqli_file, 'r') as file:
        urls = file.readlines()
        for url in urls:
            parsed_url = urllib.parse.urlparse(url.strip())
            query_params = urllib.parse.parse_qs(parsed_url.query)
            # Create a standardized query string with parameter names only, append '=' to simulate an input point
            sanitized_query = '&'.join([f"{key}=" for key in sorted(query_params.keys())])
            sanitized_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            if sanitized_query:
                sanitized_url += f"?{sanitized_query}"
            unique_urls.add(sanitized_url)

    with open(sqli_file, 'w') as file:
        for url in sorted(unique_urls):
            file.write(url + '\n')

    logger.info(f"Deduplicated URLs written back to {sqli_file}")

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
    subprocess.run(command)
    logger.info("sqlmap scan completed successfully.")

def sqli_scan(katana_dir, sqli_dir):
    logger = setup_logger()
    os.makedirs(sqli_dir, exist_ok=True)
    sqli_file_path = os.path.join(sqli_dir, 'urls.sqli')

    for file_path in glob.glob(os.path.join(katana_dir, '*')):
        logger.info(f"Processing file: {file_path}")
        if filter_sqli_urls(file_path, sqli_file_path):
            deduplicate_urls(sqli_file_path)  # Deduplicate URLs after gf filtering
            run_sqlmap(sqli_file_path)

    logger.info("All files processed for SQL Injection testing.")

if __name__ == "__main__":
    katana_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/katana"
    sqli_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/sqli"
    sqli_scan(katana_dir, sqli_dir)
