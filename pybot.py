#! /usr/bin/env python
# -*- coding: utf-8 -*-

#  Talisman core
#  pybot.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2007 dimichxp <dimichxp@gmail.com>
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
import codecs
import macros

import locale
locale.setlocale(locale.LC_CTYPE, "")


################################################################################
GENERAL_CONFIG_FILE = 'config.txt'

fp = open(GENERAL_CONFIG_FILE, 'r')
GENERAL_CONFIG = eval(fp.read())
fp.close()

SERVER = GENERAL_CONFIG['SERVER']
PORT = GENERAL_CONFIG['PORT']
USERNAME = GENERAL_CONFIG['USERNAME']
PASSWORD = GENERAL_CONFIG['PASSWORD']
RESOURCE = GENERAL_CONFIG['RESOURCE']

GROUPCHAT_CACHE_FILE = 'dynamic/chatrooms.list'
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

LAST,BOOT = {},0
LAST['c']=''
LAST['t']=0
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
########################

COMMAND_HANDLERS = {}

GLOBACCESS = {}
ACCBYCONF = {}
ACCBYCONFFILE = {}

COMMOFF = {}
GREETZ={}

GCHCFGS={}

JCON = None
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

#def write_file(filename, data):
#	fp = file(filename, 'w')
#	fp.write(data)
#	fp.close()
	
def write_file(filename, data):
	mtx=thread.allocate_lock()
	mtx.acquire()
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()
	mtx.release()

def check_file(gch='',file=''):
	pth,pthf='',''
	if gch:
		pthf='dynamic/'+gch+'/'+file
		pth='dynamic/'+gch
	else:
		pthf='dynamic/'+file
		pth='dynamic'
	if os.path.exists(pthf):
		return 1
	else:
		try:
			if not os.path.exists(pth):
				os.mkdir(pth,0755)
			if os.access(pthf, os.F_OK):
				fp = file(pthf, 'w')
			else:
				fp = open(pthf, 'w')
			fp.write('{}')
			fp.close()
			return 1
		except:
			return 0

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

def register_command_handler(instance, command, category=[], access=0, desc='', syntax='', examples=[]):
	command = command.decode('utf-8')
	COMMAND_HANDLERS[command] = instance
	COMMANDS[command] = {'category': category, 'access': access, 'desc': desc, 'syntax': syntax, 'examples': examples}

def call_message_handlers(type, source, body):
	for handler in MESSAGE_HANDLERS:
		thread.start_new_thread(handler, (type, source, body,))
def call_outgoing_message_handlers(target, body):
	for handler in OUTGOING_MESSAGE_HANDLERS:
		thread.start_new_thread(handler, (target, body,))
def call_join_handlers(groupchat, nick, afl, role):
	for handler in JOIN_HANDLERS:
		thread.start_new_thread(handler, (groupchat, nick, afl, role,))
def call_leave_handlers(groupchat, nick, reason, code):
	for handler in LEAVE_HANDLERS:
		thread.start_new_thread(handler, (groupchat, nick, reason, code,))
def call_iq_handlers(iq):
	for handler in IQ_HANDLERS:
		thread.start_new_thread(handler, (iq,))
def call_presence_handlers(prs):
	for handler in PRESENCE_HANDLERS:
		thread.start_new_thread(handler, (prs,))

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
	print '\nLOADING PLUGINS'
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

def get_commoff(gch):
	try:
		if GCHCFGS[gch].has_key('commoff'):
			commoff=GCHCFGS[gch]['commoff']
			COMMOFF[gch]=gch
			COMMOFF[gch]=commoff
		else:
			COMMOFF[gch]=gch
			COMMOFF[gch]=[]
	except:
		pass
			
def get_greetz(gch):
	grtfile='dynamic/'+gch+'/greetz.txt'
	try:
		grt = eval(read_file(grtfile))
		if gch in GREETZ.keys():
			GREETZ[gch]=grt
		else:
			GREETZ[gch]=gch
			GREETZ[gch]=grt				
	except:
		pass
			
