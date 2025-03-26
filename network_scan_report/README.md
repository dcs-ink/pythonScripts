### The files network_scanner.py and port_scanner.py are not used. They were used as testing scripts as I explored nmap. 


# Network Scan Report Script

This Python script uses `nmap` to scan a network for active hosts, hostnames, and open ports. It provides a detailed report of the scan results and saves the report to a text file in the user's home directory.

---

## Features

- Scans a specified IP range for active hosts.
- Detects hostnames and open ports for common services.
- Displays the scan results in a readable format.
- Saves the scan report to a file in the user's home directory.

---

## Requirements

1. **Python 3.x**: Ensure Python 3 is installed on your system.
2. **Nmap**: The script requires `nmap` to be installed system-wide. Install it using:
   ```bash
   sudo apt install nmap
   ```
3. **Root Privileges**: The script must be run with `sudo` to perform certain types of scans.

---

## Installation

1. Clone or download this repository to your local machine.
2. Navigate to the directory containing the script:
   ```bash
   cd /path/to/script
   ```

---

## Usage

1. Run the script with `sudo`:
   ```bash
   sudo python3 network_scan_report.py
   ```

2. Enter the target IP range when prompted (e.g., `192.168.1.0/24`).

3. The script will:
   - Perform a network scan.
   - Display the results in the terminal.
   - Save the report to a file in your home directory (e.g., `~/nmap_report_YYYY-MM-DD.txt`).

---

## Example Output

### Terminal Output
```plaintext
Enter target IP range: 192.168.1.0/24
Running nmap scan on 192.168.1.0/24...

Scan completed successfully!

Network Scan Report:
==================================================
IP Address: 192.168.1.1
Hostname: router.local
State: up
Open Ports:
  - Port 80: open (http)
  - Port 443: open (https)
==================================================
IP Address: 192.168.1.100
Hostname: desktop.local
State: up
Open Ports:
  - Port 22: open (ssh)
==================================================
Report saved to ~/nmap_report_2025-03-22.txt
```

### Saved Report (`~/nmap_report_YYYY-MM-DD.txt`)
```plaintext
Network Scan Report:
==================================================
IP Address: 192.168.1.1
Hostname: router.local
State: up
Open Ports:
  - Port 80: open (http)
  - Port 443: open (https)
==================================================
IP Address: 192.168.1.100
Hostname: desktop.local
State: up
Open Ports:
  - Port 22: open (ssh)
==================================================
```

---

## Customization

### Ports
The script scans a predefined list of common ports. You can modify the `ports` variable in the `run_nmap_scan` function to include additional ports or change the range.

### Output File
The report is saved to the user's home directory with the filename format `nmap_report_YYYY-MM-DD.txt`. You can modify the `save_report_to_file` function to change the location or filename format.

---

