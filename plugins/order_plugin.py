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

import re

order_stats = {}
order_obscene_words = [u'бляд', u' блят', u' бля ', u' блять ', u' плять ', u' хуй', u' ибал', u' ебал', u'нахуй', u' хуй', u' хуи', u'хуител', u' хуя', u'хуя', u' хую', u' хуе', u' ахуе', u' охуе', u'хуев', u' хер ', u' хер', u'хер', u' пох ', u' нах ', u'писд', u'пизд', u'рizd', u' пздц ', u' еб', u' епана ', u' епать ', u' ипать ', u' выепать ', u' ибаш', u' уеб', u'проеб', u'праеб', u'приеб', u'съеб', u'сьеб', u'взъеб', u'взьеб', u'въеб', u'вьеб', u'выебан', u'перееб', u'недоеб', u'долбоеб', u'долбаеб', u' ниибац', u' неебац', u' неебат', u' ниибат', u' пидар', u' рidаr', u' пидар', u' пидор', u'педор', u'пидор', u'пидарас', u'пидараз', u' педар', u'педри', u'пидри', u' заеп', u' заип', u' заеб', u'ебучий', u'ебучка ', u'епучий', u'епучка ', u' заиба', u'заебан', u'заебис', u' выеб', u'выебан', u' поеб', u' наеб', u' наеб', u'сьеб', u'взьеб', u'вьеб', u' гандон', u' гондон', u'пахуи', u'похуис', u' манда ', u'мандав', u' залупа', u' залупог']

#resmile = re.compile('\*[A-Z_! ]+\*') 

def check_order_obscene_words(body):
	body=body.strip().lower()
	body=u' '+body+u' '
	for x in order_obscene_words:
		if body.count(x):
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

def handler_order_message(type, source, body):
	nick=source[2]
	groupchat=source[1]
	if nick in GROUPCHATS[groupchat] and user_level(source,groupchat)<11:
		if get_bot_nick(groupchat)!=nick and nick!='':
			jid=get_true_jid(groupchat+'/'+nick)
			if groupchat in order_stats and jid in order_stats[groupchat]:
				lastmsg=order_stats[groupchat][jid]['msgtime']
				now = time.time()
				if body != '':
					order_stats[groupchat][jid]['msgtime']=time.time()
					sourcebody=body
					body = body.lower().replace(' ', '').strip()
					if GCHCFGS[groupchat]['filt']['smile']==1:
#						sml=re.findall(resmile, sourcebody)
#						print sml
						if body.count('-)') > 7 or body.count('-(') > 7:
#							order_stats[groupchat][jid]['flood']+=1
							order_stats[groupchat][jid]['devoice']['time']=now
							order_stats[groupchat][jid]['devoice']['cnd']=1
							order_kick(groupchat, nick, 'смайл-флуд')
							return
					if GCHCFGS[groupchat]['filt']['time']==1:
						if now-lastmsg<=2.2:
							order_stats[groupchat][jid]['msg']+=1
							if order_stats[groupchat][jid]['msg']>2:
#								order_stats[groupchat][jid]['flood']+=1
								order_stats[groupchat][jid]['devoice']['time']=now
								order_stats[groupchat][jid]['devoice']['cnd']=1
								order_stats[groupchat][jid]['msg']=0
								order_kick(groupchat, nick, 'слишком быстро отправляешь')
								return
					if GCHCFGS[groupchat]['filt']['len']==1:
						if len(sourcebody)>900:
#							order_stats[groupchat][jid]['flood']+=1
							order_stats[groupchat][jid]['devoice']['time']=now
							order_stats[groupchat][jid]['devoice']['cnd']=1
							order_kick(groupchat, nick, 'флуд')
							return
					if GCHCFGS[groupchat]['filt']['obscene']==1:
						if check_order_obscene_words(sourcebody):