def get_gch_cfg(gch):
	cfgfile='dynamic/'+gch+'/config.cfg'
	if not check_file(gch,'config.cfg'):
		print 'unable to create config file for new groupchat!'
		raise
	try:
		cfg = eval(read_file(cfgfile))
		GCHCFGS[gch]=gch
		GCHCFGS[gch]=cfg
	except:
		pass

def get_order_pl_cfg(gch):
	if not 'filt' in GCHCFGS[gch]:
		GCHCFGS[gch]['filt']={}		
	for x in ['smile','time','presence','len','like','caps','prsstlen','obscene','kicks','fly']:
		if x == 'kicks':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={}
				GCHCFGS[gch]['filt'][x]['cond']=1
				GCHCFGS[gch]['filt'][x]['cnt']=2
			continue
		if x == 'fly':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={}
				GCHCFGS[gch]['filt'][x]['cond']=1
				GCHCFGS[gch]['filt'][x]['mode']='ban'
				GCHCFGS[gch]['filt'][x]['time']=60
			continue
		if not x in GCHCFGS[gch]['filt']:
			GCHCFGS[gch]['filt'][x]=1
	DBPATH='dynamic/'+gch+'/config.cfg'
	write_file(DBPATH, str(GCHCFGS[gch]))
	
def get_sendpl_cache(gch):
	sfc='dynamic/'+gch+'/send.txt'
	if not check_file(gch,'send.txt'):
		print 'error with caches in send_plugin.py'
		raise
	try:
		cache = eval(read_file(sfc))
		sendqueue[gch]=gch
		sendqueue[gch]={}
		sendqueue[gch]=cache
	except:
		pass	

################################################################################

"""
def get_true_jid(jid):
	true_jid = ''
	if type(jid) is types.ListType:
		jid = jid[0]
	if type(jid) is types.InstanceType:
		jid = unicode(jid)
	jid = string.split(jid, '/', 1)
	stripped_jid = jid[0]
	resource = ''
	if len(jid) == 2:
		resource = jid[1]
	if GROUPCHATS.has_key(stripped_jid):
		if GROUPCHATS[stripped_jid].has_key(resource):
			true_jid = string.split(unicode(GROUPCHATS[stripped_jid][resource]['jid']), '/', 1)[0]
		else:
			true_jid = None
	else:
		true_jid = None
	return true_jid
"""

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

def get_bot_nick(groupchat):
	if check_file(file='chatrooms.list'):
		gchdb = eval(read_file(GROUPCHAT_CACHE_FILE))
		if gchdb.has_key(groupchat):
			return gchdb[groupchat]['nick']
		else:
			return DEFAULT_NICK
	else:
		print 'Error adding groupchat to groupchats list file!'

def add_gch(groupchat=None, nick=None, passw=None):
	if check_file(file='chatrooms.list'):
		gchdb = eval(read_file(GROUPCHAT_CACHE_FILE))
		if not groupchat in gchdb:
			gchdb[groupchat] = groupchat
			gchdb[groupchat] = {}
			gchdb[groupchat]['nick'] = nick
			gchdb[groupchat]['passw'] = passw
		else:
			if nick and groupchat and passw:
				gchdb[groupchat]['nick'] = nick
				gchdb[groupchat]['passw'] = passw
			elif nick and groupchat:
				gchdb[groupchat]['nick'] = nick
			elif groupchat:
				del gchdb[groupchat]
			elif passw:
				gchdb[groupchat]['passw'] = passw
			else:
				return 0
		write_file(GROUPCHAT_CACHE_FILE, str(gchdb))
		return 1
	else:
		print 'Error adding groupchat to groupchats list file!'

################################################################################

