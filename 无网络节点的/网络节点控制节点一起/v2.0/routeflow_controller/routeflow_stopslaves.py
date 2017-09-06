#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import os
import time
from run_on_controller import get_networkinfo_and_insert_vminfo,insert_routerinfo,delete_all

def stop_all_slaves():
    os.system('curl http://192.168.1.71:8801/stop')
    print 'Stop websever on Network_node and Computer_node.'
    

if __name__ == '__main__':
    stop_all_slaves()

