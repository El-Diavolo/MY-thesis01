import shodan
import sys

def shodan_search(api_key, query):
    # Initialize the Shodan client with your API key
    api = shodan.Shodan(api_key)
    
    try:
        # Perform the search on Shodan
        results = api.search(query)
        print(f"Results found: {results['total']}")
        
        # Loop through the matches and print some data
        for result in results['matches']:
            print("IP: {}".format(result['ip_str']))
            print("Organization: {}".format(result.get('org', 'n/a')))
            print("Operating System: {}".format(result.get('os', 'n/a')))
            # Add more fields as necessary
            
            # Print available ports
            ports = ", ".join(str(port) for port in result['ports']) if 'ports' in result else 'n/a'
            print(f"Ports: {ports}")
            
            print("")  # Newline for readability between records
    except shodan.APIError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        api_key = sys.argv[1]
        query = sys.argv[2]
        shodan_search(api_key, query)
    else:
        print("Usage: %s <API key> <search query>" % sys.argv[0])
        sys.exit(1)