def get_access_levels():
	global GLOBACCESS
	global ACCBYCONFFILE
	GLOBACCESS = eval(read_file(GLOBACCESS_FILE))
	for jid in ADMINS:
		GLOBACCESS[jid] = 100
		write_file(GLOBACCESS_FILE, str(GLOBACCESS))
	ACCBYCONFFILE = eval(read_file(ACCBYCONF_FILE))


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

def change_access_perm(gch, source, level=None):
	global ACCBYCONF
	jid = get_true_jid(source)
	try:
		level = int(level)
	except:
		pass
	temp_access = eval(read_file(ACCBYCONF_FILE))
	if not temp_access.has_key(gch):
		temp_access[gch] = gch
		temp_access[gch] = {}
	if not temp_access[gch].has_key(jid):
		temp_access[gch][jid]=jid
	if level:
		temp_access[gch][jid]=level
	else:
		del temp_access[gch][jid]
	write_file(ACCBYCONF_FILE, str(temp_access))
	if not ACCBYCONF.has_key(gch):
		ACCBYCONF[gch] = gch
		ACCBYCONF[gch] = {}
	if not ACCBYCONF[gch].has_key(jid):
		ACCBYCONF[gch][jid]=jid
	if level:
		ACCBYCONF[gch][jid]=level
	else:
		del ACCBYCONF[gch][jid]
	get_access_levels()

def change_access_perm_glob(source, level=0):
	global GLOBACCESS
	jid = get_true_jid(source)
	temp_access = eval(read_file(GLOBACCESS_FILE))
	if level:
		temp_access[jid] = level
	else:
		del temp_access[jid]
	write_file(GLOBACCESS_FILE, str(temp_access))
	get_access_levels()
	
def change_access_temp_glob(source, level=0):
	global GLOBACCESS
	jid = get_true_jid(source)
	if level:
		GLOBACCESS[jid] = level
	else:
		del GLOBACCESS[jid]

def user_level(source, gch):
	global ACCBYCONF
	global GLOBACCESS
	global ACCBYCONFFILE
	jid = get_true_jid(source)
	if GLOBACCESS.has_key(jid):
		return GLOBACCESS[jid]
	if ACCBYCONFFILE.has_key(gch):
		if ACCBYCONFFILE[gch].has_key(jid):
			return ACCBYCONFFILE[gch][jid]
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

def join_groupchat(groupchat=None, nick=DEFAULT_NICK, passw=None):
	prs=xmpp.protocol.Presence(groupchat+'/'+nick)
	prs.setStatus(u'напишите "помощь" и следуйте указаниям, чтобы понять как со мной работать')
	pres=prs.setTag('x',namespace=xmpp.NS_MUC)
	pres.addChild('history',{'maxchars':'0','maxstanzas':'0'})
	if passw:
		pres.setTagData('password', passw)
	JCON.send(prs)
	if not groupchat in GROUPCHATS:
		GROUPCHATS[groupchat] = {}
	if check_file(groupchat,'macros.txt'):
		pass
	else:
		msg(groupchat, u'ВНИМАНИЕ!!! Локальная база макросов не была создана! Возникла ошибка, срочно сообщите о ней администраору бота!')

def leave_groupchat(groupchat,status=''):
	prs=xmpp.Presence(groupchat, 'unavailable')
	if status:
		prs.setStatus(status)
	JCON.send(prs)
	if GROUPCHATS.has_key(groupchat):
		del GROUPCHATS[groupchat]
		add_gch(groupchat)

def msg(target, body):
	msg = xmpp.Message(target, body)
	if GROUPCHATS.has_key(target):
		if len(body)>1000:
			body=body[:1000]+u' >>>>'
		msg.setType('groupchat')
	else:
		msg.setType('chat')
	JCON.send(msg)
	call_outgoing_message_handlers(target, body)

def reply(ltype, source, body):
	if type(body) is types.StringType:
		body = body.decode('utf8', 'replace').strip()
	if ltype == 'public':
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

