#!/usr/bin/python
import random
import string
import re

def xml_esc(s):
	s = s.replace('\'', '&apos;')
	s = s.replace('>', '&gt;')
	s = s.replace('<', '&lt;')
	return s
	
def macro_get_rand(args, source):
	try:
		f=int(args[0])
		t=int(args[1])
		return str(random.randrange(f, t))
	except:
		return ''

def macro_xml_escape(args, source):
	return xml_esc(args[0])

def macro_context(args, source):
	arg = args[0]
	if arg == 'conf':
		return xml_esc(source[1])
	elif arg == 'nick':
		return xml_esc(source[2])
	elif arg == 'conf_jid':
		return xml_esc(source[0])
	else:
		return ''

def read_file(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def write_file(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()
		
class MacroCommands:
	commands={
	          'rand':       [2, macro_get_rand  ],
                  'xml_escape': [1, macro_xml_escape],
		  'context':    [1, macro_context   ]
		 }
	
	def map_char(self, x, i):
		st=i['state']
		if i['esc']:
			i['esc']=False
			ret=i['level']
		elif x == '\\':
			i['esc']=True
			ret=0
		elif x == '%':
			i['state']='cmd_p'
			ret=0
		elif x == '(':
			if i['state'] == 'cmd_p':
				i['level']+=1
				i['state'] = 'args'
			ret=0
		elif x == ')':
			if i['state'] == 'args':
				i['state'] = 'null'
			ret=0
		else:
			if i['state'] == 'args':
				ret = i['level']
			else:
				i['state'] = 'null'
				ret = 0
		return ret

	def get_map(self, inp):
		i={'level': 0, 'state': 'null', 'esc': False}
		return [self.map_char(x, i) for x in list(inp)]
	
	def parse_cmd(self, me):
		i = 0
		m = self.get_map(me)
		args=[''] * max(m)
		while i<len(m):
			if m[i] != 0:
				args[m[i]-1]+=me[i]
			i+=1

		return args
	def execute_cmd(self, cmd, args, source):
		if self.commands.has_key(cmd):
			if self.commands[cmd][0] <= len(args):
				return self.commands[cmd][1](args, source)
		return ''
	def proccess(self, cmd, source):
		command = cmd[0]
		args = cmd[1:]
		return self.execute_cmd(command, args, source)

class Macros:
	macrolist={}
	accesslist={}
	macrocmds = MacroCommands()
	def init(self):
		self.macrolist = eval(read_file("dynamic/macros.txt"))
		self.accesslist = eval(read_file("dynamic/macroaccess.txt"))
	def flush(self):
		write_file('dynamic/macros.txt', str(self.macrolist))
		write_file('dynamic/macroaccess.txt', str(self.accesslist))
	def add(self, mapee, map):
		self.macrolist[mapee]=map
	def remove(self, mapee):
		if self.macrolist.has_key(mapee):
			del self.macrolist[mapee]
	def map_char(self, x, i):
		ret=i['level']
		if i['esc']:
			i['esc']=False
		elif x == '\\':
			i['esc']=True
			ret=0
		elif x == '`':
			i['larg'] = not i['larg']
			ret=0
		elif x == ' ':
			if not i['larg']:
				i['level']+=1
				ret=0
		return ret

	def get_map(self, inp):
		i={'larg': False, 'level': 1, 'esc': False}
		return [self.map_char(x, i) for x in list(inp)]
	
	def parse_cmd(self, me):
		i=0
		m = self.get_map(me)
		args=[''] * max(m)
		while i<len(m):
			if m[i] != 0:
				args[m[i]-1]+=me[i]
			i+=1
		return args

	def expand(self, cmd, source):
		if type(cmd) is None:
			return ''
		cl=self.parse_cmd(cmd)
		if (len(cl)<1):
			return cmd
		command=cl[0].split(' ')[0]
		args=cl[1:]
		exp = ''
		for macro in self.macrolist:
			if len(command)<=len(macro) and command == macro[0:len(macro)]:
				if self.macrolist[macro]:
					exp = self.apply(self.macrolist[macro], args, source)
		if not exp:
			return cmd
		rexp = self.expand(exp, source)
		return rexp
	def apply(self, macro, args, source):
		expanded = macro
		m=self.macrocmds.parse_cmd(macro)
		expanded = expanded.replace('$*', ' '.join(args));
		for i in m:
			cmd = [x.strip() for x in i.split(',')]
			for j in re.findall('\$[0-9]+', i):
				index = int(j[1:])-1
				if len(args)<=index:
					return expanded
				cmd = [x.replace(j, args[index]) for x in cmd]
			res = self.macrocmds.proccess(cmd, source)
			if res:
				expanded = expanded.replace('%('+i+')', res)
		for j in re.findall('\$[0-9]+', expanded):
			index = int(j[1:])-1
			if len(args)<=index:
				return expanded
			expanded = expanded.replace(j, args[index])
		return expanded
	def get_access(self, macro):
		if self.accesslist.has_key(macro):
			return self.accesslist[macro]
		return -1
	def give_access(self, macro, access):
		self.accesslist[macro] = access
