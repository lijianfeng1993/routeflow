#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from utility.sql_helper import MySqlHelper

class Vminfo(object):
	def __init__(self):
		self.__helper = MySqlHelper()
       
	def Get_Dict(self):
		sql = "select * from vminfo"
		return self.__helper.Get_Dict(sql)

	def Get_routerinfo_Dict(self):
		sql = "select * from routerinfo"
		return self.__helper.Get_routerinfo_Dict(sql)
 
	def Insert_vm_info(self,name,instance_name,ip,mac):
		sql = "insert into vminfo(name,instance_name,ip,mac) values('%s','%s','%s','%s')" % (name,instance_name,ip,mac)
		return self.__helper.Insert_vm_info(sql)

	def Get_network_info_Dict(self):
		sql = "select ports.id,subnets.network_id,subnets.cidr from ports inner join subnets on ports.network_id=subnets.network_id and subnets.name not like '%ipv6%'"
		return self.__helper.Get_network_info_Dict(sql)

	def Insert_routetable_network(self,network):
		sql = "insert into routetable(network) values ('%s')" % network
		return self.__helper.Insert_routetable_network(sql)


