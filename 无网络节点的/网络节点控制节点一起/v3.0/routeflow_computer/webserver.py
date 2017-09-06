#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle,route,run,request,post
import os,signal
from run_on_computer import get_vminfo_and_add_flowtable,get_vminfo_and_remove_flowtable

@route('/get_info_from_controller_add_flowtable')
def get_info_from_controller_add_flowtable():
	#print 'computer节点已经处理vminfo，并执行流表下发'
	get_vminfo_and_add_flowtable()
	return '计算节点：已经处理vminfo，并执行流表下发.'

@route('/get_info_from_controller_remove_flowtable')
def get_info_from_controller_remove_flowtable():
	get_vminfo_and_remove_flowtable()
	return '计算节点：已经删除相关流表.'

@route('/stop')
def stop():
	os.kill(os.getpid(),signal.SIGTERM)
	return 'webserver has closed.'

if __name__ == '__main__':
	try:
		run(host='0.0.0.0',port=8801)
	except Exception,ex:
		print ex
