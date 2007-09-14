#! /usr/bin/env python
# -*- coding: utf-8 -*-

#  Talisman core
#  pybot.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@admin.ru.net>
#  Modifications Copyright © 2007 dimichxp <dimichxp@ezxdev.org>
#  Parts of code Copyright © Boris Kotov <admin@avoozl.ru> 

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import sys
import os
os.chdir(os.path.dirname(sys.argv[0]))

sys.path.insert(1, 'modules')

import xmpp
import string
import time
import thread
import random
import types
import traceback
import getopt
import codecs
import macros

################################################################################
CONFIGURATION_FILE = 'dynamic/config.cfg'

GENERAL_CONFIG_FILE = 'config.txt'

fp = open(GENERAL_CONFIG_FILE, 'r')
GENERAL_CONFIG = eval(fp.read())
fp.close()

SERVER = GENERAL_CONFIG['SERVER']
PORT = GENERAL_CONFIG['PORT']
USERNAME = GENERAL_CONFIG['USERNAME']
PASSWORD = GENERAL_CONFIG['PASSWORD']
RESOURCE = GENERAL_CONFIG['RESOURCE']

GROUPCHAT_CACHE_FILE = 'dynamic/conferences.list'
GLOBACCESS_FILE = 'dynamic/globaccess.cfg'
ACCBYCONF_FILE = 'dynamic/accbyconf.cfg'
PLUGIN_DIR = 'plugins'

DEFAULT_NICK = GENERAL_CONFIG['DEFAULT_NICK']
ADMINS = GENERAL_CONFIG['ADMINS']
ADMIN_PASSWORD = GENERAL_CONFIG['ADMIN_PASSWORD']

AUTO_RESTART = GENERAL_CONFIG['AUTO_RESTART']

PUBLIC_LOG_DIR = GENERAL_CONFIG['PUBLIC_LOG_DIR']
PRIVATE_LOG_DIR = GENERAL_CONFIG['PRIVATE_LOG_DIR']

INITSCRIPT_FILE = GENERAL_CONFIG['INITSCRIPT_FILE']

ROLES={'none':0, 'visitor':0, 'participant':10, 'moderator':15}
AFFILIATIONS={'none':0, 'member':1, 'admin':5, 'owner':15}
	
BOOT = time.time()
################################################################################

COMMANDS = {}
MACROS = macros.Macros()

GROUPCHATS = {}

############ lists handlers ############
MESSAGE_HANDLERS = []
OUTGOING_MESSAGE_HANDLERS = []
JOIN_HANDLERS = []
LEAVE_HANDLERS = []
IQ_HANDLERS = []
PRESENCE_HANDLERS = []
BAN_HANDLERS = []
KICK_HANDLERS = []
STATUS_CHANGE_HANDLERS = []
RA_HANDLERS = []
NICK_CHANGE_HANDLERS = []
########################

COMMAND_HANDLERS = {}

GLOBACCESS = {}
ACCBYCONF = {}

COMMOFF = {}

JCON = None

CONFIGURATION = {}

################################################################################
"""
optlist, args = getopt.getopt(sys.argv[1:], '', ['pid='])
for opt_tuple in optlist:
	if opt_tuple[0] == '--pid':
		pid_filename = opt_tuple[1]
		fp = open(pid_filename, 'w')
		fp.write(str(os.getpid()))
		fp.close()
"""
################################################################################

def initialize_file(filename, data=''):
	if not os.access(filename, os.F_OK):
		fp = file(filename, 'w')
		if data:
			fp.write(data)
		fp.close()

