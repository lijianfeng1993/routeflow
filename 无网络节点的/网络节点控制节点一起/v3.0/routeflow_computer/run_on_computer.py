#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from model.vminfo import Vminfo 
from computer import libvirt_test
from ttl_handler import Ttl_handler
from itertools import combinations
from computer.flowtable_handler import Flowtable_handler
import time
from IPy import IP

# 将两个列表的元素进行组合
def twolist_zuhe(list1,list2):
	retList = []
	for a in list1:
		for b in list2:
			retList.append((a,b))
	return retList

def get_vminfo_and_add_flowtable():
	vm = Vminfo()
	vminfos = vm.Get_Dict()

	# 初始化ttl_handler
	ttl_hand = Ttl_handler()
	ttl_hand.init_graph()
	
	# 获取每一个主机信息，查找其在ovs中的ofport并添加为ovs_port属性值，查找主机所连接的路由器信息，添加为access_router属性值，为列表形式，在openstack中，可能会有多个路由器连到这个网络，因此，该属性值为连接路由器列表，后面会计算最短的路径
	router_infos_net = ttl_hand.router_infos_net
	for vminfo in vminfos:
		vminfo['ovs_port'] =  str(libvirt_test.get_port_num_in_ovs(vminfo['instance_name']))
		vminfo['access_router'] = []
		for router_name in router_infos_net.keys():
			router_iplist = router_infos_net.get(router_name)
			for ip in router_iplist:
				if IP(vminfo['ip']) in IP(ip):
					vminfo['access_router'].append(router_name)
	#print vminfos
	
	#将所有的虚拟机进行组合通信
	zuhe_list = list(combinations(vminfos,2))
	#print zuhe_list
	

	for tupul in zuhe_list:
		ip1 = tupul[0]['ip']
		mac1 = tupul[0]['mac']
		host1_port = tupul[0]['ovs_port']
		host1_access_router = tupul[0]['access_router']
		ip2 = tupul[1]['ip']
		mac2 = tupul[1]['mac']
		host2_port = tupul[1]['ovs_port']
		host2_access_router = tupul[1]['access_router']
		
		#计算所有组合的间隔路由器，并计算这些路由器的路径，去路径的最小值
		access_router_zuhe = twolist_zuhe(host1_access_router,host2_access_router)
		all_path_len = []
		for tupul2 in access_router_zuhe:
			all_path_len.append(len(ttl_hand.find_shortest_path(tupul2[0],tupul2[1])))
		min_len = min(all_path_len)
		ttl = str(64-min_len)
	
		print ip1, ip2, mac1, mac2, host1_port, host2_port, ttl
		flowtable_handler = Flowtable_handler('br-int')
		flowtable_handler.add_flowtable_into_ovs(ip1, ip2, mac1, mac2, host1_port, host2_port, ttl = ttl)
		#time.sleep(0.3)
	

def get_vminfo_and_remove_flowtable():
    vm = Vminfo()
    vminfos = vm.Get_Dict()
    for vminfo in vminfos:
        vminfo['ovs_port'] = str(libvirt_test.get_port_num_in_ovs(vminfo['instance_name']))
    print vminfos

    zuhe_list = list(combinations(vminfos,2))	
	
    for tupul in zuhe_list:
        ip1 = tupul[0]['ip']
        mac1 = tupul[0]['mac']
        host1_port = tupul[0]['ovs_port']
        ip2 = tupul[1]['ip']
        mac2 = tupul[1]['mac']
        host2_port = tupul[1]['ovs_port']
        print ip1, ip2, mac1, mac2, host1_port, host2_port
        flowtable_handler = Flowtable_handler('br-int')
        flowtable_handler.del_flowtable_from_ovs(ip1,ip2)
		#del_flow_to_ovs(ip1,ip2)
        time.sleep(0.3)

if __name__ == '__main__':
	get_vminfo_and_add_flowtable()
	#get_vminfo_and_remove_flowtable()

