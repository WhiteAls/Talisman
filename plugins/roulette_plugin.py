#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  roulette_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_roulette(type, source, parameters):
	groupchat = source[1]
	qwer = source[2]
	admin = groupchat+'/'+qwer
	rep =''
	if not has_access(admin, 20, groupchat):
		if GROUPCHATS.has_key(groupchat):
			nick = source[2]
			if nick:
				random.seed(int(time.time()))
				if random.randrange(0,2) == 0:
					iq = xmpp.Iq('set')
					iq.setTo(source[1])
					iq.setID('kick'+str(random.randrange(1000, 9999)))
					query = xmpp.Node('query')
					query.setNamespace('http://jabber.org/protocol/muc#admin')
					reason=query.addChild('item', {'nick':nick, 'role':'none'})
					reason.setTagData('reason', u'ПТЫДЫЩЬ!!!')
					iq.addChild(node=query)
					JCON.SendAndCallForResponse(iq, handler_roulette_answ, {'type': type, 'source': source})
				else:
					rep = u'ЩЁЛК!'
		else:
			rep = u'что-то вглюкнуло...'
		if rep:
			reply(type, source, rep)
	else:
		reply(type, source, u'не поднимается рука в модера стрелять :(')

def handler_roulette_answ(coze, res, type, source):
	if res:
		if res.getType() == 'result':
			msg(source[1],  u'/me выстрелил в '+source[2])
			return
		else:
			rep = u'не поднимается рука в модера стрелять :('
	else:
		rep = u'аблом какой-то...'
	reply(type, source, rep)	

register_command_handler(handler_roulette, 'рр', ['фан','инфо','все'], 10, 'Старая добрая русская рулетка.', 'рр (русские буквы)', ['рр'])
