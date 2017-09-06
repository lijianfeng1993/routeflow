#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle,route,run,request,post
import os,signal
from run_on_network import handle_network_and_insert_networkinfo

@route('/get_info_from_controller')
def get_info_from_controller():
	#print '处理网络和路由表，向数据库中routetable中插入可达性网络信息'
	handle_network_and_insert_networkinfo()	
	return '网络节点：已处理网络和路由表，并将可达性网络插入数据库.'

@route('/stop')
def stop():
	os.kill(os.getpid(),signal.SIGTERM)
	return 'webserver has closed.'

if __name__ == '__main__':
	try:
		run(host='0.0.0.0',port=8801)
	except Exception,ex:
		print ex