def read_file(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def write_file(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()
	
def check_file(gch,file):
	path,pathf='',''
	if gch:
		pathf='dynamic/'+gch+'/'+file
		path='dynamic/'+gch
	else:
		path='dynamic/'+file
		pathf='dynamic'
	if os.path.exists(pathf):
		return 1
	else:
		try:
			if not os.path.exists(path):
				os.mkdir(path)
			if os.access(pathf, os.F_OK):
				fp = file(pathf, 'w')
			else:
				fp = open(pathf, 'w')
			fp.write('{}')
			fp.close()
			return 1
		except:
			return 0	
	
################################################################################

initialize_file(CONFIGURATION_FILE, '{}')
try:
	CONFIGURATION = eval(read_file(CONFIGURATION_FILE))
except:
	print 'Error Parsing Configuration File'

def config_get(category, key):
	if CONFIGURATION.has_key(category):
		if CONFIGURATION[category].has_key(key):
			return CONFIGURATION[category][key]
		else:
			return None
	else:
		return None

def config_set(category, key, value):
	if not CONFIGURATION.has_key(category):
		CONFIGURATION[category] = {}
	CONFIGURATION[category][key] = value
	config_string = '{\n'
	for category in CONFIGURATION.keys():
		config_string += repr(category) + ':\n'
		for key in CONFIGURATION[category].keys():
			config_string += '\t' + repr(key) + ': ' + repr(CONFIGURATION[category][key]) + '\n'
		config_string += '\n'
	config_string += '}'
	write_file(CONFIGURATION_FILE, config_string)

################################################################################

def register_message_handler(instance):
	MESSAGE_HANDLERS.append(instance)
def register_outgoing_message_handler(instance):
	OUTGOING_MESSAGE_HANDLERS.append(instance)
def register_join_handler(instance):
	JOIN_HANDLERS.append(instance)
def register_leave_handler(instance):
	LEAVE_HANDLERS.append(instance)
def register_iq_handler(instance):
	IQ_HANDLERS.append(instance)
def register_presence_handler(instance):
	PRESENCE_HANDLERS.append(instance)
def register_kick_handler(instance):
	KICK_HANDLERS.append(instance)
def register_ban_handler(instance):
	BAN_HANDLERS.append(instance)
def register_status_change_handler(instance):
	STATUS_CHANGE_HANDLERS.append(instance)	
def register_ra_handler(instance):
	RA_HANDLERS.append(instance)
def nick_change_handler(instance):
	NICK_CHANGE_HANDLERS.append(instance)

def register_command_handler(instance, command, category=[], access=0, desc='', syntax='', examples=[]):
	command = command.decode('utf-8')
	COMMAND_HANDLERS[command] = instance
	COMMANDS[command] = {'category': category, 'access': access, 'desc': desc, 'syntax': syntax, 'examples': examples}

def call_message_handlers(type, source, body):
	for handler in MESSAGE_HANDLERS:
		thread.start_new_thread(handler, (type, source, body))
def call_outgoing_message_handlers(target, body):
	for handler in OUTGOING_MESSAGE_HANDLERS:
		thread.start_new_thread(handler, (target, body))
def call_join_handlers(groupchat, nick):
	for handler in JOIN_HANDLERS:
		thread.start_new_thread(handler, (groupchat, nick))
def call_leave_handlers(groupchat, nick, reason):
	for handler in LEAVE_HANDLERS:
		thread.start_new_thread(handler, (groupchat, nick))
def call_iq_handlers(iq):
	for handler in IQ_HANDLERS:
		thread.start_new_thread(handler, (iq,))
def call_presence_handlers(prs):
	for handler in PRESENCE_HANDLERS:
		thread.start_new_thread(handler, (prs,))
def call_kick_handlers(groupchat, nick, reason):
	for handler in KICK_HANDLERS:
		thread.start_new_thread(handler, (groupchat, nick, reason))
def call_ban_handlers(groupchat, nick, reason):
	for handler in BAN_HANDLERS:
		thread.start_new_thread(handler, (groupchat, nick, reason))
def call_status_change_handlers(groupchat, nick, status, stmsg):
	for handler in STATUS_CHANGE_HANDLERS:
		thread.start_new_thread(handler, (groupchat, nick, status, stmsg))	
def call_ra_handlers(groupchat, nick, aff, role, reason):
	for handler in RA_HANDLERS:
		thread.start_new_thread(handler, (groupchat, nick, aff, role, reason))	
def call_nick_change_handlers(groupchat, nick, newnick):
	for handler in NICK_CHANGE_HANDLERS:
		thread.start_new_thread(handler, (groupchat, nick, newnick))		
	
def call_command_handlers(command, type, source, parameters, callee):
	real_access = MACROS.get_access(callee, source[1])
	if real_access < 0:
		real_access = COMMANDS[command]['access']
	if COMMAND_HANDLERS.has_key(command):
		if has_access(source, real_access, source[1]):
			thread.start_new_thread(COMMAND_HANDLERS[command], (type, source, parameters))
		else:
			reply(type, source, 'ага, щаззз')

################################################################################

def find_plugins():
	valid_plugins = []
	invalid_plugins = []
	possibilities = os.listdir('plugins')
	for possibility in possibilities:
		if possibility[-3:].lower() == '.py':
			try:
				fp = file(PLUGIN_DIR + '/' + possibility)
				data = fp.read(23)
				if data == '#===istalismanplugin===':
					valid_plugins.append(possibility)
				else:
					invalid_plugins.append(possibility)
			except:
				pass
	if invalid_plugins:
		print '\nfailed to load',len(invalid_plugins),'plug-ins:'
		invalid_plugins.sort()
		invp=', '.join(invalid_plugins)
		print invp
		print 'plugins header is not corresponding\n'
	else:
		print '\nthere are not unloadable plug-ins'
	return valid_plugins

def load_plugins():
	plugins = find_plugins()
	for plugin in plugins:
		try:
			fp = file(PLUGIN_DIR + '/' + plugin)
			exec fp in globals()
			fp.close()
		except:
			raise
	plugins.sort()
	print '\nloaded',len(plugins),'plug-ins:'
	loaded=', '.join(plugins)
	print loaded,'\n'

def get_commoff(gch=None):
	if not gch:
		poss = os.listdir('dynamic')
		for x in poss:
			try:
				files = os.listdir('dynamic/'+x)
				for y in files:
					if y == 'config.cfg':
						cfgfile='dynamic/'+x+'/config.cfg'
						try:
							cfg = eval(read_file(cfgfile))
							if cfg.has_key('commoff'):
								commoff=cfg['commoff']
								COMMOFF[x]=x
								COMMOFF[x]=commoff
							else:
								COMMOFF[x]=x
								COMMOFF[x]=[]
						except:
							pass
			except:
				pass
	else:
		cfgfile='dynamic/'+gch+'/config.cfg'
		try:
			cfg = eval(read_file(cfgfile))
			if cfg.has_key('commoff'):
				commoff=cfg['commoff']
				COMMOFF[gch]=gch
				COMMOFF[gch]=commoff
			else:
				COMMOFF[gch]=gch
				COMMOFF[gch]=[]
		except:
			pass		

################################################################################

def get_conf_jid(gc, nick):
	if gc.has_key(nick):
		info = gc[nick]
		if info.has_key('jid') and info['jid']:
			return info['jid']
	return ''
	
def get_jid(source, parameter):
	groupchat = source[1]
	parameter = parameter.strip()
	jid = ''
	if parameter == '':
		parameter = source[2]
	if GROUPCHATS.has_key(groupchat):
		jid = get_conf_jid(GROUPCHATS[groupchat], parameter)
#	jid = get_true_jid(source)
	return jid

def get_true_jid(jid):
	true_jid = ''
	if type(jid) is types.ListType:
		jid = jid[0]
	if type(jid) is types.InstanceType:
		jid = unicode(jid)
	stripped_jid = string.split(jid, '/', 1)[0]
	resource = ''
	if len(string.split(jid, '/', 1)) == 2:
		resource = string.split(jid, '/', 1)[1]
	if GROUPCHATS.has_key(stripped_jid):
		if GROUPCHATS[stripped_jid].has_key(resource):
			true_jid = string.split(unicode(GROUPCHATS[stripped_jid][resource]['jid']), '/', 1)[0]
		else:
			true_jid = stripped_jid
	else:
		true_jid = stripped_jid
	return true_jid
	
def get_groupchat(jid):
	if type(jid) is types.ListType:
		jid = jid[1]
	jid = string.split(unicode(jid), '/')[0] # str(jid)
	if GROUPCHATS.has_key(jid):
		return jid
	else:
		return None

def get_bot_nick(groupchat):
	if check_file('','conferences.list'):
		gchdb = eval(read_file(GROUPCHAT_CACHE_FILE))
		if gchdb.has_key(groupchat):
			return gchdb[groupchat]
		else:
			return DEFAULT_NICK
	else:
		print 'Error adding groupchat to groupchats list file!'

def add_gch(groupchat, nick=None):
	if check_file('','conferences.list'):
		gchdb = eval(read_file(GROUPCHAT_CACHE_FILE))
		if nick:
			if not gchdb.has_key(groupchat):
				gchdb[groupchat] = groupchat
			gchdb[groupchat] = nick
		elif groupchat:
			del gchdb[groupchat]
		else:
			return
		write_file(GROUPCHAT_CACHE_FILE, str(gchdb))
	else:
		print 'Error adding groupchat to groupchats list file!'

################################################################################

def get_access_levels():
	global GLOBACCESS
	initialize_file(GLOBACCESS_FILE, '{}')
	GLOBACCESS = eval(read_file(GLOBACCESS_FILE))
	for jid in ADMINS:
		GLOBACCESS[jid] = 100
		write_file(GLOBACCESS_FILE, str(GLOBACCESS))
	

def change_access_temp(gch, source, level=0):
	global ACCBYCONF
	jid = get_true_jid(source)
	try:
		level = int(level)
	except:
		level = 0
	if not ACCBYCONF.has_key(gch):
		ACCBYCONF[gch] = gch
		ACCBYCONF[gch] = {}
	if not ACCBYCONF[gch].has_key(jid):
		ACCBYCONF[gch][jid]=jid
	ACCBYCONF[gch][jid]=level
	
def change_access_perm(gch, source, level=0):
	global ACCBYCONF
	jid = get_true_jid(source)
	try:
		level = int(level)
	except:
		level = 0
	temp_access = eval(read_file(ACCBYCONF_FILE))
	if not temp_access.has_key(gch):
		temp_access[gch] = gch
		temp_access[gch] = {}
	if not temp_access[gch].has_key(jid):
		temp_access[gch][jid]=jid
	temp_access[gch][jid]=level
	write_file(ACCBYCONF_FILE, str(temp_access))
	if not ACCBYCONF.has_key(gch):
		ACCBYCONF[gch] = gch
		ACCBYCONF[gch] = {}
	if not ACCBYCONF[gch].has_key(jid):
		ACCBYCONF[gch][jid]=jid
	ACCBYCONF[gch][jid]=level
	
def change_access_perm_glob(source, level=0):
	global GLOBACCESS
	jid = get_true_jid(source)
	temp_access = eval(read_file(GLOBACCESS_FILE))
	if level:
		temp_access[jid] = level
	else:
		del temp_access[jid]
	write_file(GLOBACCESS_FILE, str(temp_access))

def user_level(source, gch):
	global ACCBYCONF
	global GLOBACCESS
	ACCFILE = eval(read_file(ACCBYCONF_FILE))
	jid = get_true_jid(source)
	if GLOBACCESS.has_key(jid):
		return GLOBACCESS[jid]
	if ACCFILE.has_key(gch):
		if ACCFILE[gch].has_key(jid):
			return ACCFILE[gch][jid]
	if ACCBYCONF.has_key(gch):
		if ACCBYCONF[gch].has_key(jid):
			return ACCBYCONF[gch][jid]
	return 0

def has_access(source, level, gch):
	jid = get_true_jid(source)
	if user_level(jid,gch) >= int(level):
		return 1
	return 0
	
################################################################################

def join_groupchat(groupchat, passw=None):
	add_gch(groupchat, DEFAULT_NICK)
	presence=xmpp.protocol.Presence(groupchat+'/'+DEFAULT_NICK)
	presence.setStatus(u'напишите "помощь" и следуйте указаниям, чтобы понять что к чему!')
	pres=presence.setTag('x',namespace=xmpp.NS_MUC)
	pres.addChild('history',{'maxchars':'0','maxstanzas':'0'})
	if passw:
		pres.setTagData('password', passw)
	JCON.send(presence)
	if not GROUPCHATS.has_key(groupchat):
		GROUPCHATS[groupchat] = {}
	if check_file(groupchat,'macros.txt'):
		pass
	else:
		msg(groupchat, u'ВНИМАНИЕ!!! Локальная база макросов не была создана! Возникла ошибка, срочно сообщите о ней администраору бота!')
		
def leave_groupchat(groupchat):
	JCON.send(xmpp.Presence(groupchat, 'unavailable'))
	if GROUPCHATS.has_key(groupchat):
		del GROUPCHATS[groupchat]
		add_gch(groupchat)

def msg(target, body):
	msg = xmpp.Message(target, body)
	if GROUPCHATS.has_key(target):
		msg.setType('groupchat')
	else:
		msg.setType('chat')
	JCON.send(msg)
	call_outgoing_message_handlers(target, body)

def reply(ltype, source, body):
	if type(body) is types.StringType:
		body = body.decode('utf-8', 'backslashreplace')
	if ltype == 'public':
		if len(body)>1000:
			body=body[:1000]+u'[...]'
		msg(source[1], source[2] + ': ' + body)
	elif ltype == 'private':
		msg(source[0], body)

def isadmin(jid):
	if type(jid) is types.ListType:
		jid = jid[0]
	jid = str(jid)
	stripped_jid = string.split(jid, '/', 1)[0]
	resource = ''
	if len(string.split(jid, '/', 1)) == 2:
		resource = string.split(jid, '/', 1)[1]
	if stripped_jid in ADMINS:
		return 1
	elif GROUPCHATS.has_key(stripped_jid):
		if GROUPCHATS[stripped_jid].has_key(resource):
			if string.split(str(GROUPCHATS[stripped_jid][resource]['jid']), '/', 1)[0] in ADMINS:
				return 1
	return 0

################################################################################
def findPresenceItem(node):
	for p in [x.getTag('item') for x in node.getTags('x')]:
		if p != None:
			return p
	return None

def messageCB(con, msg):
	msgtype = msg.getType()
	body = msg.getBody()
	fromjid = msg.getFrom()
	cbody = ''
	rcmd = ''
	if body:
		rcmd = body.split(' ')[0]
		cbody = MACROS.expand(body, [fromjid, fromjid.getStripped(), fromjid.getResource()])
	command = ''
	parameters = ''
	mynick = get_bot_nick(fromjid.getStripped())
	if cbody and string.split(cbody):
		if mynick and cbody[0:len(mynick)+1] == mynick+':':
			nbody=cbody[len(mynick)+1:].strip().split();
			if nbody:
				command = nbody[0]
				parameters = ' '.join(nbody[1:])
		else:
			command = string.lower(string.split(cbody)[0])
			if cbody.count(' '):
				parameters = cbody[(cbody.find(' ') + 1):]
	if not msg.timestamp:
		if msgtype == 'groupchat':
			mtype='public'
		else:
			mtype='private'
		call_message_handlers(mtype, [fromjid, fromjid.getStripped(), fromjid.getResource()], body)
		if command in COMMANDS:
			try:
				if command in COMMOFF[fromjid.getStripped()]:
					return
			except:
				pass
			call_command_handlers(command, mtype, [fromjid, fromjid.getStripped(), fromjid.getResource()], unicode(parameters), rcmd)

def presenceCB(con, prs):
	call_presence_handlers(prs)
	ptype = prs.getType()
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	item = findPresenceItem(prs)

	if groupchat in GROUPCHATS:
		try:
			stmsg = prs.getStatus()
		except:
			stmsg=''
		try:
			status = prs.getShow()
		except:
			status = 'online'
		call_status_change_handlers(groupchat, nick, status, stmsg)
		try:
			aff=prs.getAffiliation()
			role=prs.getRole()
			reason=prs.getReason()
			call_ra_handlers(groupchat, nick, aff, role, reason)
		except:
			pass
		if ptype == 'available' or ptype == None:
			if not GROUPCHATS[groupchat].has_key(nick):
				if item == None:
					msg(groupchat, u'я кажется не имею прав модера... без них работать не могу. ухожу')
					leave_groupchat(groupchat)
				else:
					jid = item['jid']
					if jid != None:
						call_join_handlers(groupchat, nick)
				GROUPCHATS[groupchat][nick] = {'jid': jid, 'idle': time.time()}
				try:
					if GLOBACCESS.has_key(jid):
						return
				except:
					ACCFILE = eval(read_file(ACCBYCONF_FILE))
					if ACCFILE[groupchat].has_key(jid):
						pass
				else:
					if GROUPCHATS[groupchat].has_key(nick):
						role = item['role']
						aff = item['affiliation']
						if ROLES.has_key(role):
 							accr = ROLES[role]
						else:
							accr = 0
						if AFFILIATIONS.has_key(aff):
							acca = AFFILIATIONS[aff]
						else:
							acca = 0
						access = int(accr)+int(acca)
						change_access_temp(groupchat, jid, access)
		elif ptype == 'unavailable':
			if GROUPCHATS[groupchat].has_key(nick):
				del GROUPCHATS[groupchat][nick]
				try:
					code = prs.getStatusCode()
				except:
					code = None		
				try:
					reason = prs.getReason
				except:
					reason = None										
				call_leave_handlers(groupchat, nick, reason)
				if code:	
					if code == '307':
						call_kick_handlers(groupchat, nick, reason)	
					if code == '301':
						call_ban_handlers(groupchat, nick, reason)	
					if code == '303':	
						try:
							newnick = prs.getNick
						except:
							newnick = None								
						call_nick_change_handlers(groupchat, nick, newnick)
		elif ptype == 'error':
			try:
				code = prs.getErrorCode()
			except:
				code = None
			if code == '409':
				join_groupchat(groupchat, nick + '-')

def iqCB(con, iq):
	global JCON
	if iq.getTags('query', {}, xmpp.NS_VERSION):
		osname=os.popen("uname -sr", 'r')
		osver=osname.read().strip()
		osname.close()
		pipe = os.popen('sh -c ' + '"' + 'python -V 2>&1' + '"')
		pyver = pipe.read(1024).strip()
		osver = osver + ' ' + pyver
		result = iq.buildReply('result')
		query = result.getTag('query')
		query.setTagData('name', 'Тао-Альфа-Лямбда-Ипсилон-Сигма-Мю-Альфа-Ню')
		query.setTagData('version', 'alpha')
		query.setTagData('os', osver)
		JCON.send(result)
	else:
		call_iq_handlers(iq)
	

def dcCB():
	print 'DISCONNECTED'
	if AUTO_RESTART:
		print 'WAITING FOR RESTART...'
		time.sleep(5) # sleep for (240) 5 seconds - by als
		print 'RESTARTING'
		os.execl(sys.executable, sys.executable, sys.argv[0])
	else:
		sys.exit(0)

################################################################################

def start():
	global JCON
	JCON = xmpp.Client(server=SERVER, port=PORT, debug=[])

	get_access_levels()
	load_plugins()
	get_commoff()

	con=JCON.connect()
	if not con:
		print 'COULDN\'T CONNECT\nSleep for 30 seconds'
		time.sleep(30)
		sys.exit(1)
	else:
		print 'Connection Established'
	if con!='tls':
		print "Warning: unable to estabilish secure connection - TLS failed!"
		
	print 'Using',JCON.isConnected()
		
	auth=JCON.auth(USERNAME, PASSWORD, RESOURCE)
	if not auth:
		print 'Auth Error. Incorrect login/password?\nError: ', JCON.lastErr, JCON.lastErrCode
		sys.exit(0)
	else:
		print 'Logged In'
	if auth!='sasl':
		print 'Warning: unable to perform SASL auth. Old authentication method used!'


	JCON.RegisterHandler('message', messageCB)
	JCON.RegisterHandler('presence', presenceCB)
	JCON.RegisterHandler('iq', iqCB)
	JCON.RegisterDisconnectHandler(dcCB)
#	JCON.UnregisterDisconnectHandler(JCON.DisconnectHandler)
	print 'Handlers Registered'
	JCON.getRoster()
	JCON.sendInitPresence()
	print 'Entering Rooms'

	groupchats = eval(read_file(GROUPCHAT_CACHE_FILE))
	MACROS.init()
	for groupchat in groupchats:
		join_groupchat(groupchat)
		time.sleep(0.1)
		
#	load_plugins()

	print '\nOk, i\'m ready to work :)'

	while 1:
		JCON.Process(10)

if __name__ == "__main__":
	try:
		start()
	except KeyboardInterrupt:
		print '\nINTERUPT (Ctrl+C)'
#		for gch in GROUPCHATS.keys():
#			msg(gch,u'я получил Сtrl+C из консоли -> выключаюсь')
		sys.exit(0)
	except:
		if AUTO_RESTART:
			if sys.exc_info()[0] is not SystemExit:
				traceback.print_exc()
			try:
				JCON.disconnected()
			except IOError:
				pass
			try:
				time.sleep(3)
			except KeyboardInterrupt:
				print '\nINTERUPT (Ctrl+C)'
#				for gch in GROUPCHATS.keys():
#					msg(gch,u'я получил Сtrl+C из консоли -> выключаюсь')
				sys.exit(0)
			print 'RESTARTING'
			os.execl(sys.executable, sys.executable, sys.argv[0])
		else:
			raise

#EOF
