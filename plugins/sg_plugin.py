#===istalismanplugin===
# -*- coding: utf-8 -*-
####### It is translated by Als #######

def handler_SG_get(type, source, parameters):
		groupchat = source[1]
		iq = xmpp.Iq('get')
		iq.setQueryNS('http://jabber.org/protocol/stats')
		if parameters!='':
			iq.setTo(parameters.strip())
		else:
			iq.setTo(SERVER)
			parameters=SERVER
		JCON.SendAndCallForResponse(iq,first_handler_SG,{'parameters':parameters,'type':type,'source':source})

def first_handler_SG(coze,res,parameters,type,source):
	#print par
	payload=res.getQueryPayload()
	if res.getType()=='error':
		reply(type,source,u'аблом '+res.getErrorCode()+ ': '+res.getError())
		pass
	elif res.getType()=='result':
		iq = xmpp.Iq('get')
		iq.setQueryNS('http://jabber.org/protocol/stats')
		iq.setQueryPayload(payload)
		iq.setTo(parameters.strip())
		JCON.SendAndCallForResponse(iq,second_handler_SG,{'parameters':parameters,'type':type,'source':source})

def second_handler_SG(coze,stats,parameters,type,source):
	pay=stats.getQueryPayload()
	if stats.getType()=='result':
		result=u'Инфа о ' + parameters + ':\n'
		for stat in pay:
			result=result+stat.getAttrs()['name']+': '+stat.getAttrs()['value'] + ' '+stat.getAttrs()['units'] + '\n'
			
		reply(type,source,result)
		
		
register_command_handler(handler_SG_get, {1: 'инфа', 2: 'statz', 3: '!stats'}, ['инфо','все'], 10, 'Возвращает статистику о сервере юзая XEP-0039.', 'statz <сервер>', ['statz jabber.aq'])
