#===istalismanplugin===
# -*- coding: utf-8 -*-
####### all by Als #######

import string

time_pending=[]		
	
def handler_gettime_xep_disco(type, source, parameters):
	if parameters.strip():
		jid=source[1]+'/'+parameters.strip().strip()
		if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(parameters.strip()):
			if GROUPCHATS[source[1]][parameters.strip()].has_key('timexep'):
				if GROUPCHATS[source[1]][parameters.strip()]['timexep']:
					gettime_xep0202(type,source,jid,parameters.strip())
					return
				else:
					gettime_xep0090(type,source,jid,parameters.strip())
					return
		else:
			reply(type,source, u'а он тут? :-O')
			return
	else:
		jid=source[1]+'/'+source[2]
		if GROUPCHATS[source[1]][source[2]].has_key('timexep'):
			if GROUPCHATS[source[1]][source[2]]['timexep']:
				gettime_xep0202(type,source,jid,source[2])
				return
			else:
				gettime_xep0090(type,source,jid,source[2])
				return
	iq = xmpp.Iq('get')
	iq.setTo(jid)
	id='info'+str(random.randrange(1000, 9999))
	globals()['time_pending'].append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'http://jabber.org/protocol/disco#info')
	JCON.SendAndCallForResponse(iq, handler_gettime_xep_disco_answ, {'type': type, 'source': source, 'parameters': parameters.strip(), 'jid':jid})

		
def handler_gettime_xep_disco_answ(coze, res, type, source, parameters, jid):
	id=res.getID()
	if id in globals()['time_pending']:
		globals()['time_pending'].remove(id)
	else:
		print 'oooops...'
		return
	rep =''
	if res:
		if not res.getType() == 'result':
			reply(type,source,u'диско не идёт')
			return			
		res=res.getQueryChildren()
		for x in res:
			att=x.getAttrs()
			if att.has_key('var'):
				att=att['var']
				if att == 'urn:xmpp:time':
					if parameters.strip():
						GROUPCHATS[source[1]][parameters.strip()]['timexep'] = 1	
					else:
						GROUPCHATS[source[1]][source[2]]['timexep'] = 1	
					gettime_xep0202(type,source,jid,parameters.strip())
					return
		if parameters.strip():
			if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(parameters.strip()):
				GROUPCHATS[source[1]][parameters.strip()]['timexep'] = 0
			else:
				reply(type,source, u'а он тут? :-O')
				return
		else:
			if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(source[2]):
				GROUPCHATS[source[1]][source[2]]['timexep'] = 0
			else:
				reply(type,source, u'а он тут? :-O')
				return
		gettime_xep0090(type,source,jid,parameters.strip())
	else:
		reply(type,source,u'таймаут')
		return


def gettime_xep0090(type,source,jid,param=''):
	nick=''
	if param:
		nick=param
	time_iq = xmpp.Iq('get')
	id='time'+str(random.randrange(1000, 9999))
	globals()['time_pending'].append(id)
	time_iq.setID(id)
	time_iq.addChild('query', {}, [], 'jabber:iq:time');
	time_iq.setTo(jid)
	JCON.SendAndCallForResponse(time_iq, gettime_xep0090_answ, {'type': type, 'source': source, 'nick':nick})
	
	
def gettime_xep0090_answ(coze, res, nick, type, source):
	id=res.getID()
	if id in globals()['time_pending']:
		globals()['time_pending'].remove(id)
	else:
		print 'oooops...'
		reply(type,source, u'глюк')
	if res:
		if res.getType()=='error':
			if nick:
				reply(type,source, u'хехе, твой клиент не дружит с этим')
			else:
				reply(type,source, u'хехе, его клиент не дружит с этим')
		elif res.getType() == 'result':
			time = ''
			props = res.getQueryChildren()
			for p in props:
				if p.getName() == 'display':
					time = p.getData()
			if time:
				if nick:
					reply(type,source, u'у <'+nick+ u'> сейчас ' +time)
				else:
					reply(type,source, u'у тебя сейчас '+time)
	else:
		reply(type,source, u'что-то никак...')
		
		
def gettime_xep0202(type,source,jid,param=''):
	nick=''
	if param:
		nick=param
	time_iq = xmpp.Iq('get')
	id='time'+str(random.randrange(1000, 9999))
	globals()['time_pending'].append(id)
	time_iq.setID(id)
	time_iq.addChild('time', {}, [], 'urn:xmpp:time');
	time_iq.setTo(jid)
	JCON.SendAndCallForResponse(time_iq, gettime_xep0202_answ, {'type': type, 'source': source, 'nick':nick})
	
	
def gettime_xep0202_answ(coze, res, nick, type, source):
	id=res.getID()
	if id in globals()['time_pending']:
		globals()['time_pending'].remove(id)
	else:
		print 'oooops...'
		reply(type,source, u'глюк')
	if res:
		if res.getType()=='error':
			if nick:
				reply(type,source, u'хехе, твой клиент не дружит с этим')
			else:
				reply(type,source, u'хехе, его клиент не дружит с этим')
		elif res.getType() == 'result':
			tzo = ''
			utc = ''
			props = res.getChildren()
			for p in props:
				tzo = p.getTagData('tzo')
				utc = p.getTagData('utc')
			if tzo and utc:
				if tzo[0]=='-' or tzo[0]=='+':
					tzoh=tzo[1:3]
					if tzoh[0]=='0':
						tzoh=tzoh[1]
					if tzo[3:]!='00':
						tzom=tzo[4:5]
				else:
					tzoh=tzo[0:2]
					if tzoh[0]=='0':
						tzoh=tzoh[1]
					if tzo[2:]!='00':
						tzom=tzo[4:5]
				tzoop=tzo[0]
				data=utc[:10]
				hours=utc[11:13]
				minutes=utc[14:16]
				seconds=utc[17:19]
				if tzoop=='+' or tzoop=='0':
					hours=int(hours)+int(tzoh)	
					if tzom:
						minutes=int(minutes)+int(tzom)
				else:
					hours=int(hours)-int(tzoh)
					if tzom:
						minutes=int(minutes)-int(tzom)
				if hours>=24:
					hours=int(hours)-24
				if minutes>=60:
					minutes=int(minutes)-60
				time=str(hours)+':'+str(minutes)+':'+seconds
				if nick:
					reply(type,source, u'у '+nick+u' сейчас '+time+' ('+data+')')
				else:
					reply(type,source, u'у тебя сейчас '+time+' ('+data+')')
			else:
				reply(type,source, u'твой клиент - глюк, инфы не хватает')
	else:
		reply(type,source, u'что-то никак...')

register_command_handler(handler_gettime_xep_disco, {1: 'часики', 2: 'clock', 3: '!time'}, ['мук','инфо','все'], 10, 'Показывает сколько сейчас времени у указанного ника.', 'clock <ник>', ['clock','clock guy'])
