#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import commands

def add_flow_to_ovs(ip1, ip2, mac1, mac2, host1_port, host2_port):
	commands.getstatusoutput('ovs-ofctl add-flow br-int table=0,priority=15,ip,nw_src=%s,nw_dst=%s,actions=mod_dl_src:%s,mod_dl_dst:%s,output:%s' % (ip1, ip2, mac1, mac2, host2_port))
	commands.getstatusoutput('ovs-ofctl add-flow br-int table=0,priority=15,ip,nw_src=%s,nw_dst=%s,actions=mod_dl_src:%s,mod_dl_dst:%s,output:%s' % (ip2, ip1, mac2, mac1, host1_port))
	print 'add flowtable of  %s to %s successful.' % (ip1,ip2)
	#print 'ovs-ofctl add-flow br-int table=0,priority=15,ip,nw_src=%s,nw_dst=%s,actions=mod_dl_src:%s,mod_dl_dst:%s,output:%s' % (ip1, ip2, mac1, mac2, host2_port)
	#print 'ovs-ofctl add-flow br-int table=0,priority=15,ip,nw_src=%s,nw_dst=%s,actions=mod_dl_src:%s,mod_dl_dst:%s,output:%s' % (ip2, ip1, mac2, mac1, host1_port)


def del_flow_to_ovs(ip1,ip2):
	commands.getstatusoutput('ovs-ofctl del-flows br-int nw_src=%s,nw_dst=%s' % (ip1, ip2))
	commands.getstatusoutput('ovs-ofctl del-flows br-int nw_src=%s,nw_dst=%s' % (ip2, ip1))
	print 'del flowtable of  %s to %s successful.' % (ip1,ip2) 


if __name__ == '__main__':
	#add_flow_to_ovs('10.0.111.202', '192.168.11.212', 'fa:16:3e:53:d1:af', 'fa:16:3e:11:69:64', '24', '23')
	del_flow_to_ovs('10.0.111.202', '192.168.11.212')
	
	