#							order_stats[groupchat][jid]['obscene']+=1
							order_stats[groupchat][jid]['devoice']['time']=now
							order_stats[groupchat][jid]['devoice']['cnd']=1
							order_kick(groupchat, nick, 'маты фтопку')
							return
					if GCHCFGS[groupchat]['filt']['caps']==1:
						ccnt=0
						nicks = GROUPCHATS[groupchat].keys()
						sbody=sourcebody
						for x in nicks:
							if sbody.count(x):
								sbody=sbody.replace(x,'')
#						if sourcebody.strip().split()[0].replace(':', '').replace(',', '').replace('>', '') in nicks:
#							sourcebody=' '.join(sourcebody.split()[1:]).strip()
						for x in [x for x in sbody.replace(' ', '').strip()]:
							if x.isupper():
								ccnt+=1
						if ccnt>=len(sbody)/2 and ccnt>9:
#							order_stats[groupchat][jid]['flood']+=1
							order_stats[groupchat][jid]['devoice']['time']=now
							order_stats[groupchat][jid]['devoice']['cnd']=1
							order_kick(groupchat, nick, 'слишком много капса')
							return
					if GCHCFGS[groupchat]['filt']['like']==1:
						lcnt=0
						if order_stats[groupchat][jid]['msgbody'] is not None:
							if now-lastmsg>60:
								order_stats[groupchat][jid]['msgbody']=sourcebody.strip().split()
							else:
								for x in order_stats[groupchat][jid]['msgbody']:
									for y in sourcebody.strip().split():
										if x==y:
											lcnt+=1
								if lcnt:
									lensrcmsgbody=len(sourcebody.strip().split())
									lenoldmsgbody=len(order_stats[groupchat][jid]['msgbody'])
									avg=(lensrcmsgbody+lenoldmsgbody/2)/2
									if lcnt>avg:
										order_stats[groupchat][jid]['msg']+=1
										if order_stats[groupchat][jid]['msg']>=2:
#											order_stats[groupchat][jid]['flood']+=1
											order_stats[groupchat][jid]['devoice']['time']=now
											order_stats[groupchat][jid]['devoice']['cnd']=1
											order_stats[groupchat][jid]['msg']=0
											order_kick(groupchat, nick, 'мессаги слишком похожи')
											return
								order_stats[groupchat][jid]['msgbody']=sourcebody.strip().split()
						else:
							order_stats[groupchat][jid]['msgbody']=sourcebody.strip().split()
						
def handler_order_join(groupchat, nick, aff, role):
	jid=get_true_jid(groupchat+'/'+nick)
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		now = time.time()
		if not groupchat in order_stats.keys():
			order_stats[groupchat] = {}
		if jid in order_stats[groupchat].keys():
			if order_stats[groupchat][jid]['devoice']['cnd']==1:
				if now-order_stats[groupchat][jid]['devoice']['time']>300:
					order_stats[groupchat][jid]['devoice']['cnd']=0
				else:
					order_visitor(groupchat, nick)
#			if order_stats[groupchat][jid]['obscene']>=1:
#				order_visitor(groupchat, nick)
#			if order_stats[groupchat][jid]['flood']!=0:
#				if order_stats[groupchat][jid]['flood']<3:
#					order_visitor(groupchat, nick)
#				elif order_stats[groupchat][jid]['flood']>3:
#					order_stats[groupchat][jid]['flood']=0
#					order_ban(groupchat, nick, 'слишком много флуда')
			if GCHCFGS[groupchat]['filt']['kicks']['cond']==1:
				kcnt=GCHCFGS[groupchat]['filt']['kicks']['cnt']
				if order_stats[groupchat][jid]['kicks']>kcnt:
					order_ban(groupchat, nick, 'слишком много киков')			
		elif nick in GROUPCHATS[groupchat]:
			order_stats[groupchat][jid]={}
			order_stats[groupchat][jid]['kicks']=0
