import subprocess
import os
from datetime import datetime  # Added to handle date for the filename

def run_nmap_scan(ip_range):
    """Runs an nmap scan using subprocess and streams the output."""
    print(f"Running nmap scan on {ip_range}...\n")
    try:
        # Define the specific ports to scan
        ports = (
            "21,22,23,25,53,80,110,143,161,162,443,"
            "3306,3389,5900,6379,8080,8443,"
            "445,139,135,5985,5986,1433,1521,2375,2376,9200"
        )
        process = subprocess.Popen(
            ['sudo', 'nmap', '-sS', '-T4', '--min-rate', '1000', '--max-retries', '1', '-p', ports, ip_range],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = []  # Capture output here
        for line in process.stdout:
            print(line.strip())  # Print each line of output as it arrives
            output.append(line.strip())  # Append to output list
        process.wait()
        if process.returncode != 0:
            print(f"Error running nmap: {process.stderr.read().strip()}")
            return None
        return "\n".join(output)  # Return the captured output as a single string
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


def save_report_to_file(report):
    """Saves the scan report to a text file in the home directory."""
    date_str = datetime.now().strftime("%Y-%m-%d")  # Get current date
    filename = os.path.expanduser(f"~/nmap_report_{date_str}.txt")  # File path in home directory
    with open(filename, "w") as file:
        file.write("Network Scan Report:\n")
        file.write("=" * 50 + "\n")
        for host in report:
            file.write(f"IP Address: {host['IP']}\n")
            file.write(f"Hostname: {host['Hostname']}\n")
            file.write(f"State: {host['State']}\n")
            if host['Open Ports']:
                file.write("Open Ports:\n")
                for port in host['Open Ports']:
                    file.write(f"  - Port {port['Port']}: {port['State']} ({port['Service']})\n")
            else:
                file.write("No open ports found.\n")
            file.write("=" * 50 + "\n")
    print(f"Report saved to {filename}")


if __name__ == "__main__":
    target_range = input("Enter target IP range: ")

    # Check if the script is run with sudo
    if os.geteuid() != 0:
        print("This script must be run as root. Please use sudo.")
        exit(1)

    # Run the nmap scan
    raw_output = run_nmap_scan(target_range)
    if raw_output:
        print("\nScan completed successfully!")
        parsed_report = parse_nmap_output(raw_output)
        display_report(parsed_report)
        save_report_to_file(parsed_report)  # Save the report to a file