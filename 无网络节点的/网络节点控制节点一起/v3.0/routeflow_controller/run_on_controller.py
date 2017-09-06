#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from model.vminfo import Vminfo 
from controller.jiaoji import getIntersection
from controller.get_need_hosts_info import get_need_hosts_infomation
from controller.get_router_info import get_router_info
import re
from IPy import IP
import commands

def get_networkinfo_and_insert_vminfo():
	# 提取数据库中可达网络，前提是网络节点中已经将路由表插入控制节点的数据库中
	vm = Vminfo()	
	need_nets_dict = vm.Get_access_network_Dict()
	#print need_nets_dict	
	need_nets = []
	for net_dict in need_nets_dict:
		need_nets.append(net_dict.get('network'))
	print need_nets
	# need_nets 内容为 ['10.0.223.0/24', '10.0.224.0/24', '10.0.111.0/24']	
	
	# 查找到need_nets中的所有主机信息，将其信息插入数据库中vminfo表中
	vminfos = get_need_hosts_infomation(*need_nets)
	print vminfos

	for vm_name in vminfos.keys():
		try:
			vm.Insert_vm_info(vm_name,vminfos.get(vm_name)[0],vminfos.get(vm_name)[1],vminfos.get(vm_name)[2])
			print 'Insert vminfo of %s successful.' % vm_name
		except Exception,e:
			print e.reason
	

def insert_routerinfo():	
	# 将当前网络中的虚拟路由器信息插入数据库
	vm = Vminfo()
	routers_info = get_router_info()
	print routers_info
	# {u'router2': [u'10.0.224.3', u'10.0.223.6'], u'router1': [u'10.0.111.21', u'10.0.223.5']}
	vm = Vminfo()
	for router_name in routers_info.keys():
		try:
			vm.Insert_router_info(router_name,routers_info.get(router_name))
			print 'Insert routerinfo of %s successful.' % router_name
		except Exception,e:
			print e 

def handle_network_and_insert_networkinfo():
	# 获取当前数据库中的所有网络信息,格式 ({'network_id': 'a9de4d55-ccbe-4a66-98bc-b1eac089f883', 'cidr': '10.0.111.0/24', 'id': '25756bbb-f905-4336-ab51-d6e42e7f1347'},....)
	vm = Vminfo()
	network_info = vm.Get_network_info_Dict()
	#print network_info	


	# 获取当前数据库routeflow中的虚拟路由器信息
	router = Vminfo()
	routerinfos = router.Get_routerinfo_Dict()
	# routerinfos格式 ({'iplist': "[u'10.0.224.3', u'10.0.223.6']", 'name': 'router2'}, {'iplist': "[u'10.0.111.21', u'10.0.223.5']", 'name': 'router1'})
	# 重新处理一下路由器信息
	routers_info = {}
	for routerinfo in routerinfos:
		router_name = routerinfo.get('name')
		iplist_str = routerinfo.get('iplist')
		pattern = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
		iplist_list = [] 
		for ip in pattern.findall(iplist_str):
			iplist_list.append(ip)
		routers_info[router_name] = iplist_list
	# 处理后的路由器信息 {'router2': ['10.0.224.3', '10.0.223.6'], 'router1': ['10.0.111.21', '10.0.223.5']}
	#print routers_info


	# 根据路由器的一个IP地址找到相应的网络命名空间namespace
	# 格式 {'10.0.224.3': 'qdhcp-9713a489-1bcc-418f-81e4-8d138db94c8a', '10.0.111.21': 'qdhcp-a9de4d55-ccbe-4a66-98bc-b1eac089f883'}
	routetable_needinfo = {}
	for router_name in routers_info.keys():
		ip1 = routers_info.get(router_name)[0]
		#print ip1
		for net_dict in network_info:
			if IP(ip1) in IP(net_dict.get('cidr')):
				routetable_needinfo[ip1] = 'qdhcp-' + net_dict.get('network_id')
				#print net_dict.get('network_id')
				break
	#print routetable_needinfo

	# 根据所有路由器中的路由表计算出共有的互通的网络
	routetables = {}
	routetables_filter_network = {}
	for ipaddr in routetable_needinfo.keys():
		network_list = []
		result = commands.getoutput('ip netns exec %s curl http://%s:4501/route' % (routetable_needinfo.get(ipaddr),ipaddr))
		pattern = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
		for ip in pattern.findall(result):
			network_list.append(ip)
		routetables_filter_network[ipaddr] = network_list
	#print routetables_filter_network
	#取所有路由器路由表中的交集
	network_list_all = []
	for ipaddr in routetables_filter_network.keys():
		network_list_all.append(routetables_filter_network.get(ipaddr))
	new_network_list = getIntersection(network_list_all)
	#print new_network_list 
	# 去掉重复和一些固定不需要的
	routetables_filter_network2 = list(set(new_network_list))	
	routetables_filter_network2.remove('255.255.255.0')
	routetables_filter_network2.remove('255.255.255.255')
	routetables_filter_network2.remove('169.254.169.254')
	routetables_filter_network2.remove('0.0.0.0')
	#print routetables_filter_network2
	
	# routetables_filter_network2 内容为 ['10.0.223.0', '10.0.223.1', '10.0.224.0', '10.0.111.0']
	# routetables_filter_network4 为最后需要的路由表,格式为 ['10.0.223.0/24', '10.0.224.0/24', '10.0.111.0/24']
	routetables_filter_network3 = []
	routetables_filter_network4 = []
	# 将末尾是0的地址取出来
	for ip in routetables_filter_network2:
		if ip.split('.')[-1] == '0':
			routetables_filter_network3.append(ip)
	for ip in routetables_filter_network3:
		routetables_filter_network4.append(ip + '/24')
	print routetables_filter_network4
	
	
	# 将可达性网络插入数据库
	for network in routetables_filter_network4:
		vm.Insert_routetable_network(network)
		print 'insert network %s to database successful.' % network

def delete_all():
	vm = Vminfo()
	vm.Delete_all_in_routerinfo()
	vm.Delete_all_in_routetable()
	vm.Delete_all_in_vminfo()	
	
if __name__ == '__main__':
	#insert_routerinfo()
	#handle_network_and_insert_networkinfo()
	#get_networkinfo_and_insert_vminfo()
	delete_all()
