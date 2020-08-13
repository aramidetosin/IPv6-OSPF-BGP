from ipaddress import IPv4Address

list_ip = ['192.168.1.201','192.168.1.202', '192.168.1.203', '192.168.1.214', '192.168.1.205', '192.168.1.206', '192.168.1.207', '192.168.1.208']


with open("hosts.yaml", "w") as file:
    file.write("---\n")
    for num , ip in enumerate(list_ip):
        file.write(f'R{num+1}:\n')
        file.write(f'    hostname: {ip}\n')
        file.write(f'    platform: ios\n')
        file.write(f'    groups:\n')
        file.write(f'      - cisco_group\n')