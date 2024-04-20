import subprocess
import os
import logging
import glob

def setup_logger():
    logger = logging.getLogger('SQLI_Detection')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logger

def filter_sqli_urls(input_file, output_file):
    logger = setup_logger()
    if not os.path.exists(input_file):
        logger.error(f"Input file {input_file} does not exist.")
        return False

    # Run the 'gf' command to filter SQLi URLs from the input file
    with open(output_file, 'w') as outfile:
        command = ["gf", "sqli", input_file]
        process = subprocess.run(command, stdout=outfile)

    # Check if the output file is successfully created and has content
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        logger.info(f"SQLi URLs filtered and written to {output_file}")
        return True
    else:
        logger.error(f"Failed to create or write to {output_file}")
        return False

def run_sqlmap(sqli_file, sqli_dir):
    logger = setup_logger()

    if not os.path.exists(sqli_file):
        logger.error(f"SQLi file {sqli_file} does not exist.")
        return

    # Run sqlmap with the specified parameters
    print("Running sqlmap")
    sqlmap_command = [
        "sqlmap",
        "-m", sqli_file,
        "--level", "5",
        "--risk", "3",
        "--batch",
        "--dbs",
        "--tamper", "between"
    ]

    try:
        subprocess.run(sqlmap_command, check=True)
        print("sqlmap scan completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"sqlmap failed: {str(e)}")

def sqli_scan(katana_dir, sqli_dir):
    logger = setup_logger()
    os.makedirs(sqli_dir, exist_ok=True)
    all_files = glob.glob(os.path.join(katana_dir, '*'))

    # Iterate over all files in the Katana directory
    for file_path in all_files:
        logger.info(f"Processing file: {file_path}")
        sqli_file = os.path.join(sqli_dir, 'sqli_urls.txt')
        if filter_sqli_urls(file_path, sqli_file):
            run_sqlmap(sqli_file, sqli_dir)
            break  # Stop after processing the found file
    else:
        logger.info("No appropriate files found for SQLi processing in the Katana directory.")

if __name__ == "__main__":
    target_domain = "testphp.vulnweb.com"
    katana_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/katana"
    sqli_dir = "/mnt/d/MY-thesis01/Hamood-Thesis/results/sqli"
    sqli_scan(katana_dir, sqli_dir)
