import subprocess
import os

def run_nmap_scan(ip_range):
    """Runs an nmap scan using subprocess and streams the output."""
    print(f"Running nmap scan on {ip_range}...\n")
    try:
        process = subprocess.Popen(
            ['sudo', 'nmap', '-sS', '-T4', '--min-rate', '1000', '--max-retries', '1', '-p', '1-100', ip_range],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in process.stdout:
            print(line.strip())  # Print each line of output as it arrives
        process.wait()
        if process.returncode != 0:
            print(f"Error running nmap: {process.stderr.read().strip()}")
            return None
        return process.stdout.read()
    except FileNotFoundError:
        print("Error: nmap is not installed or not found in PATH.")
        return None
    except subprocess.TimeoutExpired:
        print("Error: The scan took too long and was terminated.")
        return None


def parse_nmap_output(output):
    """Parses the raw nmap output and extracts IPs, hostnames, and open ports."""
    report = []
    current_host = None

    for line in output.splitlines():
        line = line.strip()

        # Detect a new host
        if line.startswith("Nmap scan report for"):
            if current_host:
                report.append(current_host)
            current_host = {
                "IP": None,
                "Hostname": None,
                "State": "up",
                "Open Ports": []
            }
            parts = line.split("for")
            if len(parts) > 1:
                host_info = parts[1].strip()
                if "(" in host_info and ")" in host_info:
                    hostname, ip = host_info.split("(", 1)
                    current_host["Hostname"] = hostname.strip()
                    current_host["IP"] = ip.strip(")")
                else:
                    current_host["IP"] = host_info

        # Detect open ports
        elif line.startswith("PORT"):
            continue  # Skip the header line
        elif line and current_host and "/" in line:
            parts = line.split()
            port = parts[0].split("/")[0]
            state = parts[1]
            service = parts[2] if len(parts) > 2 else "unknown"
            current_host["Open Ports"].append({
                "Port": port,
                "State": state,
                "Service": service
            })

    # Add the last host to the report
    if current_host:
        report.append(current_host)

    return report


def display_report(report):
    """Displays the scan report in a readable format."""
    print("\nNetwork Scan Report:")
    print("=" * 50)
    for host in report:
        print(f"IP Address: {host['IP']}")
        print(f"Hostname: {host['Hostname']}")
        print(f"State: {host['State']}")
        if host['Open Ports']:
            print("Open Ports:")
            for port in host['Open Ports']:
                print(f"  - Port {port['Port']}: {port['State']} ({port['Service']})")
        else:
            print("No open ports found.")
        print("=" * 50)


if __name__ == "__main__":
    target_range = input("Enter target IP range (e.g., 192.168.1.0/24): ")

    # Check if the script is run with sudo
    if os.geteuid() != 0:
        print("This script must be run as root. Please use sudo.")
        exit(1)

    # Run the nmap scan
    raw_output = run_nmap_scan(target_range)
    if raw_output:
        print("\nScan completed successfully!")