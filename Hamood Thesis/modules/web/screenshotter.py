import subprocess
import os

def run_eyewitness(subdomains_dir = 'results/subdomains', output_dir='results/screenshots'):
    
    """
    Takes screenshots of domains listed in files within the subdomains_dir using EyeWitness,
    attempting to use subprocess and echo to handle prompts.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over each file in the subdomains directory
    for filename in os.listdir(subdomains_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(subdomains_dir, filename)
            print(f"Taking screenshots for: {filepath}")

            # Construct the EyeWitness command
            command = f"eyewitness --web -f {filepath} --timeout 100 -d {output_dir} --no-prompt"
            

            
            try:
                result = subprocess.run(command, shell=True, check=True)
                print(f"Screenshots completed for {filepath}")
                if result.stderr:
                    print(f"Error or warning messages: {result.stderr}")
            except subprocess.CalledProcessError as e:
                print(f"Error running EyeWitness on {filepath}: {e}")


