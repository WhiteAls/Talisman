#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  commoff_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

stick_nicks={}

def handler_stick(type, source, parameters):
	groupchat = source[1]
	if parameters:
		if parameters==u'last10':
			cnt=0
			rep=''
			nicks = set()
			for x in [stick_nicks[source[1]] for x in stick_nicks]:
				nicks = nicks | set(x)
			for x in nicks:
				cnt=cnt+1
				rep += str(cnt)+u') '+x+u'\n'
			reply('private',source,rep[:-1])
			return
		if not stick_nicks.has_key(source[1]):
			stick_nicks[source[1]]=source[1]
			stick_nicks[source[1]]=[]
		if len(stick_nicks[source[1]])==10:
			stick_nicks[source[1]]=[]
		else:
			stick_nicks[source[1]].append(source[2])
		args = parameters.split(' ')
		if not args[0] == u'себя' or not args[0] == get_bot_nick(source[1]):
			if len(args)<=1:
				nick = args[0]
				replies = [u'/me облил ' +nick+ u' ледяной водой',u'/me закидал ' +nick+ u' тухлыми помидорами',u'/me шарахнул ' +nick+ u' веслом по голове',u'/me ткнул ' +nick+ u' в глаз',u'/me поставил ' +nick+ u' подножку',u'/me постукал ' +nick+ u' головой апстенку',u'/me дал ' +nick+ u' йаду',u'/me slaps ' +nick+ u' around a bit with a large trout',u'приковал наручниками к кровати '+nick+u' и заставлил слушать Децла. МНОГО ДЕЦЛА!',u'/me шарахнул '+nick+u' веслом по голове',u'/me щас засунет '+nick+u' кляп в рот ]:->',u'/me целится плюсомётом в '+nick,u'/me тыкает '+nick+u' со словами "нуу, пратииивный"',u'/me кинул нож в сторону '+nick]
				rep = random.choice(replies)
				msg(source[1],rep)
			elif len(args)>=2:
				nick = args[0]
				body = ' '.join(args[1:])
				msg(source[1],  u'/me ткнул '+nick+u' '+body)
		else:
			reply(type, source, u'шибко умный, да? ]:->')	
	else:
		reply(type, source, u'мазохист? :D')

		
def handler_test(type, source, parameters):
	reply(type,source,u'пассед')
	
def handler_clean_conf(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
		for x in range(1, 20):
			msg(source[1], x)
			time.sleep(1.3)

			
def handler_kick_ass(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
		if parameters:
			rep = ''
			splitdata = string.split(parameters)
			if splitdata[0]==u':)':
				for x in range(0, int(splitdata[1])):
					for y in range(0, int(splitdata[2])):
						rep += u':) '
					msg(source[1], rep)
					rep = ''
					time.sleep(0.5)
			else:
				for x in range(0, int(splitdata[1])):
					for y in range(0, int(splitdata[2])):
						rep += u':) '
					msg(source[1]+'/'+splitdata[0], rep)
					rep = ''
					time.sleep(0.5)
	
register_command_handler(handler_stick, 'тык', ['фан','все'], 10, 'Ткнуть кого-то в глаз или во что-то.', 'тык <ник> <куда>', ['тык qwerty','тык qwerty в живот'])
register_command_handler(handler_test, 'тест', ['фан','инфо','все'], 0, 'Тупо отвечает пассед.', 'тест', ['тест'])
register_command_handler(handler_test, 'test', ['фан','инфо','все'], 0, 'Тупо отвечает пассед.', 'test', ['test'])
register_command_handler(handler_clean_conf, 'фконфу', ['фан','мук','все'], 15, 'Очищает конференцию (считает до 20).', 'фконфу', ['фконфу'])

#  listed below command handler are not recommended
#  register_command_handler(handler_kick_ass, 'засрать', ['фан','суперадмин','мук','все'], 100, 'Засирает конфожид указанным количеством мессаг со смайликом, кол-во  которых определяется третьим параметром.. Если первый параметр смайлик ( :) ), то засирает кол-вом мессаг из второго параметра, засовывая в каждую мессагу кол-во смайлов из третьего параметра.', 'засрать [ник] [кол-во] [кол-во]', ['засрать Als 100 200','засрать :) 50 200'])
