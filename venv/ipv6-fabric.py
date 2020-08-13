from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir_scrapli.tasks import send_command, send_configs


def underlay(task):
    device = str(f"{task.host.hostname}")
    num = device[-2:]
    loopback_ip = f"2001:db8:acad:{num}::{num}/64"

    loopback_command = [
        'ipv6 unicast-routing',
        'int lo0',
        'ipv6 address ' + loopback_ip,
        'ipv6 ospf 1 area 0'
    ]

    deploy_loopback = task.run(send_configs, name="Configuring Loopback", configs=loopback_command)
    ospf_commands = [
        'ipv6 router ospf 1',
        f'router-id {num}.{num}.{num}.{num}'
    ]
    deploy_ospf = task.run(send_configs,name="Automating OSPF process and RIDs", configs = ospf_commands)
    interface_commands = [
        'interface range G0/0-1',
        'no sh',
        f'ipv6 address fe80::{num} link-local',
        'ipv6 ospf 1 area 0'
    ]
    deploy_interface = task.run(send_configs, name="Automating OSPF Interfaces", configs=interface_commands)

    bgp_rid_commands = [
        'no router bgp ' + str(task.host['asn']),
        f'bgp router-id {num}.{num}.{num}.{num}'
    ]
    deploy_rid = task.run(send_configs, name="Automating BGP", configs=bgp_rid_commands)
    for i in range(1, 8):
        bgp_commands = [
            'router bgp ' + str(task.host['asn']),
            'neighbor 2001:db8:acad:' + str(i) + "::" + str(i) + ' remote-as ' + str(task.host['asn']),
            'neighbor 2001:db8:acad:' + str(i) + "::" + str(i) + ' update-source loopback0',
            'neighbor 2001:db8:acad:' + str(i) + "::" + str(i) + ' password cisco',
            'neighbor 2001:db8:acad:' + str(i) + "::" + str(i) + ' timers 10 30',
            'address-family ipv6',
            'neighbor 2001:db8:acad:' + str(i) + "::" + str(i) + ' activate'
        ]
        deploy_bgp = task.run(send_configs, name="Automating IPv6 BGP Configurations", configs=bgp_commands)




def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=underlay)
    print_result(result)

if __name__ == '__main__':
        main()


