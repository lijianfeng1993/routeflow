#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from utility.sql_helper import MySqlHelper

class Vminfo(object):
	def __init__(self):
		self.__helper = MySqlHelper()
       
	def Get_Dict(self):
		sql = "select * from vminfo"
		return self.__helper.Get_Dict(sql)
 
	def Insert_vm_info(self,name,instance_name,ip,mac):
		sql = "insert into vminfo(name,instance_name,ip,mac) values('%s','%s','%s','%s')" % (name,instance_name,ip,mac)
		return self.__helper.Insert_vm_info(sql)
