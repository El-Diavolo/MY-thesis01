""" Run nmap scans against a targeted system
- Full TCP SYN/ACK (-sT)
- UDP Scan (-sU)
- ICS/OT Specific (-sT -sV)
etc.
"""

def web_scans(url):
    pass

def run_scan(user_input: str, url: str) -> str:
    if user_input == 'web':
        web_scans(url)
    pass