#			order_stats[groupchat][jid]['obscene']=0
#			order_stats[groupchat][jid]['flood']=0
			order_stats[groupchat][jid]['devoice']={}
			order_stats[groupchat][jid]['devoice']['cnd']=0
			order_stats[groupchat][jid]['devoice']['time']=0
			order_stats[groupchat][jid]['msgbody']=None
			order_stats[groupchat][jid]['msgtime']=0
			order_stats[groupchat][jid]['prstime']={}
			order_stats[groupchat][jid]['prstime']['fly']=0
			order_stats[groupchat][jid]['prstime']['status']=0			
			order_stats[groupchat][jid]['prs']={}
			order_stats[groupchat][jid]['prs']['fly']=0
			order_stats[groupchat][jid]['prs']['status']=0
			order_stats[groupchat][jid]['msg']=0
			
		if GCHCFGS[groupchat]['filt']['fly']['cond']==1:
			lastprs=order_stats[groupchat][jid]['prstime']['fly']
			order_stats[groupchat][jid]['prstime']['fly']=time.time()	
			if now-lastprs<=70:
				order_stats[groupchat][jid]['prs']['fly']+=1
				if order_stats[groupchat][jid]['prs']['fly']>4:
					order_stats[groupchat][jid]['prs']['fly']=0
					fmode=GCHCFGS[groupchat]['filt']['fly']['mode']
					ftime=GCHCFGS[groupchat]['filt']['fly']['time']
					if mode=='ban':
						order_ban(groupchat, nick, 'хватит летать')
						time.sleep(ftime)
						order_unban(groupchat, jid)
					else:
						order_kick(groupchat, nick, 'хватит летать')
			else:
				order_stats[groupchat][jid]['prs']['fly']=0

def handler_order_presence(prs):
	ptype = prs.getType()
	if ptype=='unavailable' or ptype=='error':
		return
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	stmsg = prs.getStatus()
	jid=get_true_jid(groupchat+'/'+nick)
	item=findPresenceItem(prs)

	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		now = time.time()
		if now-GROUPCHATS[groupchat][nick]['joined']>1:
			if item['role']=='participant':
				order_stats[groupchat][jid]['devoice']['cnd']=0
			lastprs=order_stats[groupchat][jid]['prstime']['status']
			order_stats[groupchat][jid]['prstime']['status']=time.time()
			if GCHCFGS[groupchat]['filt']['presence']==1:
				if now-lastprs>300:
					order_stats[groupchat][jid]['prs']['status']=0
				else:
					order_stats[groupchat][jid]['prs']['status']+=1
					if order_stats[groupchat][jid]['prs']['status']>5:
						order_stats[groupchat][jid]['prs']['status']=0
						order_kick(groupchat, nick, 'презенс-флуд')
						return
			if GCHCFGS[groupchat]['filt']['prsstlen']==1 and stmsg:
				if len(stmsg)>=200:
					order_stats[groupchat][jid]['flood']+=1
					order_kick(groupchat, nick, 'статусная мессага слишком большая')						
				order_stats[groupchat][jid]['prstime']['status']=time.time()
				
	elif groupchat in order_stats and jid in order_stats[groupchat]:
		if item['affiliation']=='member':
			del order_stats[groupchat][jid]
			return
	else:
		pass		

#		elif ptype=='unavailable':
#			try:
#				lastprs=order_stats[groupchat][jid]['prstime']['fly']
#				if now-lastprs<=70:
#					if now-lastprs>=300:
#						order_stats[groupchat][jid]['prs']['fly']=0
#					else:
#						order_stats[groupchat][jid]['prs']['fly']+=1
#						if order_stats[groupchat][jid]['prs']['fly']>5:
#							order_stats[groupchat][jid]['prs']['fly']=0
#							order_kick(groupchat, nick, 'flying flood')
#				order_stats[groupchat][jid]['prstime']['fly']=time.time()
#			except:
#				pass
			
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

def handler_order_leave(groupchat, nick, reason, code):
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		jid=get_true_jid(groupchat+'/'+nick)
		if GCHCFGS[groupchat]['filt']['presence']==1:
			if reason=='Replaced by new connection':
				return
			if code:
				if code=='307': # kick
					order_stats[groupchat][jid]['kicks']+=1
					return
				elif code=='301': # ban
					del order_stats[groupchat][jid]
					return
				elif code=='407': # members-only
					return
		if GCHCFGS[groupchat]['filt']['fly']==1:
			now = time.time()
			lastprs=order_stats[groupchat][jid]['prstime']['fly']
			order_stats[groupchat][jid]['prstime']['fly']=time.time()
			if now-lastprs<=70:
				order_stats[groupchat][jid]['prs']['fly']+=1
			else:
				order_stats[groupchat][jid]['prs']['fly']=0