def messageHnd(con, msg):
	msgtype = msg.getType()
	fromjid = msg.getFrom()
	if fromjid.getStripped() not in GROUPCHATS and fromjid.getStripped() not in ADMINS:
		return
	if user_level(fromjid,fromjid.getStripped())==-100:
		return
	if msg.timestamp:
		return
	body = msg.getBody()
	if body:
		body=body.strip()
	if not body:
		return
	if len(body)>1000:
		body=body[:1000]+u' >>>>'	
	if msgtype == 'groupchat':
		mtype='public'
		if GROUPCHATS.has_key(fromjid.getStripped()) and GROUPCHATS[fromjid.getStripped()].has_key(fromjid.getResource()):
			GROUPCHATS[fromjid.getStripped()][fromjid.getResource()]['idle'] = time.time()	
	elif msgtype == 'error':
		if msg.getErrorCode()=='500':
			time.sleep(0.6)
			JCON.send(xmpp.Message(fromjid, body, 'groupchat'))
			return
		return
	else:
		mtype='private'
	call_message_handlers(mtype, [fromjid, fromjid.getStripped(), fromjid.getResource()], body)
	LAST=time.time()
	
	bot_nick = get_bot_nick(fromjid.getStripped())
	if bot_nick == fromjid.getResource():
		return
	command,parameters,cbody,rcmd = '','','',''
	for x in [bot_nick+x for x in [':',',','>']]:
		body=body.replace(x,'')
#	if bot_nick and body.split()[0] in [bot_nick+x for x in [':',',','>']]:
#		body=' '.join(body.split()[1:])
	body=body.strip()
	if not body:
		return
	rcmd = body.split(' ')[0].lower()
	if fromjid.getStripped() in COMMOFF and rcmd in COMMOFF[fromjid.getStripped()]:
		return
	cbody = MACROS.expand(body, [fromjid, fromjid.getStripped(), fromjid.getResource()])
	command=cbody.split()[0].lower()
	if cbody.count(' '):
		parameters = cbody[(cbody.find(' ') + 1):].strip()
	if command in COMMANDS:
		if fromjid.getStripped() in COMMOFF and command in COMMOFF[fromjid.getStripped()]:
			return
		else:
			call_command_handlers(command, mtype, [fromjid, fromjid.getStripped(), fromjid.getResource()], unicode(parameters), rcmd)
			globals()['LAST']['t'] = time.time()
			globals()['LAST']['c'] = command

def presenceHnd(con, prs):
	ptype = prs.getType()
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	item = findPresenceItem(prs)
	
	if ptype == 'subscribe':
		JCON.send(xmpp.protocol.Presence(to=prs.getFrom(), typ='subscribed'))
	elif ptype == 'unsubscribe':
		JCON.send(xmpp.protocol.Presence(to=prs.getFrom(), typ='unsubscribed'))

	if groupchat in GROUPCHATS:
		if ptype == 'unavailable':
			jid = item['jid']
			scode = prs.getStatusCode()
			reason = prs.getStatus()
			if scode == '303':
				newnick = prs.getNick()
				GROUPCHATS[groupchat][newnick] = {'jid': jid, 'idle': time.time(), 'joined': time.time(), 'ishere': 1}
				for x in ['idle','status','stmsg','joined','status','stmsg']:
					try:
						del GROUPCHATS[groupchat][nick][x]
						if GROUPCHATS[groupchat][nick]['ishere']==1:
							GROUPCHATS[groupchat][nick]['ishere']=0
					except:
						pass
			else:
				for x in ['idle','status','stmsg','joined','status','stmsg']:
					try:
						del GROUPCHATS[groupchat][nick][x]
						if GROUPCHATS[groupchat][nick]['ishere']==1:
							GROUPCHATS[groupchat][nick]['ishere']=0
					except:
						pass
				call_leave_handlers(groupchat, nick, reason, scode)
		elif ptype == 'available' or ptype == None:
			jid = item['jid']
			afl=prs.getAffiliation()
			role=prs.getRole()
			if not jid:
				time.sleep(2)
				msg(groupchat, u'моя функциональность в полной мере без прав модератора невозможна')
				time.sleep(1)
				leave_groupchat(groupchat, u'отсутствие прав модератора')        
				return
			else:
				if nick in GROUPCHATS[groupchat] and GROUPCHATS[groupchat][nick]['jid']==jid and GROUPCHATS[groupchat][nick]['ishere']==1:
					pass
				else:
					GROUPCHATS[groupchat][nick] = {'jid': jid, 'idle': time.time(), 'joined': time.time(), 'ishere': 1, 'status': '', 'stmsg': ''}
					if role=='moderator' or user_level(jid,groupchat)>=15:
						GROUPCHATS[groupchat][nick]['ismoder'] = 1
					else:
						GROUPCHATS[groupchat][nick]['ismoder'] = 0
					call_join_handlers(groupchat, nick, afl, role)
		elif ptype == 'error':
			ecode = prs.getErrorCode()
			if ecode:
				if ecode == '409':
					join_groupchat(groupchat, nick + '-')
				elif ecode == '404':
					del GROUPCHATS[groupchat]
				elif ecode in ['401','403','405',]:
					del GROUPCHATS[groupchat]
					add_gch(groupchat)
				elif ecode == '503':
					time.sleep(60)
					join_groupchat(groupchat, nick)
		else:
			pass
		call_presence_handlers(prs)

