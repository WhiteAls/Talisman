#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  disco_plugin.py

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

from re import match

disco_pending=[]
	
def handler_disco(type, source, parameters):
	if parameters==u'ограничения':
		reply('private',source,u'В паблик может дать max 30 результатов, без указания кол-ва - 10.\n В приват может дать max 150, без указания кол-ва 50.')
		return
	iq = xmpp.Iq('get')
	id='dis'+str(random.randrange(1000, 9999))
	globals()['disco_pending'].append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'http://jabber.org/protocol/disco#items')
	if parameters:
		parst=string.split(parameters, ' ', 1)
		if len(parst)==2:
			stop=parst[1]
			if type == 'public':
				if int(stop)>30:
					stop='30'
			else:
				if int(stop)>150:
					stop='150'
			iq.setTo(parst[0])
		else:
			if type == 'public':
				stop='10'
			if type == 'private':
				stop='50'
			iq.setTo(parameters)
	else:
		reply(type,source,u'и чё?')
		return
	JCON.SendAndCallForResponse(iq, handler_disco_ext, {'type': type, 'source': source, 'stop': stop, 'parameters': parameters})

def handler_disco_ext(coze, res, type, source, stop, parameters):
	test1=string.split(parameters, ' ', 1)
	test2=string.split(test1[0], '@', 1)
	if len(test2)==2:
		trig=0
	else:
		trig=1
	disco=[]
	rep=''
	id=res.getID()
	if id in globals()['disco_pending']:
		globals()['disco_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		reply(type, source, u'глюк')
		return
	if res:
		if res.getType() == 'result':
			props=res.getQueryChildren()
			for x in props:
				att=x.getAttrs()
				if trig:
					if att.has_key('name'):
						st=re.match('(.*) \(([0-9]+)\)$', att['name'])
						if st:
							st=st.groups()
							disco.append([st[0],att['jid'],int(st[1])])
							trig=1
					else:
						disco.append(att['jid'])
						trig=2
				else:
					if att.has_key('name'):
						disco.append(att['name'])
						trig=0
			handler_disco_answ(type,source,trig,stop,disco)
			return
		else:
			rep = u'не могу'
	else:
		rep = u'аблом...'
	reply(type, source, rep)
	
	
def handler_disco_answ(type,source,trig,stop,disco):
	total=0
	rep = u'надискаверил:\n'
	if trig==1:
		disco.sort(lambda x,y: x[2] - y[2])
		disco.reverse()
		for x in disco:
			total=total+1
			rep += str(total)+u') '+x[0]+u' ['+x[1]+u']: '+str(x[2])+u'\n'
			if str(total)==stop:
				break
	if trig==0 or trig==2:
		disco.sort()
		for x in disco:
			total=total+1
			rep += str(total)+u') '+x+u'\n'
			if str(total)==stop:
				break
	reply(type, source, rep[:-1])
	disco=[]
			
register_command_handler(handler_disco, 'диско', ['мук','инфо','все'], 10, 'Показывает результату discovery для указанного жида. Об ограничениях - "диско ограничния".', 'диско <сервер> <кол-во результатов>', ['диско jabber.aq','диско conference.jabber.aq 5'])