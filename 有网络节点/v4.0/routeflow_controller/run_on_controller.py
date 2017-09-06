#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from model.vminfo import Vminfo 
from controller.get_need_hosts_info import get_need_hosts_infomation
from controller.get_router_info import get_router_info

def main():
		
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
	

	'''	
	# 将当前网络中的虚拟路由器信息插入数据库
	routers_info = get_router_info()
	# {u'router2': [u'10.0.224.3', u'10.0.223.6'], u'router1': [u'10.0.111.21', u'10.0.223.5']}
	vm = Vminfo()
	for router_name in routers_info.keys():
		try:
			vm.Insert_router_info(router_name,routers_info.get(router_name))
			print 'Insert routerinfo of %s successful.' % router_name
		except Exception,e:
			print e 
	'''
	
if __name__ == '__main__':
	main()

