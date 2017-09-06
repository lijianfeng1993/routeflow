#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
from run_on_controller import get_networkinfo_and_insert_vminfo,insert_routerinfo,delete_all,handle_network_and_insert_networkinfo

def add_flowtable():
	insert_routerinfo()
	handle_network_and_insert_networkinfo()
	#os.system('curl http://192.168.1.21:8801/get_info_from_controller')
	#os.system('curl http://192.168.1.21:8801/stop')
	get_networkinfo_and_insert_vminfo()
	#print 'get network info ,and insert vminfo into database.'
	time.sleep(0.3)
	os.system('curl http://192.168.1.71:8801/get_info_from_controller_remove_flowtable')
	#os.system('curl http://192.168.1.31:8801/stop')
	time.sleep(0.5)
	print 'Routeflow add routetable execute successfull.'
	delete_all()

if __name__ == '__main__':
	add_flowtable()