def iqHnd(con, iq):
	global JCON
	if iq.getTags('query', {}, xmpp.NS_VERSION):
		osname=os.popen("uname -sr", 'r')
		osver=osname.read().strip()
		osname.close()
		pyver = sys.version
		osver = osver + ' ' + pyver
		result = iq.buildReply('result')
		query = result.getTag('query')
		query.setTagData('name', 'ταλιςμαη')
		query.setTagData('version', 'ver.1 (svn rev 65) [antiflood]')
#		query.setTagData('version', 'ver.1 (author ver) [antiflood]')
		query.setTagData('os', osver)
		JCON.send(result)
		raise xmpp.NodeProcessed
	elif iq.getTags('time', {}, 'urn:xmpp:time'):
		tzo=(lambda tup: tup[0]+"%02d:"%tup[1]+"%02d"%tup[2])((lambda t: tuple(['+' if t<0 else '-', abs(t)/3600, abs(t)/60%60]))(time.altzone if time.daylight else time.timezone))
		utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
		result = iq.buildReply('result')
		reply=result.addChild('time', {}, [], 'urn:xmpp:time')
		reply.setTagData('tzo', tzo)
		reply.setTagData('utc', utc)
		JCON.send(result)
		raise xmpp.NodeProcessed
	elif iq.getTags('query', {}, xmpp.NS_DISCO_INFO):
		items=[]
		ids=[]
		ids.append({'category':'client','type':'bot','name':'Talisman'})
		features=[xmpp.NS_DISCO_INFO,xmpp.NS_DISCO_ITEMS,xmpp.NS_MUC,'urn:xmpp:time','urn:xmpp:ping',xmpp.NS_VERSION,xmpp.NS_PRIVACY,xmpp.NS_ROSTER,xmpp.NS_VCARD,xmpp.NS_DATA,xmpp.NS_LAST,xmpp.NS_COMMANDS,'msglog','fullunicode',xmpp.NS_TIME]
		info={'ids':ids,'features':features}
		b=xmpp.browser.Browser()
		b.PlugIn(JCON)
		b.setDiscoHandler({'items':items,'info':info})
	elif iq.getTags('query', {}, xmpp.NS_LAST):
		last=time.time()-LAST['t']
		result = iq.buildReply('result')
		query = result.getTag('query')
		query.setAttr('seconds',int(last))
		query.setData(LAST['c'])
		JCON.send(result)
		raise xmpp.NodeProcessed
	elif iq.getTags('query', {}, xmpp.NS_TIME):
		timedisp=time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.localtime())
		timetz=time.strftime("%Z", time.localtime())
		timeutc=time.strftime('%Y%m%dT%H:%M:%S', time.gmtime())
		result = iq.buildReply('result')
		result.setTagData('utc', timeutc)
		result.setTagData('tz', timetz)
		result.setTagData('display', timedisp)
		JCON.send(result)
		raise xmpp.NodeProcessed
	elif iq.getTags('query', {}, 'urn:xmpp:ping'):
		JCON.send(iq.buildReply('result'))
		raise xmpp.NodeProcessed
	else:
		call_iq_handlers(iq)