######################################################################################################################

def handler_order_filt(type, source, parameters):
	if parameters:
		parameters=parameters.split()
		if GCHCFGS[source[1]].has_key('filt'):
			if parameters[0]=='smile':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация смайлов отключена')
					GCHCFGS[source[1]]['filt']['smile']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация смайлов включена')
					GCHCFGS[source[1]]['filt']['smile']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='time':
				if parameters[1]=='0':
					reply(type,source,u'временная фильтрация сообщений отключена')
					GCHCFGS[source[1]]['filt']['time']=0
				elif parameters[1]=='1':
					reply(type,source,u'временная фильтрация сообщений включена')
					GCHCFGS[source[1]]['filt']['time']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='presence':
				if parameters[1]=='0':
					reply(type,source,u'временная фильтрация презенсов отключена')
					GCHCFGS[source[1]]['filt']['presence']=0
				elif parameters[1]=='1':
					reply(type,source,u'временная фильтрация презенсов включена')
					GCHCFGS[source[1]]['filt']['presence']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='len':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация длинных сообщений отключена')
					GCHCFGS[source[1]]['filt']['len']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация длинных сообщений включена')
					GCHCFGS[source[1]]['filt']['len']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='like':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация подозрительно одинаковых сообщений отключена')
					GCHCFGS[source[1]]['filt']['like']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация подозрительно одинаковых сообщений включена')
					GCHCFGS[source[1]]['filt']['like']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='caps':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация капса отключена')
					GCHCFGS[source[1]]['filt']['caps']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация капса включена')
					GCHCFGS[source[1]]['filt']['caps']=1
				else:
					reply(type,source,u'синтакс инвалид')	
			elif parameters[0]=='prsstlen':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация длинных статусных сообщений отключена')
					GCHCFGS[source[1]]['filt']['prsstlen']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация длинных статусных сообщений включена')
					GCHCFGS[source[1]]['filt']['prsstlen']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='obscene':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация мата отключена')
					GCHCFGS[source[1]]['filt']['obscene']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация мата включена')
					GCHCFGS[source[1]]['filt']['obscene']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='fly':
				if parameters[1]=='cnt':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'синтакс инвалид')
					if int(parameters[2]) in xrange(0,121):
						reply(type,source,u'разморозка установлена на '+parameters[2]+u' секунд')
						GCHCFGS[source[1]]['filt']['fly']['time']=int(parameters[2])	
					else:
						reply(type,source,u'не более двух минут (120 секунд)')
				elif parameters[1]=='mode':
					if parameters[2] in ['kick','ban']:
						if parameters[2] == 'ban':
							reply(type,source,u'за полёты будем банить')
							GCHCFGS[source[1]]['filt']['fly']['mode']='ban'
						else:
							reply(type,source,u'за полёты будем кикать')
							GCHCFGS[source[1]]['filt']['fly']['mode']='kick'	
					else:
						reply(type,source,u'синтакс инвалид')		
				elif parameters[1]=='0':
					reply(type,source,u'фильтр полётов отключен')
					GCHCFGS[source[1]]['filt']['fly']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтр полётов включен')
					GCHCFGS[source[1]]['filt']['fly']['cond']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='kicks':
				if parameters[1]=='cnt':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'синтакс инвалид')
					if int(parameters[2]) in xrange(2,10):
						reply(type,source,u'автобан после '+parameters[2]+u' киков')
						GCHCFGS[source[1]]['filt']['kicks']['cnt']=int(parameters[2])	
					else:
						reply(type,source,u'от 2 до 10 киков')
				elif parameters[1]=='0':
					reply(type,source,u'фильтр автобана после нескольких киков отключен')
					GCHCFGS[source[1]]['filt']['kicks']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтр автобана после нескольких киков включен')
					GCHCFGS[source[1]]['filt']['kicks']['cond']=1
				else:
					reply(type,source,u'синтакс инвалид')
			else:
				reply(type,source,u'синтакс инвалид')
				return					
			DBPATH='dynamic/'+source[1]+'/config.cfg'
			write_file(DBPATH, str(GCHCFGS[source[1]]))
		else:
			reply(type,source,u'случилось что-то странное, ткните админа бота')
	else:
		rep,foff,fon=u'',[],[]
		smile=GCHCFGS[source[1]]['filt']['smile']
		time=GCHCFGS[source[1]]['filt']['time']
		prs=GCHCFGS[source[1]]['filt']['presence']
		len=GCHCFGS[source[1]]['filt']['len']
		like=GCHCFGS[source[1]]['filt']['like']
		caps=GCHCFGS[source[1]]['filt']['caps']
		prsstlen=GCHCFGS[source[1]]['filt']['prsstlen']
		obscene=GCHCFGS[source[1]]['filt']['obscene']
		fly=GCHCFGS[source[1]]['filt']['fly']['cond']
		flytime=str(GCHCFGS[source[1]]['filt']['fly']['time'])
		flymode=GCHCFGS[source[1]]['filt']['fly']['mode']
		kicks=GCHCFGS[source[1]]['filt']['kicks']['cond']
		kickscnt=str(GCHCFGS[source[1]]['filt']['kicks']['cnt'])
		if smile:
			fon.append(u'фильтрация смайлов')
		else:
			foff.append(u'фильтрация смайлов')
		if time:
			fon.append(u'временная фильтрация сообщений')
		else:
			foff.append(u'временная фильтрация сообщений')
		if prs:
			fon.append(u'временная фильтрация презенсов')
		else:
			foff.append(u'временная фильтрация презенсов')
		if len:
			fon.append(u'фильтрация длинных сообщений')
		else:
			foff.append(u'фильтрация длинных сообщений')
		if like:
			fon.append(u'фильтрация подозрительно одинаковых сообщений')
		else:
			foff.append(u'фильтрация подозрительно одинаковых сообщений')
		if caps:
			fon.append(u'фильтрация капса')
		else:
			foff.append(u'фильтрация капса')
		if prsstlen:
			fon.append(u'фильтрация длинных статусных сообщений')
		else:
			foff.append(u'фильтрация длинных статусных сообщений')
		if obscene:
			fon.append(u'фильтрация мата')
		else:
			foff.append(u'фильтрация мата')
		if fly:
			fon.append(u'фильтр полётов (режим '+flymode+u', таймер '+flytime+u' секунд)')
		else:
			foff.append(u'фильтр полётов')
		if kicks:
			fon.append(u'автобан после '+kickscnt+u' киков')
		else:
			foff.append(u'автобан после нескольких киков')
		fon=u', '.join(fon)
		foff=u', '.join(foff)
		if fon:
			rep+=u'ВКЛЮЧЕНЫ\n'+fon+u'\n\n'
		if foff:
			rep+=u'ВЫКЛЮЧЕНЫ\n'+foff
		reply(type,source,rep.strip())


register_message_handler(handler_order_message)
register_join_handler(handler_order_join)
register_leave_handler(handler_order_leave)
register_presence_handler(handler_order_presence)
register_command_handler(handler_order_filt, 'filt', ['админ','мук','все'], 20, 'Включает или отключает определённые фильтры для конференции.\nsmile - фильтр смайлов\ntime - временной фильтр\nlen - количественный фильтр\npresence - фильтр презенсов\nlike - фильтр одинаковых сообщений\ncaps - фильтр капса (ЗАГЛАВНЫХ букв)\nprsstlen - фильтр длинных статусных сообщений\nobscene - фильтр матов\nfly - фильтр полётов (частых входов/выходов в конмату), имеет два режима ban и kick, таймер от 0 до 120 секунд\nkicks - автобан после N киков, параметр cnt - количество киков от 1 до 10', 'filt [фильтр] [режим] [состояние]', ['filt smile 1', 'filt len 0','filt fly mode ban'])
