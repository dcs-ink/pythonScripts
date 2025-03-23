# # ========================================
# # Old Code
# # ========================================

# # import subprocess
# # import ipaddress
# # import platform
# # import socket

# # This can be run anywhere in the code but is not best practice. It is better to define functions and call them.
# # hostname = socket.gethostname()
# # print(hostname)

# # Creates a variable "hostname" and uses the socket module to get the local hostname.
# # def get_local_network():
# #     hostname = socket.gethostname()
# #    print(hostname)
# #     local_ip = socket.gethostbyname(hostname)
# #     print(local_ip)

# # get_local_network()

# # This grabs the IP address from the local machine, which is typically 127.0.0.1
# # I'm looking to get the local area network address.

# # def get_local_ip():
# #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# #     s.settimeout(0)


# # After researching the socket module, I discovered "SOCK_DGRAM" is used for UDP and is quicker than TCP. In this case it would be fine because the goal is to trick the interface into opening up the network. 

# # HOWEVER

# # I don't want to retrieve the IP from the local maachine, I want to know what the local gateway thinks the device's IP is.

# # THEREFORE

# # I will be ditching the socket module and use nmap instead. nmap doesn't need "platform" either so we'll be removing that. NMAP handles what the modules "ipaddress" and "platform" do as well.

# # pip isnstall pythonnmap
# import nmap
# # Back to using some of previous script
# import ipaddress
# import socket

# def get_local_network():
#     # get the hostname
#     hostname = socket.gethostname()
#     # get the IP
#     local_ip = socket.gethostbyname(hostname)
#     print(local_ip)

#     # Extract first two octets and assume a /16 network
#     ip_parts = local_ip.split('.')
#     network_str = f"{ip_parts[0]}.{ip_parts[1]}.0.0/16"

#     return ipaddress.IPv4Network(network_str, strict=False)

# network = get_local_network()
# print(f"Network: {network}")

# nm = nmap.PortScanner()

# nm.scan(str(network), arguments='-sn') #scan the network for live hosts.

# hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

# for host, status in hosts_list:
#     print(f"Host: {host} is {status}")

# # define the main variable "network" 
# def scan_network_nmap(network):
#     # create a variable "nm" for code readability and consistency
#     nm = nmap.PortScanner()
#     # invokes "scan" from nmap with "-sn" directing a ping scan or ICMP echo request.
#     nm.scan(host=network, arguments='-sn')
    
#     # define a variable for what will be found
#     live_devices = []
#     # use "all_hosts" from the PortScanner object to get all the hosts (IP addresses) in the network. The colon  is there to indicate a loop to find all the hosts.
#     for host in nm.all_hosts():
#         # check if hostnames are available for current IP address
#         if 'hostnames' in nm[host]:
#             # find hostname
#             hostname = nm[host].hostnames()
#         else:
#             hostname = None
#         live_devices.append((host, hostname))
    
#     return live_devices

# # I am going to end up using a bit of code from previously because I don't want to manually put the network information in. I want the script to automatically try and find it. I'll make a note above pointing it out.

# ..Later that evening
# Restarting to Reinforce Past Lessons and Focus on Practical Applications

import nmap

def scan_network(ip_range):
    scanner = nmap.PortScanner()
    print(f"Scanning network: {ip_range}...")

    scanner.scan(hosts=ip_range, arguments='-Pn')

    for host in scanner.all_hosts():
        print(f"Host: {host} is {scanner[host].state}")

if __name__ == "__main__":
    target_range = input("Enter target IP range: ")
    scan_network(target_range)