def dcHnd():
	print 'DISCONNECTED'
	if AUTO_RESTART:
		print 'WAITING FOR RESTART...'
		time.sleep(10)
		print 'RESTARTING'
		os.execl(sys.executable, sys.executable, sys.argv[0])
	else:
		sys.exit(0)

################################################################################

def start():
	print '\n...---===STARTING BOT===---...\n'
	global JCON
	JCON = xmpp.Client(server=SERVER, port=PORT, debug=[])

	get_access_levels()
	load_plugins()

	print 'Waiting For Connection...\n'

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

	print '\nWaiting For Authentication...'

	auth=JCON.auth(USERNAME, PASSWORD, RESOURCE)
	if not auth:
		print 'Auth Error. Incorrect login/password?\nError: ', JCON.lastErr, JCON.lastErrCode
		sys.exit(1)
	else:
		print 'Logged In'
	if auth!='sasl':
		print 'Warning: unable to perform SASL auth. Old authentication method used!'

	JCON.RegisterHandler('message', messageHnd)
	JCON.RegisterHandler('presence', presenceHnd)
	JCON.RegisterHandler('iq', iqHnd)
	JCON.RegisterDisconnectHandler(dcHnd)
	JCON.UnregisterDisconnectHandler(JCON.DisconnectHandler)
	print 'Handlers Registered'
	JCON.getRoster()
	JCON.sendInitPresence()
	print 'Entering Rooms'

	if check_file(file='chatrooms.list'):
		groupchats = eval(read_file(GROUPCHAT_CACHE_FILE))
		for groupchat in groupchats:
			thread.start_new_thread(join_groupchat, (groupchat,groupchats[groupchat]['nick'],groupchats[groupchat]['passw']))
			MACROS.init(groupchat)
			get_gch_cfg(groupchat)
			get_commoff(groupchat)
			get_greetz(groupchat)
			get_order_pl_cfg(groupchat)
			get_sendpl_cache(groupchat)
	else:
		print 'Error: unable to create chatrooms list file!'

#	load_plugins()
	

	print '\nOk, i\'m ready to work :)\n'
	
	globals()['BOOT'] = time.time()
	
	while 1:
		JCON.Process(10)

if __name__ == "__main__":
	try:
		start()
	except KeyboardInterrupt:
		print '\nINTERUPT (Ctrl+C)'
		prs=xmpp.Presence(typ='unavailable')
		prs.setStatus(u'got Ctrl-C -> shutdown')
		JCON.send(prs)
		time.sleep(2)
		print 'DISCONNECTED'
		print '\n...---===BOT STOPPED===---...\n'
		sys.exit(0)
	except:
		if AUTO_RESTART:
#			if sys.exc_info()[0] is not SystemExit:
			traceback.print_exc()
			try:
				JCON.disconnected()
			except IOError:
				pass
			try:
				time.sleep(5)
			except KeyboardInterrupt:
				print '\nINTERUPT (Ctrl+C)'
				prs=xmpp.Presence(typ='unavailable')
				prs.setStatus(u'got Ctrl-C -> shutdown')
				JCON.send(prs)
				time.sleep(2)
				print 'DISCONNECTED'
				print '\n...---===BOT STOPPED===---...\n'
				sys.exit(0)
				print 'WAITING FOR RESTART...'
			print 'RESTARTING'
			os.execl(sys.executable, sys.executable, sys.argv[0])
		else:
			raise
