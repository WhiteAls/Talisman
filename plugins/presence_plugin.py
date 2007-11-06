#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  presence_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_presence_subscr(prs):
	type = prs.getType()
	who = prs.getFrom()
	if not type:
		type = 'available'
	if type == 'subscribe':
		JCON.send(xmpp.protocol.Presence(to=who, typ='subscribed'))
	elif type == 'unsubscribe':
		JCON.send(xmpp.protocol.Presence(to=who, typ='unsubscribed'))
	else:
		pass
"""
	elif type == 'subscribed':
		pass
	elif type == 'unsubscribed':
		pass
	elif type == 'available':
		pass
	elif type == 'unavailable':
		pass
"""
"""
def handler_presence_moder_check(prs):
	time.sleep(1)
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	botnick = get_bot_nick(groupchat)
	item = findPresenceItem(prs)
	if nick == botnick:
		DBPATH='dynamic/'+groupchat+'/config.cfg'
		if check_file(groupchat,'config.cfg'):
			gchconfdb = eval(read_file(DBPATH))
			if gchconfdb.has_key('ismoder'):
				if gchconfdb['ismoder'] == 1:
					if item['role'] == 'moderator':
						return
					else:
						gchconfdb['ismoder'] = 0
						msg(groupchat, u'я не смогу работать корректно здесь, потому что я не имею прав модератора. это связано с системой прав к командам. поэтому чтобы не казатся глюком, я отключаю все команды и жду прав модера.')	
						if not COMMOFF.has_key(groupchat):
							COMMOFF[groupchat]=groupchat
						COMMOFF[groupchat]=[]
						COMMOFF[groupchat].append('*****')
				else:
					if item['role'] != 'moderator':
						if not COMMOFF.has_key(groupchat):
							COMMOFF[groupchat]=groupchat
						COMMOFF[groupchat]=[]
						COMMOFF[groupchat].append('*****')
					else:
						gchconfdb['ismoder'] = 1
						try:
							ind=COMMOFF[groupchat].index('*****')
							COMMOFF[groupchat].remove[ind]
						except:
							pass
						msg(groupchat, u'реджойнюсь...')
						leave_groupchat(groupchat)
						time.sleep(0.2)
						join_groupchat(groupchat)						
			else:
				if item['role'] != 'moderator':
					gchconfdb['ismoder'] = 0
					msg(groupchat, u'я не смогу работать корректно здесь, потому что я не имею прав модератора. это связано с системой прав к командам. поэтому чтобы не казатся глюком, я отключаю все команды и жду прав модера.')
					if not COMMOFF.has_key(groupchat):
						COMMOFF[groupchat]=groupchat
					COMMOFF[groupchat]=[]
					COMMOFF[groupchat].append('*****')
				else:
					gchconfdb['ismoder'] = 1
					try:
						ind=COMMOFF[groupchat].index('*****')
						COMMOFF[groupchat].remove[ind]
					except:
						pass
					msg(groupchat, u'реджойнюсь...')
					leave_groupchat(groupchat)
					time.sleep(0.2)
					join_groupchat(groupchat)		

def handler_presence_ra_change(prs):
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	jid = get_true_jid(groupchat+'/'+nick)
	item = findPresenceItem(prs)
	try:
		if GLOBACCESS.has_key(jid):
			return
	except:
		ACCFILE = eval(read_file(ACCBYCONF_FILE))
		if ACCFILE[groupchat].has_key(jid):
			pass
	else:
		if GROUPCHATS[groupchat].has_key(nick):
			if jid != None:
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
"""				
def handler_presence_ra_change(prs):
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	jid = get_true_jid(groupchat+'/'+nick)
	item = findPresenceItem(prs)
	if jid in GLOBACCESS:
		return
	else:
		if groupchat in ACCBYCONFFILE and jid in ACCBYCONFFILE[groupchat]:
			pass
		else:
			if groupchat in GROUPCHATS and nick in GROUPCHATS[groupchat]:
				if jid != None:
					role = item['role']
					aff = item['affiliation']
					if role in ROLES:
						accr = ROLES[role]
						if role=='moderator':
							GROUPCHATS[groupchat][nick]['ismoder'] = 1
						else:
							GROUPCHATS[groupchat][nick]['ismoder'] = 0
					else:
						accr = 0
					if aff in AFFILIATIONS:
						acca = AFFILIATIONS[aff]
					else:
						acca = 0
					access = accr+acca
					change_access_temp(groupchat, jid, access)

def handler_presence_nickcommand(prs):
	groupchat = prs.getFrom().getStripped()
	if groupchat in GROUPCHATS:
		code = prs.getStatusCode()
		if code == '303':
			nick = prs.getNick()
		else:
			nick = prs.getFrom().getResource()
		nicksource=nick.split()[0].strip()
		if nicksource in (COMMANDS.keys() + MACROS.gmacrolist.keys() + MACROS.macrolist[groupchat].keys()):
			iq = xmpp.Iq('set')
			iq.setTo(groupchat)
			iq.setID('kick'+str(random.randrange(1000, 9999)))
			query = xmpp.Node('query')
			query.setNamespace('http://jabber.org/protocol/muc#admin')
			reason=query.addChild('item', {'nick':nick, 'role':'none'})
			reason.setTagData('reason', u'not allowed')
			iq.addChild(node=query)
			JCON.send(iq)
			return

	
register_presence_handler(handler_presence_subscr)
register_presence_handler(handler_presence_ra_change)
register_presence_handler(handler_presence_nickcommand)

#  listed below command handler are not recommended. it's not working at now.
#  register_presence_handler(handler_presence_moder_check)
