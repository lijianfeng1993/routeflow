#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import os
import time
from run_on_controller import get_networkinfo_and_insert_vminfo,insert_routerinfo,delete_all

def stop_all_slaves():
    os.system('curl http://192.168.1.21:8801/stop')
    time.sleep(0.5)
    os.system('curl http://192.168.1.31:8801/stop')
    time.sleep(0.5)
    print 'Stop websever on Network_node and Computer_node.'
    

if __name__ == '__main__':
    stop_all_slaves()

