#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
from run_on_controller import get_networkinfo_and_insert_vminfo,insert_routerinfo,delete_all

def remove_flowtable():
	insert_routerinfo()
	time.sleep(0.5)
	os.system('curl http://192.168.1.21:8801/get_info_from_controller')
	#os.system('curl http://192.168.1.21:8801/stop')
	time.sleep(0.5)
	get_networkinfo_and_insert_vminfo()
	#print 'get network info ,and insert vminfo into database.'
	time.sleep(0.5)
	os.system('curl http://192.168.1.31:8801/get_info_from_controller_remove_flowtable')
	#os.system('curl http://192.168.1.31:8801/stop')
	time.sleep(0.5)
	print 'Routeflow remove flowtable execute successfull.'
	delete_all()

if __name__ == '__main__':
	remove_flowtable()
