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
	total = '0'
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		for x in nicks:
			total = int(total) + 1
		reply(type, source, 'я здесь вижу '+str(total)+' юзеров')
	else:
		reply(type, source, u'аблом какой-то...')
		
		
def handler_bot_uptime(type, source, parameters):
	if BOOT:
		idletime = int(time.time() - BOOT)
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


register_command_handler(handler_getrealjid, 'тружид', ['инфо','админ','мук','все'], 20, 'Показывает реальный жид указанного ника. Работает только если бот модер ессно', 'тружид <ник>', ['тружид guy'])
register_command_handler(handler_total_in_muc, 'инмук', ['инфо','мук','все'], 10, 'Показывает количество юзеров находящихся в конференции.', 'инмук', ['инмук'])
register_command_handler(handler_bot_uptime, 'ботап', ['инфо','админ','все'], 10, 'Показывает сколько времени бот работает без падений.', 'ботап', ['ботап'])
