#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from keystoneauth1 import identity
from keystoneauth1 import session
from neutronclient.v2_0.client import Client as neClient
from novaclient.client import Client as nvClient

credentials = {'username': 'admin','password': '123456','project_name': 'admin','project_domain_name': 'default','user_domain_name': 'default','auth_url': 'http://controller:35357/v3'}
auth = identity.Password(**credentials)
sess = session.Session(auth=auth)
nova_client = nvClient('2',session=sess)
neutron_client = neClient(session=sess)

def get_router_info():
	routers = []
	routers_info = {}
	for server in nova_client.servers.list():
		server_image_id = server.image.get('id')
		if server_image_id == '0a6e7051-14ae-48d0-8214-c854854751fa':
			routers.append(server)
	# print routers
	# return routers
	for router in routers:
		ipaddress = []
		for interface in router.interface_list():
			ipaddress.append(interface.fixed_ips[0].get('ip_address'))
		routers_info[router.name] = ipaddress
	#print routers_info
	return routers_info

if __name__ == '__main__':
	get_router_info()
