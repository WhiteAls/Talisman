#===istalismanplugin===
# -*- coding: utf-8 -*-
####### It is translated by Als #######

ping_pending=[]
def handler_ping(type, source, parameters):
	nick=parameters
	groupchat=source[1]
	jid=groupchat+'/'+nick
	iq = xmpp.Iq('get')
	id = 'vers'+str(random.randrange(1000, 9999))
	globals()['ping_pending'].append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:version');
	if parameters:
		if GROUPCHATS.has_key(source[1]):
			nicks = GROUPCHATS[source[1]].keys()
			param = parameters.strip()
			if not nick in nicks:
				iq.setTo(param)
			else:
				iq.setTo(jid)
	else:
		jid=groupchat+'/'+source[2]
		iq.setTo(jid)
		param=''
	t0 = time.time()
	JCON.SendAndCallForResponse(iq, handler_ping_answ,{'t0': t0, 'mtype': type, 'source': source, 'param': param})
	return

def handler_ping_answ(coze, res, t0, mtype, source, param):
	id = res.getID()
	if id in globals()['ping_pending']:
		globals()['ping_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	if res:
		if res.getType() == 'result':
			t = time.time()
			rep = u'понг от '
			if param:
				rep += param
			else:
				rep += u'тебя'
			rep+=u' '+str(round(t-t0, 3))+u' секунд'
		else:
			rep = u'не пингуется'
	else:
		rep = u'не дождался :('
	reply(mtype, source, rep)
	
register_command_handler(handler_ping, {1: 'пинг', 2: 'ring', 3: '!p'}, ['инфо','мук','все'], 0, 'Пинг тебя или определённый ник (не сервер!).', 'ring [ник]', ['ring guy','ring jabber.aq'])