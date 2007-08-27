#===istalismanplugin===
# -*- coding: utf-8 -*-
####### all by Als #######

def handler_status(type, source, parameters):
	if parameters:
		if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(parameters):
			stmsg=GROUPCHATS[source[1]][parameters]['stmsg']
			status=GROUPCHATS[source[1]][parameters]['status']
			if stmsg:
				reply(type,source, parameters+u' сейчас '+status+u' ('+stmsg+u')')
			else:
				reply(type,source, parameters+u' сейчас '+status)
		else:
			reply(type,source, u'а он тут? :-O')
	else:
		if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(source[2]):
			stmsg=GROUPCHATS[source[1]][source[2]]['stmsg']
			status=GROUPCHATS[source[1]][source[2]]['status']
			if stmsg:
				reply(type,source, u'ты сейчас '+status+u' ('+stmsg+u')')
			else:
				reply(type,source, u'ты сейчас '+status)

def status_change(prs):
	time.sleep(5)
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	stmsg = prs.getStatus()
	if not stmsg:
		stmsg=''
	status = prs.getShow()
	if not status:
		status=u'online'
	try:
		if GROUPCHATS[groupchat].has_key(nick):
			GROUPCHATS[groupchat][nick]['status']=status
		if GROUPCHATS[groupchat].has_key(nick):
			GROUPCHATS[groupchat][nick]['stmsg']=stmsg
	except:
		pass
	

register_presence_handler(status_change)
register_command_handler(handler_status, {1: 'статус', 2: 'sts', 3: '!status'}, ['инфо','мук','все'], 0, 'Показывает статус и статусное сообщение (если есть) определённого юзера или себя.', 'sts <юзер>', ['sts', 'sts guy'])
