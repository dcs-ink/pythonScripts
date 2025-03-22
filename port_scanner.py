import socket
import threading

def scan_port(ip, port):
    """Attempts to connect to a specific port on the given IP"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # 1-second timeout
    result = sock.connect_ex((ip, port))
    if result == 0:
        print(f"Port {port} is OPEN")
    sock.close()

def scan_ports(ip, start_port, end_port):
    """Scans ports in the given range using threading"""
    print(f"Scanning {ip} from port {start_port} to {end_port}...")
    threads = []

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    target_ip = input("Enter target IP: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    scan_ports(target_ip, start_port, end_port)
