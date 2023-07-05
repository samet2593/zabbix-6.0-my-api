from pyzabbix import ZabbixAPI

USER = 'YOUR USERNAME'
PSWD = 'YOUR PASSWORD'
URL = 'http://"YOUR URL"/zabbix/api_jsonrpc.php'


zapi = ZabbixAPI(URL, timeout=5)
zapi.login(USER, PSWD)


group = zapi.hostgroup.get(filter={"name": "Hostgroup_name"}, output=["groupid"])
group_id = group[0]["groupid"]


mac_addresses = {}  

for hosts in zapi.host.get(
    output=['extend'],
    groupids=[group_id],
    selectInventory=['macaddress_a']
):
    if 'inventory' in hosts and hosts['inventory'].get('macaddress_a'):
        mac_address = hosts['inventory']['macaddress_a']
        if mac_address in mac_addresses:
            mac_addresses[mac_address] += 1  # Increment occurrence count
            new_name = f"{mac_address}_{mac_addresses[mac_address] + 1}"
            while zapi.host.get(filter={"name": new_name}):
                mac_addresses[mac_address] += 1
                new_name = f"{mac_address}_{mac_addresses[mac_address] + 1}"
        else:
            mac_addresses[mac_address] = 0
            new_name = mac_address

        # Update the host's visible name as taken from the inventory
        zapi.host.update(
            hostid=hosts['hostid'],
            name=new_name
        )
    else:
        if 'inventory' in hosts:
            print(f"Skipping host {hosts['hostid']} because MAC address is missing or empty")
        else:
            name = hosts.get('name') or hosts['host']
            zapi.host.update(
                hostid=hosts['hostid'],
                name=name
            )
