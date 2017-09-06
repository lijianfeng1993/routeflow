#!/usr/bin/env python

import api as ovsdb
import commands

DEFAULT_OVS_VSCTL_TIMEOUT = 10
FAILMODE_SECURE = 'secure'

class BaseOVS(object):
	def __init__(self):
		self.vsctl_timeout = DEFAULT_OVS_VSCTL_TIMEOUT
		self.ovsdb = ovsdb.API()

	def add_bridge(self, bridge_name):
		self.ovsdb.add_br(bridge_name)
		return 

	def  delete_bridge(self, bridge_name):
		self.ovsdb.del_br(bridge_name)
		return

	def bridge_exists(self, bridge_name):
		return self.ovsdb.br_exists(bridge_name)

	# find bridge_name the iface accessed in.
	def get_bridge_for_iface(self, iface):
		return self.ovsdb.iface_to_br(iface)

	# find bridge_name the port accessed in.
	def get_bridge_for_port(self, port):
		return self.ovsdb.port_to_br(port)

	def get_bridges(self):
		return self.ovsdb.list_br()

	

class OVSBridge(BaseOVS):
	def __init__(self, br_name):
		super(OVSBridge, self).__init__()
		self.br_name = br_name

	def set_controller(self, controllers):
		pass

	def del_controller(self):
		pass

	def get_controller(self):
		pass

	def set_secure_mode(self):
		self.ovsdb.set_fail_mode(self.br_name, FAILMODE_SECURE)
		return 
	def del_secure_mode(self):
		self.ovsdb.del_fail_mode(self.br_name)
		return 

	def create(self):
		self.add_bridge(self.br_name)
		return 

	def destroy(self):
		self.delete_bridge(self.br_name)
		return 

	def add_port(self, port, *interface_attr_tuples):
		self.ovsdb.add_port(self.br_name, port)
		'''
		if interface_attr_tuples:
			self.ovsdb.db_set('Interface', port_name,
                                          *interface_attr_tuples))
                           '''
		return 

	def delete_port(self, port):
		self.ovsdb.del_port(self.br_name, port)
		return

	def list_ports(self):
		return self.ovsdb.list_ports(self.br_name)

	def run_ofctl(self, cmd, args):
		if type(args) is not list:
			full_args = 'ovs-ofctl ' + cmd + ' ' + self.br_name + ' ' + args
		else:
			str_args = ''
			for arg in args:
				str_args = str_args + arg + ' '
			full_args = 'ovs-ofctl ' + cmd + ' ' + self.br_name + ' ' + str_args
		try:
			#print full_args
			(status, output) = commands.getstatusoutput(full_args)
			if status ==0:
				return output
		except Exception as e:
			#raise('Unable to execute %s.' % full_args)
			return 'Unable to execute %s.' % full_args

	def count_flows(self):
		flow_list = self.run_ofctl("dump-flows", []).split("\n")[1:]
		return len(flow_list)

	def remove_all_flows(self):
		self.run_ofctl('del-flows ', [])
		return

	def do_action_flows(self, action, kwargs_list):
		flow_strs = [_build_flow_expr_str(kw, action) for kw in kwargs_list]
		if action == 'del':
			self.run_ofctl('%s-flows ' % action, '\n'.join(flow_strs))
		else:
			self.run_ofctl('%s-flow ' % action, '\n'.join(flow_strs))

	def add_flow(self, **kwargs):
		self.do_action_flows('add', [kwargs])

	def mod_flow(self, **kwargs):
		self.do_action_flows('mod', [kwargs])

	def delete_flows(self, **kwargs):
		self.do_action_flows('del', [kwargs])

	def dump_flows_for_table(self, table):
		retval = None
 		flow_str = "table=%s" % table
 		flows = self.run_ofctl("dump-flows", [flow_str])
 		if flows:
			retval = '\n'.join(item for item in flows.splitlines()
				if 'NXST' not in item)
		return retval


def _build_flow_expr_str(flow_dict, cmd):
	flow_expr_arr = []
	actions = None
	if cmd == 'add':
		flow_expr_arr.append("hard_timeout=%s" % 
			flow_dict.pop('hard_timeout', '0'))
		flow_expr_arr.append("idle_timeout=%s" % 
			flow_dict.pop('idle_timeout', '0'))
		flow_expr_arr.append("priority=%s" % 
			flow_dict.pop('priority', '1'))
	elif 'priority' in flow_dict:
		msg = _("Cannot match priority on flow deletion or modification")
		raise exceptions.InvalidInput(error_message=msg)

	if cmd != 'del':
		if "actions" not in flow_dict:
			msg = _("Must specify one or more actions on flow addition" 
				" or modification")
			raise exceptions.InvalidInput(error_message=msg)
		actions = "actions=%s" % flow_dict.pop('actions')

	for key, value in flow_dict.iteritems():
		if key == 'proto':
			flow_expr_arr.append(value)
		else:
			flow_expr_arr.append("%s=%s" % (key, str(value)))

	if actions:
		flow_expr_arr.append(actions)

	return ','.join(flow_expr_arr)


if __name__ == '__main__':
	baseovs = BaseOVS()
	#baseovs.add_bridge('br-int')
	#baseovs.delete_bridge('br-int')
	#print baseovs.bridge_exists('br-int')
	#print baseovs.get_bridges()
	br_int = OVSBridge('br-int')
	#br_int.add_port('eth0')
	#print br_int.list_ports()
	#br_int.delete_port('eth0')
	#print  baseovs.get_bridge_for_iface('eth0')
	#print baseovs.get_bridge_for_port('eth0')
	#br_int.set_secure_mode()
	#br_int.del_secure_mode()
	#br_tun = OVSBridge('br-tun')
	#br_tun.create()
	#br_tun.destroy()
	
	#br_int.remove_all_flows()
	#br_int.add_flow(table=3,
	#		priority=8,
	#		actions='NORMAL')
	
	#print br_int.dump_flows_for_table(3)
	#br_int.delete_flows(table=3)
	#print br_int.count_flows()
	br_int.remove_all_flows()





