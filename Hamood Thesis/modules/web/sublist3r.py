import subprocess
import json

def find_subdomains(domain):
    # Call the sublist3r command
    process = subprocess.Popen(['sublist3r', '-d', domain, '-o', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    # Handle errors
    if process.returncode != 0:
        print(f"Error finding subdomains: {stderr}")
        return []
    
    # Parse the output from JSON if Sublist3r is set up to output JSON
    subdomains = json.loads(stdout.decode('utf-8'))
    
    return subdomains
