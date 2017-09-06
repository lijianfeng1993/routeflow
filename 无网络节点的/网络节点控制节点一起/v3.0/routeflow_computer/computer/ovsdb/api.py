#!/usr/bin/env python

import commands

class API(object):
	def __init__(self):
		pass

	def run_vsctl(self, action, opts, args):
		full_args = 'ovs-vsctl ' +  opts + action + args
		try:
			#print full_args
			(status, output) = commands.getstatusoutput(full_args)
			if status ==0:
				return output
		except Exception as e:
			#raise('Unable to execute %s.' % full_args)
			return 'Unable to execute %s.' % full_args

	def add_br(self, name, may_exist = True):
		opts = '--may-exist ' if may_exist else None
		args = name + ' '
		self.run_vsctl('add-br ', opts, args)

	def del_br(self, name, if_exists = True):
		opts = '--if-exists ' if if_exists else None
		args = name + ' '
		self.run_vsctl('del-br ', opts, args)

	def br_exists(self, name):
		opts = ''
		args = ''
		output = self.run_vsctl('list-br', opts, args)
		return True if name in output else False

	def iface_to_br(self, iface):
		opts = ''
		args = iface + ' '
		return self.run_vsctl('iface-to-br ',  opts, args)

	def port_to_br(self, port):
		opts = ''
		args = port + ''
		return self.run_vsctl('port-to-br ', opts, args)

	def list_br(self):
		opts = ''
		args = ''
		return self.run_vsctl('list-br ', opts, args)

	def add_port(self, br_name, port):
		opts = '--may-exist ' 
		args = br_name + ' ' + port + ' '
		return self.run_vsctl('add-port ', opts, args)

	def del_port(self, br_name, port):
		opts = '--if-exists '
		args = br_name + ' ' + port + ' '
		return self.run_vsctl('del-port ', opts, args)

	def list_ports(self, bridge_name):
		opts = ''
		args = bridge_name + ' '
		return self.run_vsctl('list-ports ', opts, args)

	def set_fail_mode(self, bridge, mode):
		opts = ''
		args = bridge + ' ' + mode
		return self.run_vsctl('set-fail-mode ', opts, args)

	def del_fail_mode(self, bridge):
		opts = ''
		args = bridge + ' '
		return self.run_vsctl('del-fail-mode ', opts, args)


