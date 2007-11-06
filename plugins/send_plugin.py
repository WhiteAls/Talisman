#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  send_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

sendqueue={}
def handler_psay(ltype, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		args = parameters.split(' ')
		date=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
		fromnick=source[2]+u' из '+source[1]+u' в '+date+u' (UTC) попросил меня передать тебе следующее:\n\n'
		if len(args)>=2:
			nick = args[0]
			body = ' '.join(args[1:])
			if nick == 'botadmin':
				reply(ltype, source, u'передам')
				msg(ADMINS[0], fromnick+body)
				return
			if get_bot_nick(groupchat) != nick:
				tojid = groupchat+'/'+nick
				if nick in nicks and GROUPCHATS[groupchat][nick]['ishere']==1:
					reply(ltype, source, u'он тут сидит')
				else:
					if not sendqueue.has_key(tojid):
						sendqueue[tojid] = []
					sendqueue[tojid].append(fromnick+body)
					reply(ltype, source, u'передам')

def handler_new_join(groupchat, nick, aff, role):
	tojid = groupchat+'/'+nick
	if sendqueue.has_key(tojid) and sendqueue[tojid]:
		for x in sendqueue[tojid]:
			time.sleep(1)
			msg(tojid, x)
			sendqueue[tojid].remove(x)

register_join_handler(handler_new_join)
register_command_handler(handler_psay, 'передать', ['мук','все'], 10, 'Запоминает сообщение в базе и передаёт его указанному нику как только он зайдёт в конференцию.', 'передать <кому> <что>', ['передать Nick привет! забань Nick666'])
