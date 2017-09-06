#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import libvirt 
from xml.dom import minidom
import commands


def get_port_num_in_ovs(instance_name):
	# 通过libvirtAPI 从xml文件中解析出tap后面的编号
	conn = libvirt.open('qemu:///system')
	if conn == None:
		print('Failed to open connetion to qemu:///system')

	dom = conn.lookupByName(instance_name)
	if dom == None:
		print('Fail to find the domain %s' % instance_name)

	raw_xml = dom.XMLDesc()
	xml = minidom.parseString(raw_xml)
	domainTypes = xml.getElementsByTagName('target')
	for domainType in domainTypes:
		if 'tap' in domainType.getAttribute('dev'):
			port_num_from_libvirt = domainType.getAttribute('dev')[3:]
	# 得到OVS中对应端口的名字
	port_name_in_ovs = 'qvo%s' % port_num_from_libvirt

	# 从ovs中查询出该端口对应的port号
	try:
		(status,response) = commands.getstatusoutput('ovs-vsctl get Interface %s ofport' % port_name_in_ovs)
		return response
	except Exception:
		print 'Can not find %s from database.' % port_name_in_ovs
	'''
	try:
		(status,response) = commands.getstatusoutput('ovs-ofctl show br-int')
		index = response.index(port_name_in_ovs)
		p1 = response[index - 3]
		p2 = response[index - 2]
		# 目前只考虑了百个以内虚拟机的情况
		port_num = int(p1 + p2)
		#print instance_name + ' : ' + port_num
		return port_num
	except Exception:
		print 'Can not find %s from database.' % port_name_in_ovs
	'''
if __name__ == '__main__':
	get_port_num_in_ovs('instance-00000370')
	get_port_num_in_ovs('instance-00000371')
	get_port_num_in_ovs('instance-00000372')
