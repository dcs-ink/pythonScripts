import subprocess
import ipaddress
import platform
import socket

# This can be run anywhere in the code but is not best practice. It is better to define functions and call them.
# hostname = socket.gethostname()
# print(hostname)

# Creates a variable "hostname" and uses the socket module to get the local hostname.
def get_local_network():
    hostname = socket.gethostname()
    print(hostname)
    local_ip = socket.gethostbyname(hostname)
    print(local_ip)

get_local_network()

