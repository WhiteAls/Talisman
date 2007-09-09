#===istalismanplugin===
# -*- coding: utf-8 -*-
####### modified by Als on 50% :). original by dimichxp #######

version_pending=[]
def handler_version(type, source, parameters):
	nick = source[2]
	groupchat=source[1]
	jid=groupchat+'/'+nick
	iq = xmpp.Iq('get')
	id='vers'+str(random.randrange(1000, 9999))
	globals()['version_pending'].append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:version');
	if parameters:
		args = parameters.split(' ')
		nick = ' '.join(args[0:])
		jid=groupchat+'/'+nick
		if GROUPCHATS.has_key(source[1]):
			nicks = GROUPCHATS[source[1]].keys()
			param = parameters.strip()
			if not nick in nicks:
				iq.setTo(param)
			else:
				iq.setTo(jid)
	else:
		jid=groupchat+'/'+nick
		iq.setTo(jid)
	JCON.SendAndCallForResponse(iq, handler_version_answ, {'type': type, 'source': source})
	return

def handler_version_answ(coze, res, type, source):
	id=res.getID()
	if id in globals()['version_pending']:
		globals()['version_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	rep =''
	if res:
		if res.getType() == 'result':
			name = '[no name]'
			version = '[no ver]'
			os = '[no os]'
			props = res.getQueryChildren()
			for p in props:
				if p.getName() == 'name':
					name = p.getData()
				elif p.getName() == 'version':
					version = p.getData()
				elif p.getName() == 'os':
					os = p.getData()
			if name:
				rep = name
			if version:
				rep +=' '+version
			if os:
				rep +=u' в '+os
		else:
			rep = u'он зашифровался'
	else:
		rep = u'нету такого'
	reply(type, source, rep)
	
register_command_handler(handler_version, 'версия', ['инфо','мук','все'], 0, 'Показывает информацию о клиенте, который юзает юзер или сервер.', 'версия [ник\сервер]', ['версия','версия Nick','версия jabber.aq'])
