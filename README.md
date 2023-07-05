# zabbix-6.0-my-api
We have a zabbix environment with a total of 10500 hosts.I'm using Zabbix 6.0.
The api named duplicate.py from the codes I shared lists duplicate records created in the host group you selected.
Another problem is that we couldn't parse the name of the automatically registered devices because it came dynamically. For this, we use the python visiblename_change, thanks to this code, we change the mac address a in the inventory part that we defined to the device with its visible name.
We made a sql partition so that Zabbix can run so many hosts well.
