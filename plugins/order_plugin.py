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
	
def order_visitor(groupchat, nick):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	visitor=query.addChild('item', {'nick':nick, 'role':'visitor'})
	iq.addChild(node=query)
	JCON.send(iq)
	
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
	
def order_unban(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':'none'})
	iq.addChild(node=query)
	JCON.send(iq)

def handler_order_message(ltype, source, body):
	nick=source[2]
	groupchat=source[1]
	if groupchat in GROUPCHATS and nick in GROUPCHATS[groupchat] and 'ismoder' in GROUPCHATS[groupchat][nick] and GROUPCHATS[groupchat][nick]['ismoder'] == 0:
		if get_bot_nick(groupchat)!=nick and nick!='':
			jid=get_true_jid(groupchat+'/'+nick)
			if groupchat in order_stats.keys() and jid in order_stats[groupchat]:
				lastmsg=order_stats[groupchat][jid]['msgtime']
				now = time.time()
				cnt=0
				if body != '':
					sourcebody=body
					body = body.lower().replace(' ', '').strip()
					if GCHCFGS[groupchat]['filt']['smile']==1 and body.count(')') > 7 or body.count('(') > 7 or body.count('*') > 7 or body.count(':') > 7:
						order_stats[groupchat][jid]['flood']+=1
						order_kick(groupchat, nick, 'smile flood')
					elif GCHCFGS[groupchat]['filt']['time']==1 and now-lastmsg<=2.2:
						order_stats[groupchat][jid]['msg']+=1
						if order_stats[groupchat][jid]['msg']>2:
							order_stats[groupchat][jid]['flood']+=1
							order_stats[groupchat][jid]['msg']=0
							order_kick(groupchat, nick, 'you send messages is too fast')
					elif GCHCFGS[groupchat]['filt']['len']==1 and len(body)>=700:
						order_stats[groupchat][jid]['flood']+=1
						order_kick(groupchat, nick, 'flood')
					elif GCHCFGS[groupchat]['filt']['caps']==1:
						for x in [x for x in sourcebody.replace(' ', '').strip()]:
							if x.isupper():
								cnt+=1
						if cnt>=len(body)/2 and cnt>9:
							order_stats[groupchat][jid]['flood']+=1
							order_kick(groupchat, nick, 'too many caps')
					elif GCHCFGS[groupchat]['filt']['like']==1:
						if order_stats[groupchat][jid]['msgbody'] is not None:
							if now-lastmsg>60:
								order_stats[groupchat][jid]['msgbody']=sourcebody.strip().split()
								return
							for x in order_stats[groupchat][jid]['msgbody']:
								for y in sourcebody.strip().split():
									if x==y:
										cnt+=1
							if cnt:
								lensrcmsgbody=len(sourcebody.strip().split())
								lenoldmsgbody=len(order_stats[groupchat][jid]['msgbody'])
								avg=(lensrcmsgbody+lenoldmsgbody/2)/2
								if cnt>avg:
									order_stats[groupchat][jid]['msg']+=1
									if order_stats[groupchat][jid]['msg']>2:
										order_stats[groupchat][jid]['flood']+=1
										order_stats[groupchat][jid]['msg']=0
										order_kick(groupchat, nick, 'your messages looks like repeat-flood')
							order_stats[groupchat][jid]['msgbody']=sourcebody.strip().split()
						else:
							order_stats[groupchat][jid]['msgbody']=sourcebody.strip().split()
						
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
#			if order_stats[groupchat][jid]['obscene']>=1:
#				order_visitor(groupchat, nick)
			if order_stats[groupchat][jid]['flood']!=0:
				if order_stats[groupchat][jid]['flood']<3:
					order_visitor(groupchat, nick)
				elif order_stats[groupchat][jid]['flood']>3:
					order_stats[groupchat][jid]['flood']=0
					order_ban(groupchat, nick, 'flood excess')
					time.sleep(5)
					order_unban(groupchat, jid)
		else:
			order_stats[groupchat][jid]=jid
			order_stats[groupchat][jid]={}
#			order_stats[groupchat][jid]['obscene']=0
			order_stats[groupchat][jid]['flood']=0
			order_stats[groupchat][jid]['msgbody']=None
			order_stats[groupchat][jid]['msgtime']=0
			order_stats[groupchat][jid]['prstime']={}
			order_stats[groupchat][jid]['prstime']['fly']=0
			order_stats[groupchat][jid]['prstime']['status']=0			
			order_stats[groupchat][jid]['prs']={}
			order_stats[groupchat][jid]['prs']['fly']=0
			order_stats[groupchat][jid]['prs']['status']=0
			order_stats[groupchat][jid]['msg']=0
			
	
def handler_order_presence(prs):
	ptype = prs.getType()
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	jid=get_true_jid(groupchat+'/'+nick)
	item=findPresenceItem(prs)
	if jid!=groupchat and groupchat in GROUPCHATS and nick in GROUPCHATS[groupchat] and 'ismoder' in GROUPCHATS[groupchat][nick] and GROUPCHATS[groupchat][nick]['ismoder'] == 0 and GCHCFGS[groupchat]['filt']['presence']==1:
		now = time.time()
		if ptype==None or ptype=='available':
			try:
				if GROUPCHATS[groupchat][nick]['ishere']==1:
					if item['role']=='participant':
						order_stats[groupchat][jid]['flood']=0
					lastprs=order_stats[groupchat][jid]['prstime']['status']
					if now-lastprs<=10:
						if now-lastprs>=300:
							order_stats[groupchat][jid]['prs']['status']=0
						else:
							order_stats[groupchat][jid]['prs']['status']+=1
							if order_stats[groupchat][jid]['prs']['status']>5:
								order_stats[groupchat][jid]['prs']['status']=0
								order_kick(groupchat, nick, 'presence flood')					
					order_stats[groupchat][jid]['prstime']['status']=time.time()
				else:
					lastprs=order_stats[groupchat][jid]['prstime']['fly']
					if now-lastprs<=70:
						if now-lastprs>=300:
							order_stats[groupchat][jid]['prs']['fly']=0
						else:
							order_stats[groupchat][jid]['prs']['fly']+=1
							if order_stats[groupchat][jid]['prs']['fly']>5:
								order_stats[groupchat][jid]['prs']['fly']=0
								order_kick(groupchat, nick, 'flying flood')
					order_stats[groupchat][jid]['prstime']['fly']=time.time()					
			except:
				pass

		elif ptype=='unavailable':
			try:
				lastprs=order_stats[groupchat][jid]['prstime']['fly']
				if now-lastprs<=70:
					if now-lastprs>=300:
						order_stats[groupchat][jid]['prs']['fly']=0
					else:
						order_stats[groupchat][jid]['prs']['fly']+=1
						if order_stats[groupchat][jid]['prs']['fly']>5:
							order_stats[groupchat][jid]['prs']['fly']=0
							order_kick(groupchat, nick, 'flying flood')
				order_stats[groupchat][jid]['prstime']['fly']=time.time()
			except:
				pass
			
#		if check_order_obscene_words(GROUPCHATS[groupchat][nick]['stmsg']):
#			order_stats[groupchat][jid]['obscene']+=1
#			order_kick(groupchat, nick, 'obscene lexicon in status msg')	
			
#			order_stats[groupchat][jid]['prs']=0
#			code = prs.getStatusCode()
#			if code:
#				if groupchat in order_stats.keys():
#					if jid in order_stats[groupchat].keys():
#						if code == '307': # kick
#							order_stats[groupchat][jid]['kicked']+=1
#						if code == '301': # ban
#							del order_stats[groupchat][jid]


######################################################################################################################

def handler_order_filt(type, source, parameters):
	if parameters:
		param=parameters.strip().split()
		if GCHCFGS[source[1]].has_key('filt'):
			try:
				int(param[1])
			except:
				reply(type,source,u'синтакс инвалид')
				return				
			if param[0]=='smile':
				if param[1]=='0':
					reply(type,source,u'фильтрация смайлов отключена')
					GCHCFGS[source[1]]['filt']['smile']=int(param[1])
				elif param[1]=='1':
					reply(type,source,u'фильтрация смайлов включена')
					GCHCFGS[source[1]]['filt']['smile']=int(param[1])
			elif param[0]=='time':
				if param[1]=='0':
					reply(type,source,u'временная фильтрация сообщений отключена')
					GCHCFGS[source[1]]['filt']['time']=int(param[1])
				elif param[1]=='1':
					reply(type,source,u'временная фильтрация сообщений включена')
					GCHCFGS[source[1]]['filt']['time']=int(param[1])
			elif param[0]=='presence':
				if param[1]=='0':
					reply(type,source,u'временная фильтрация презенсов отключена')
					GCHCFGS[source[1]]['filt']['presence']=int(param[1])
				elif param[1]=='1':
					reply(type,source,u'временная фильтрация презенсов включена')
					GCHCFGS[source[1]]['filt']['presence']=int(param[1])
			elif param[0]=='len':
				if param[1]=='0':
					reply(type,source,u'фильтрация длинных сообщений отключена')
					GCHCFGS[source[1]]['filt']['presence']=int(param[1])
				elif param[1]=='1':
					reply(type,source,u'фильтрация длинных сообщений включена')
					GCHCFGS[source[1]]['filt']['presence']=int(param[1])		
			elif param[0]=='like':
				if param[1]=='0':
					reply(type,source,u'фильтрация подозрительно одинаковых сообщений отключена')
					GCHCFGS[source[1]]['filt']['like']=int(param[1])
				elif param[1]=='1':
					reply(type,source,u'фильтрация подозрительно одинаковых сообщений включена')
					GCHCFGS[source[1]]['filt']['like']=int(param[1])		
			elif param[0]=='caps':
				if param[1]=='0':
					reply(type,source,u'фильтрация капса отключена')
					GCHCFGS[source[1]]['filt']['caps']=int(param[1])
				elif param[1]=='1':
					reply(type,source,u'фильтрация капса включена')
					GCHCFGS[source[1]]['filt']['caps']=int(param[1])					
			else:
				reply(type,source,u'синтакс инвалид')
				return					
			GCHCFGS[source[1]]['filt'][param[0]]=int(param[1])
			DBPATH='dynamic/'+source[1]+'/config.cfg'
			write_file(DBPATH, str(GCHCFGS[source[1]]))
		else:
			GCHCFGS[source[1]]['filt']={}
			GCHCFGS[source[1]]['filt']['smile']=1
			GCHCFGS[source[1]]['filt']['time']=1
			GCHCFGS[source[1]]['filt']['presence']=1
			GCHCFGS[source[1]]['filt']['len']=1
			GCHCFGS[source[1]]['filt']['like']=1
			GCHCFGS[source[1]]['filt']['caps']=1
			DBPATH='dynamic/'+source[1]+'/config.cfg'
			write_file(DBPATH, str(GCHCFGS[source[1]]))
	else:
		if not GCHCFGS[source[1]].has_key('filt'):
			GCHCFGS[source[1]]['filt']={}
			GCHCFGS[source[1]]['filt']['smile']=1
			GCHCFGS[source[1]]['filt']['time']=1
			GCHCFGS[source[1]]['filt']['presence']=1
			GCHCFGS[source[1]]['filt']['len']=1
			GCHCFGS[source[1]]['filt']['like']=1
			GCHCFGS[source[1]]['filt']['caps']=1
			DBPATH='dynamic/'+source[1]+'/config.cfg'
			write_file(DBPATH, str(GCHCFGS[source[1]]))
		rep=u''
		smile=GCHCFGS[source[1]]['filt']['smile']
		time=GCHCFGS[source[1]]['filt']['time']
		prs=GCHCFGS[source[1]]['filt']['presence']
		len=GCHCFGS[source[1]]['filt']['len']
		like=GCHCFGS[source[1]]['filt']['like']
		caps=GCHCFGS[source[1]]['filt']['caps']
		if smile:
			rep += u'фильтрация смайлов включена\n'
		else:
			rep += u'фильтрация смайлов отключена\n'
		if time:
			rep += u'временная фильтрация сообщений включена\n'
		else:
			rep += u'временная фильтрация сообщений отключена\n'
		if prs:
			rep += u'временная фильтрация презенсов включена\n'
		else:
			rep += u'временная фильтрация презенсов отключена\n'
		if len:
			rep += u'фильтрация длинных сообщений включена\n'
		else:
			rep += u'фильтрация длинных сообщений отключена\n'
		if like:
			rep += u'фильтрация подозрительно одинаковых сообщений включена\n'
		else:
			rep += u'фильтрация подозрительно одинаковых сообщений отключена\n'
		if caps:
			rep += u'фильтрация капса включена'
		else:
			rep += u'фильтрация капса отключена'
		reply(type,source,rep.strip())


register_message_handler(handler_order_message)
register_join_handler(handler_order_join)
register_presence_handler(handler_order_presence)
register_command_handler(handler_order_filt, 'filt', ['админ','мук','все'], 20, 'Включает или отключает определённые фильтры для конференции.\nsmile - фильтр смайлов\ntime - временной фильтр\nlen - количественный фильтр\npresence - фильтр презенсов\nlike - фильтр одинаковых сообщений\ncaps - фильтр капса (ЗАГЛАВНЫХ букв)', 'filt [фильтр] [состояние]', ['filt smile 1', 'filt len 0'])
