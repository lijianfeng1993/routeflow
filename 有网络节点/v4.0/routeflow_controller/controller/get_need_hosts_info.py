#!/usr/bin/env python
# -*- coding:utf-8 -*-

from IPy import IP
from keystoneauth1 import identity
from keystoneauth1 import session
from novaclient.v2.client import Client as nvClient

credentials = {'username':'admin','password':'123456','project_name':'admin','project_domain_name':'default','user_domain_name':'default','auth_url':'http://controller:35357/v3'}

auth=identity.Password(**credentials)
sess=session.Session(auth=auth)
nova_client = nvClient(session = sess)

def get_need_hosts_infomation(*need_nets):
	need_servers = {}
	servers =  nova_client.servers.list()
	for server in servers:
		interface_list = server.interface_list()
		if len(interface_list) == 1:
			for net in need_nets:
				ip_address = interface_list[0].fixed_ips[0].get('ip_address')
				instance_name = getattr(server,'OS-EXT-SRV-ATTR:instance_name')
				if ip_address in IP(net):
					for k,v in server.addresses.items():
						mac = v[0].get('OS-EXT-IPS-MAC:mac_addr')
					need_servers[server.name] = [instance_name,ip_address,mac]
	#print need_servers
	return need_servers


if __name__ == '__main__':
	need_nets = ['10.0.111.0/24','10.0.222.0/24','10.0.223.0/24']
	get_need_hosts_infomation(*need_nets)




