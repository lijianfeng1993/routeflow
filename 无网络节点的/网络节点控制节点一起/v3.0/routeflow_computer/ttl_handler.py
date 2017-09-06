#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from model.vminfo import Vminfo
from IPy import IP
import re

class Ttl_handler(object):
	# 计算节点之间数据转发的ttl,首先探测当前网络中路由器信息，以邻接表的方式表示成无向图，计算无向图中任意节点间的最小距离
	def __init__(self):
		vminfo = Vminfo()
		self.router_infos_ip = {}
		self.router_infos_net = {}
		self.graph = {}
		self.routerinfos = vminfo.Get_routerinfo_Dict()
		
		#将数据库中路由器信息处理成接口为ip的形式
		for routerinfo in self.routerinfos:
			router_name = routerinfo.get('name')
			iplist_str = routerinfo.get('iplist')
			pattern = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
			iplist_list = []
			for ip in pattern.findall(iplist_str):
				iplist_list.append(ip)
			self.router_infos_ip[router_name] = iplist_list
		# 将路由器信息处理成连接为网络号的形式
		for key in self.router_infos_ip.keys():
			values = self.router_infos_ip.get(key)
			for value in values:
				values[values.index(value)] = IP(value).make_net('255.255.255.0')
			self.router_infos_net[key] = values	


	def init_graph(self):
		for key in self.router_infos_net.keys():
			self.graph[key] = []
	
		# 根据路由器连接网络的情况创建无向图
		for key1 in self.router_infos_net.keys():
			for key2 in self.router_infos_net.keys():
				if key2 != key1:
					for value in self.router_infos_net.get(key2):
						if value in self.router_infos_net.get(key1):
							self.graph[key1].append(key2)
		return 
	
	# 计算图中任意两个节点间的最短路径				
	def find_shortest_path(self,start,end,path=[]):
		path = path + [start]
		if start == end:
			return path
		if not self.graph.has_key(start):
			return None
		shortest = None
		for node in self.graph[start]:
			if node not in path:
				newpath = self.find_shortest_path(node,end,path)
				if newpath:
					if not shortest or len(newpath) < len(shortest):
						shortest = newpath
		return shortest
		

if __name__ == '__main__':
	ttl_handler = Ttl_handler()
	ttl_handler.init_graph()
	print ttl_handler.find_shortest_path('kvm-router','kvm-router5')	
