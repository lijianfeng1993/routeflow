#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import MySQLdb

class MySqlHelper(object):
	def __init__(self):
		pass

	def Get_Dict(self,sql):
		conn = MySQLdb.connect(host = '192.168.1.11',user = 'root', passwd = '123456', port = 3306, db = 'routeflow')
		cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        
		reCount = cur.execute(sql)
		data = cur.fetchall()
        
		cur.close()
		conn.close()
		return data

	def Get_routerinfo_Dict(self,sql):
		conn = MySQLdb.connect(host = '192.168.1.11',user = 'root', passwd = '123456', port = 3306, db = 'routeflow')
		cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
		reCount = cur.execute(sql)
		data = cur.fetchall()
		cur.close()
		conn.close()
		return data

	def Get_access_network_Dict(self,sql):
		conn = MySQLdb.connect(host = '192.168.1.11',user = 'root', passwd = '123456', port = 3306, db = 'routeflow')
		cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
		reCount = cur.execute(sql)
		data = cur.fetchall()
		cur.close()
		conn.close()
		return data	

	def Insert_vm_info(self,sql):
		conn = MySQLdb.connect(host = '192.168.1.11',user = 'root', passwd = '123456', port = 3306, db = 'routeflow') 
		cur = conn.cursor()
		reCount = cur.execute(sql)
		conn.commit()
		cur.close()
		conn.close()
		return reCount
 		
	def Insert_router_info(self,sql):
		conn = MySQLdb.connect(host = '192.168.1.11',user = 'root', passwd = '123456', port = 3306, db = 'routeflow')
		cur = conn.cursor()
		reCount = cur.execute(sql)
		conn.commit()
		cur.close()
		conn.close()
		return reCount
