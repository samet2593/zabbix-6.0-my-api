from pyzabbix import ZabbixAPI

USER = 'YOUR USERNAME'
PSWD = 'YOUR PASSWORD'
URL = 'http://*YOUR URL*/zabbix/api_jsonrpc.php'


zapi = ZabbixAPI(URL, timeout=5)
zapi.login(USER, PSWD)


group = zapi.hostgroup.get(filter={"name": "*HOST GROUP NAME*"}, output=["groupid"])
#example "group = zapi.hostgroup.get(filter={"name": "*hg_zabbix*"}, output=["groupid"])"
group_id = group[0]["groupid"]


ip_addresses = {}  # Dictionary to store IP addresses as keys and occurrence count as values

for hosts in zapi.host.get(
    output=['extend'],
    groupids=[group_id],
    selectInterfaces=['ip']
):
    interfaces = hosts['interfaces']
    for interface in interfaces:
        ip_address = interface['ip']
        if ip_address in ip_addresses:
            ip_addresses[ip_address].append(hosts['hostid'])
        else:
            ip_addresses[ip_address] = [hosts['hostid']]

# Print duplicate IP addresses and associated hosts
print("Duplicate IP addresses:")
for ip_address, hostids in ip_addresses.items():
    if len(hostids) > 1:
        print(f"IP address: {ip_address}")
        print("Hosts:")
        for hostid in hostids:
            host = zapi.host.get(output=['name'], hostids=hostid)[0]
            print(f"- {host['name']} (Host ID: {hostid})")
        print()
