import os
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from rich import print

nr = InitNornir()
CLEAR = "clear"
os.system(CLEAR)

good_list = []
bad_list = []

def ospf_check(task):
    get_brief = task.run(task=netmiko_send_command, command_string="show ipv6 ospf int brief", use_genie=True)
    get_inter = task.run(task=netmiko_send_command, command_string="show ipv6 interfaces", use_genie=True)
    get_neighbor = task.run(task=netmiko_send_command, command_string="show ipv6 ospf neighbor", use_genie=True)
    get_ospf = task.run(task=netmiko_send_command, command_string="show ipv6 ospf", use_genie=True)
    task.host["brief_facts"] = get_brief.result
    task.host["inter_facts"] = get_inter.result
    task.host["neigh_facts"] = get_neighbor.result
    task.host["ospf_facts"] = get_ospf.result
    interface_outer = task.host["inter_facts"]
    neigh_outer = task.host["neigh_facts"]['interfaces']

    print(task.host["neigh_outer"])

results = nr.run(task=ospf_check)
