import nmap
import subprocess
import os

def run_nmap_scan(target):
    """Runs a basic Nmap scan on the target."""
    nm = nmap.PortScanner()
    print(f"[*] Starting Nmap scan on: {target}")
    
    # -sV: Service version detection
    # -T4: Faster execution
    nm.scan(target, arguments='-sV -T4')
    
    scan_results = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                service = nm[host][proto][port]
                scan_results.append({
                    "port": port,
                    "name": service['name'],
                    "product": service.get('product', ''),
                    "version": service.get('version', ''),
                    "state": service['state']
                })
    return scan_results

def run_nikto_scan(target):
    """Runs a Nikto scan using the system command line."""
    print(f"[*] Starting Nikto scan on: {target}")
    
    # We use subprocess to run the actual 'nikto' command in Kali
    try:
        # -h: host
        # -Tuning 1,2,3: Specific scans (XSS, SQLi, etc.)
        cmd = ["nikto", "-h", target, "-Tuning", "123", "-Display", "1"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return result.stdout
    except Exception as e:
        return f"Nikto scan failed: {str(e)}"

if __name__ == "__main__":
    # Test block: This runs if you execute the file directly
    test_target = "127.0.0.1"
    nmap_data = run_nmap_scan(test_target)
    print(f"Nmap found {len(nmap_data)} ports.")
    # nikto_data = run_nikto_scan(test_target) # Uncomment to test Nikto (takes time)