#===istalismanplugin===
# -*- coding: utf-8 -*-
####### by Als #######


def handler_getrealjid(type, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		nick = parameters.strip()
		if not nick in nicks:
			reply(type,source,u'ты уверен, что <'+nick+u'> сейчас тут?')
			return
		else:
			jidsource=groupchat+'/'+nick
			if get_true_jid(jidsource) == 'None':
				reply(type, source, u'я ж не модер')
				return
			truejid=get_true_jid(jidsource)
			if type == 'public':
				reply(type, source, u'ушёл')
		reply('private', source, u'реальный жид <'+nick+u'> --> '+truejid)
		
		
def handler_total_in_muc(type, source, parameters):
	groupchat=source[1]
	total = '0'
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		for x in nicks:
			total = int(total) + 1
		reply(type, source, 'я здесь вижу '+str(total)+' юзеров')
	else:
		reply(type, source, u'аблом какой-то...')
		
		
def handler_bot_uptime(type, source, parameters):
	if BOOTUP_TIMESTAMP:
		idletime = int(time.time() - BOOTUP_TIMESTAMP)
		rep = 'я работаю без падений уже '
		seconds = idletime % 60
		minutes = (idletime / 60) % 60
		hours = (idletime / 3600) % 60
		days = idletime / 216000
		if days: rep += str(days) + ' дн '
		if hours: rep += str(hours) + ' час '
		if minutes: rep += str(minutes) + ' мин '
		rep += str(seconds) + ' сек'
	else:
		rep = 'аблом...'
	reply(type, source, rep)


register_command_handler(handler_getrealjid, {1: 'тружид', 2: 'truejid', 3: '!truejid'}, ['инфо','админ','мук','все'], 20, 'Показывает реальный жид указанного ника. Работает только если бот модер ессно', 'truejid <ник>', ['truejid guy'])
register_command_handler(handler_total_in_muc, {1: 'тотал', 2: 'inmuc', 3: '!total'}, ['инфо','мук','все'], 10, 'Показывает количество юзеров находящихся в конференции.', 'inmuc', ['inmuc'])
register_command_handler(handler_bot_uptime, {1: 'ботап', 2: 'botup', 3: '!botup'}, ['инфо','админ','все'], 20, 'Показывает сколько времени бот работает без падений.', 'botup', ['inmuc'])
