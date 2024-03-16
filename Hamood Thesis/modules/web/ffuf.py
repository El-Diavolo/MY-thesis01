import subprocess

def run_ffuf(subdomain):
    # Define the command to run ffuf
    command = [
        'ffuf', 
        '-w', '/path/to/wordlist', # Path to the wordlist
        '-u', f'http://{subdomain}/FUZZ' # The URL structure to fuzz
    ]

    # Execute the ffuf command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    # Handle errors
    if process.returncode != 0:
        print(f"Error running ffuf on {subdomain}: {stderr.decode('utf-8')}")
    else:
        print(stdout.decode('utf-8'))

    return stdout.decode('utf-8')
