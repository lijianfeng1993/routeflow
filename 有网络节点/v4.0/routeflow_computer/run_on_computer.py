#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from model.vminfo import Vminfo 
from computer import libvirt_test
from itertools import combinations
from computer.ovs import add_flow_to_ovs,del_flow_to_ovs
import time

def main():
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
		#add_flow_to_ovs(ip1, ip2, mac1, mac2, host1_port, host2_port)
		del_flow_to_ovs(ip1,ip2)
		time.sleep(0.3)

if __name__ == '__main__':
	main()

