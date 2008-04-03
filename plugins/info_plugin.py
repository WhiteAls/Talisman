#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  info_plugin.py

#  Initial Copyright © 2007 Als <Als@exploru.net>
#  Parts of code Copyright © Bohdan Turkynewych aka Gh0st <tb0hdan[at]gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_getrealjid(type, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		nick = parameters.strip()
		if not nick in nicks:
			reply(type,source,u'ты уверен, что <'+nick+u'> был тут?')
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
	if GROUPCHATS.has_key(groupchat):
		inmuc=[]
		for x in GROUPCHATS[groupchat].keys():
			if GROUPCHATS[groupchat][x]['ishere']==1:
				inmuc.append(x)
		reply(type, source, u'я здесь вижу '+str(len(inmuc))+u' юзеров\n'+u', '.join(inmuc))
	else:
		reply(type, source, u'аблом какой-то...')
		
		
def handler_bot_uptime(type, source, parameters):
	if INFO['start']:
		idletime = int(time.time() - INFO['start'])
		rep = u'я работаю без падений уже '
		seconds = idletime % 60
		minutes = (idletime / 60) % 60
		hours = (idletime / 3600) % 60
		days = idletime / 216000
		if days: rep += str(days) + u' дн '
		if hours: rep += str(hours) + u' час '
		if minutes: rep += str(minutes) + u' мин '
		rep += str(seconds) + u' сек\n'
		rep += u'я получил уже %s сообщений, обработал %s презенсов и %s iq-запросов, а также выполнил %s команд'%(str(INFO['msg']),str(INFO['prs']),str(INFO['iq']),str(INFO['cmd']))
	else:
		rep = 'аблом...'
	reply(type, source, rep)


register_command_handler(handler_getrealjid, 'тружид', ['инфо','админ','мук','все'], 20, 'Показывает реальный жид указанного ника. Работает только если бот модер ессно', 'тружид <ник>', ['тружид guy'])
register_command_handler(handler_total_in_muc, 'инмук', ['инфо','мук','все'], 10, 'Показывает количество юзеров находящихся в конференции.', 'инмук', ['инмук'])
register_command_handler(handler_bot_uptime, 'ботап', ['инфо','админ','все'], 10, 'Показывает сколько времени бот работает без падений.', 'ботап', ['ботап'])
