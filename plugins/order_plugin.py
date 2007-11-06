#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  auto_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  First Version and Idea © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

order_stats = {}
order_obscene_words = [u'бляд', u'блят', u'хуй', u'хуе', u'хуя', u'нах', u'хули', u'пизд', u'еба', u'еби', u'ебл', u'пидо', u'педр', u'педе', u'пида', u'оху', u'ёб', u'манд', u'муда', u'муди', u'гандон', u'гондон', u'дроч', u'ебл', u'уеб', u'уёб']

def check_order_obscene_words(body):
	sbody = body.split()
	for x in sbody:
		x=x.strip()
		for y in order_obscene_words:
			if x.count(y)>=1:
				return True
	return False

def order_kick(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	kick=query.addChild('item', {'nick':nick, 'role':'none'})
	kick.setTagData('reason', reason)
	iq.addChild(node=query)
	JCON.send(iq)
	return
	
def order_visitor(groupchat, nick):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	visitor=query.addChild('item', {'nick':nick, 'role':'visitor'})
	iq.addChild(node=query)
	JCON.send(iq)
	return
	
def order_ban(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'nick':nick, 'affiliation':'outcast'})
	ban.setTagData('reason', reason)
	iq.addChild(node=query)
	JCON.send(iq)
	return

def handler_order_message(ltype, source, body):
	nick=source[2]
	groupchat=source[1]
	if groupchat in GROUPCHATS and nick in GROUPCHATS[groupchat] and 'ismoder' in GROUPCHATS[groupchat][nick] and GROUPCHATS[groupchat][nick]['ismoder'] == 0:
		if get_bot_nick(groupchat)!=nick and nick!='':
			jid=get_true_jid(groupchat+'/'+nick)
			if groupchat in order_stats.keys() and jid in order_stats[groupchat]:
				lastmsg=order_stats[groupchat][jid]['msgtime']
				now = time.time()
				if body != '':
					sourcebody=body
					body = body.lower().replace(' ', '').strip()
					if body.count(':') > 7 or body.count(')') > 7 or body.count('(') > 7 or body.count('*') > 7:
						order_stats[groupchat][jid]['flood']+=1
						order_kick(groupchat, nick, 'smile flood')
					elif now-lastmsg<=2.2:
						order_stats[groupchat][jid]['msg']+=1
						if order_stats[groupchat][jid]['msg']>2:
							order_stats[groupchat][jid]['flood']+=1
							order_stats[groupchat][jid]['msg']=0
							order_kick(groupchat, nick, 'you send messages is too fast')
					elif len(body)>=600:
						order_stats[groupchat][jid]['flood']+=1
						order_kick(groupchat, nick, 'flood')
#					elif check_order_obscene_words(sourcebody):
#						order_stats[groupchat][jid]['obscene']+=1
#						order_kick(groupchat, nick, 'obscene lexicon')
				order_stats[groupchat][jid]['msgtime']=time.time()
						
def handler_order_join(groupchat, nick, aff, role):
	if groupchat in GROUPCHATS and nick in GROUPCHATS[groupchat] and 'ismoder' in GROUPCHATS[groupchat][nick] and GROUPCHATS[groupchat][nick]['ismoder'] == 0:
		jid=get_true_jid(groupchat+'/'+nick)
		if not groupchat in order_stats.keys():
			order_stats[groupchat] = {}
		if jid in order_stats[groupchat].keys():
#			if order_stats[groupchat][jid]['kicked']>2:
#				order_ban(groupchat, nick, 'too many kicks')
			if order_stats[groupchat][jid]['obscene']>=1:
				order_visitor(groupchat, nick)
			elif order_stats[groupchat][jid]['flood']!=0:
				if order_stats[groupchat][jid]['flood']==1:
					order_visitor(groupchat, nick)
#				elif order_stats[groupchat][jid]['flood']>1:
#					order_ban(groupchat, nick, 'flood excess')
		else:
			order_stats[groupchat][jid]=jid
			order_stats[groupchat][jid]={}
			order_stats[groupchat][jid]['obscene']=0
			order_stats[groupchat][jid]['flood']=0
			order_stats[groupchat][jid]['kicked']=0
			order_stats[groupchat][jid]['msgtime']=0
			order_stats[groupchat][jid]['prstime']=0
			order_stats[groupchat][jid]['prs']=0
			order_stats[groupchat][jid]['msg']=0
	
def handler_order_presence(prs):
	ptype = prs.getType()
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	jid=get_true_jid(groupchat+'/'+nick)
	if groupchat in GROUPCHATS and jid!=groupchat:
		if ptype=='available' or ptype==None:
			now = time.time()
			lastprs=order_stats[groupchat][jid]['prstime']
			if now-lastprs<=10:
				order_stats[groupchat][jid]['prs']+=1
				if order_stats[groupchat][jid]['prs']>4:
					order_stats[groupchat][jid]['flood']+=1
					order_stats[groupchat][jid]['prs']=0
					order_kick(groupchat, nick, 'presence flood')	
#			if check_order_obscene_words(GROUPCHATS[groupchat][nick]['stmsg']):
#				order_stats[groupchat][jid]['obscene']+=1
#				order_kick(groupchat, nick, 'obscene lexicon in status msg')			
		elif ptype=='unavailable':
			code = prs.getStatusCode()
			if code:
				print jid, code
				if groupchat in order_stats.keys():
					if jid in order_stats[groupchat].keys():
						if code == '307': # kick
							order_stats[groupchat][jid]['kicked']+=1
						elif code == '301': # ban
							del order_stats[groupchat][jid]			
		order_stats[groupchat][jid]['prstime']=time.time()

######################################################################################################################


register_message_handler(handler_order_message)
register_join_handler(handler_order_join)
register_presence_handler(handler_order_presence)
