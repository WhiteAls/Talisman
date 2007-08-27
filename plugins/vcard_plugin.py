#===istalismanplugin===
# -*- coding: utf-8 -*-
####### by Als #######

vcard_pending=[]

def handler_vcardget(type, source, parameters):
	vcard_iq = xmpp.Iq('get')
	id='vcard'+str(random.randrange(1000, 9999))
	globals()['vcard_pending'].append(id)
	vcard_iq.setID(id)
	vcard_iq.addChild('vCard', {}, [], 'vcard-temp');
	if parameters:
		if GROUPCHATS.has_key(source[1]):
			nicks = GROUPCHATS[source[1]].keys()
			nick = parameters.strip()
			if nick in nicks:
				jid=source[1]+'/'+nick
				vcard_iq.setTo(jid)
			else:
				reply(type, source, u'а он тут? :-O')
				return
	else:
		jid=source[1]+'/'+source[2]
		vcard_iq.setTo(jid)
		nick=''
	JCON.SendAndCallForResponse(vcard_iq, handler_vcardget_answ, {'type': type, 'source': source, 'nick': nick})
		

def handler_vcardget_answ(coze, res, type, source, nick):
	id=res.getID()
	if id in globals()['vcard_pending']:
		globals()['vcard_pending'].remove(id)
	else:
		print 'ooops!'
		return
	rep =''
	if res:
		if res.getType()=='error':
				reply(type, source, u'хехе, его клиент не дружит с этим')
				return
		elif res.getType() == 'result':
			nickname = ''
			url = ''
			email = ''
			desc = ''
			if res.getChildren():
				props = res.getChildren()[0].getChildren()
			else:
				if not nick:
					reply(type,source,u'вкард заполни сначала')
					return
				else:
					reply(type,source,u'передай ему, чтобы он свой вкард сначала заполнил')
					return
				return
			for p in props:
				if p.getName() == 'NICKNAME':
					nickname = p.getData()
				elif p.getName() == 'URL':
					url = p.getData()
				elif p.getName() == 'EMAIL':
					email = p.getData()
				elif p.getName() == 'DESC':
					desc = p.getData()
			if nickname:
				if not nick:
					rep = u'про тебя я знаю следующее:\nnick: '+nickname
				else:
					rep = u'про <'+nick+u'> я знаю следующее:\nnick: '+nickname
			if not url=='':
				rep +='\nurl: '+url
			if not email=='':
				rep +=u'\nemail: '+email		
			if not desc=='':
				rep +=u'\nabout: '+desc
			if rep=='':
				rep = u'пустой вкард'
		else:
			rep = u'он зашифровался'
	else:
		rep = u'что-то никак...'
	reply(type, source, rep)



register_command_handler(handler_vcardget, {1: 'визитка', 2: 'profile', 3: '!vcard'}, ['мук','инфо','все'], 10, 'Показывает vCard указанного пользователя.', 'profile [ник]', ['profile guy','profile'])
