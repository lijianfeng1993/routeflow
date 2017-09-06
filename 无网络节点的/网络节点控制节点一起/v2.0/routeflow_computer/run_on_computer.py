#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from model.vminfo import Vminfo 
from computer import libvirt_test
from itertools import combinations
from computer.flowtable_handler import Flowtable_handler
import time

def get_vminfo_and_add_flowtable():
	vm = Vminfo()
	vminfos = vm.Get_Dict()
	for vminfo in vminfos:
		vminfo['ovs_port'] =  str(libvirt_test.get_port_num_in_ovs(vminfo['instance_name']))
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
		flowtable_handler.add_flowtable_into_ovs(ip1, ip2, mac1, mac2, host1_port, host2_port)
		time.sleep(0.3)

def get_vminfo_and_remove_flowtable():
    vm = Vminfo()
    vminfos = vm.Get_Dict()
    for vminfo in vminfos:
        vminfo['ovs_port'] =  str(libvirt_test.get_port_num_in_ovs(vminfo['instance_name']))
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
	#get_vminfo_and_add_flowtable()
	get_vminfo_and_remove_flowtable()

