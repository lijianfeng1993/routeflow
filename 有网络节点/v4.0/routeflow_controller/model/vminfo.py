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
	
	def Get_access_network_Dict(self):
		sql = "select * from routetable"
		return self.__helper.Get_access_network_Dict(sql)
 
	def Insert_vm_info(self,name,instance_name,ip,mac):
		sql = "insert into vminfo(name,instance_name,ip,mac) values('%s','%s','%s','%s')" % (name,instance_name,ip,mac)
		return self.__helper.Insert_vm_info(sql)

	def Insert_router_info(self,name,iplist):
		sql = 'insert into routerinfo(name,iplist) values("%s","%s")' % (name,iplist)
		return self.__helper.Insert_router_info(sql)

