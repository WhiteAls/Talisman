#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  vote_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

CURRENT_POLL = {}

def handler_vote_vote(type, source, parameters):
	global CURRENT_POLL
	jid=get_true_jid(source)
	if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(source[2]):
		if CURRENT_POLL.has_key(source[1]):
			if not jid in CURRENT_POLL[source[1]]['jids']:
				CURRENT_POLL[source[1]]['jids'][jid]=jid
				CURRENT_POLL[source[1]]['jids'][jid]={}
				CURRENT_POLL[source[1]]['jids'][jid]['isnotified']=1
				CURRENT_POLL[source[1]]['jids'][jid]['isvoted']=0
			if isadmin(jid) or CURRENT_POLL[source[1]]['jids'][jid]['isvoted']==0:
				if CURRENT_POLL[source[1]]['options'].has_key(parameters.strip().lower()):
					CURRENT_POLL[source[1]]['options'][parameters.strip().lower()] += 1
					CURRENT_POLL[source[1]]['jids'][jid]['isvoted']=1
					
					reply(type, source, u'понял')
				else:
					reply(type, source, u'мнения не свои, а предопределённые)')
			else:
				reply(type, source, u'ты уже голосовал')
		else:
			reply(type, source, u'сейчас нету никаких голосований')
	else:
		reply(type, source, u'мнения принимаются только в общем чате')

def handler_vote_newpoll(type, source, parameters):
	global CURRENT_POLL
	if CURRENT_POLL.has_key(source[1]):
		poll_text = u'НОВОЕ ГОЛОСОВАНИЕ\nСоздатель: '+ CURRENT_POLL[source[1]]['creator']+u'\nВопрос: '+CURRENT_POLL[source[1]]['question'] + u'\nВарианты ответов:\n'
		for option in CURRENT_POLL[source[1]]['options'].keys():
			poll_text += '   >>> ' + option + '\n'
		poll_text += u'Чтобы проголосовать, напиши "мнение твоё_мнение"'
		msg(source[1], poll_text)
	else:
		if parameters:
			CURRENT_POLL = {source[1]: {'creator': source[2], 'options': {}, 'question': parameters, 'jids':{}}}
			reply(type, source, u'создал голосование. чтобы добавить пункты напиши "пункт твой_пункт"')
		else:
			reply(type,source,u'не вижу вопроса голосования')

def handler_vote_polloption(type, source, parameters):
	global CURRENT_POLL
	if CURRENT_POLL.has_key(source[1]):
		CURRENT_POLL[source[1]]['options'][parameters.strip().lower()] = 0
		reply(type, source, u'добавил')
	else:
		reply(type, source, u'упс... нет голосования')

def handler_vote_endpoll(type, source, parameters):
	global CURRENT_POLL
	if CURRENT_POLL.has_key(source[1]):
		poll_text = u'РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ\nСоздатель: '+ CURRENT_POLL[source[1]]['creator']+u'\nВопрос: '+CURRENT_POLL[source[1]]['question'] + u'\nИтоги:\n'
		num = 1
		for option in CURRENT_POLL[source[1]]['options'].keys():
			poll_text += str(CURRENT_POLL[source[1]]['options'][option]) + ' - ' + option + '\n'
			num += 1
		msg(source[1], poll_text)
		del CURRENT_POLL[source[1]]
	else:
		reply(type, source, u'упс... нет голосования')
		
def handler_vote_join(groupchat, nick, aff, role):
	jid=get_true_jid(groupchat+'/'+nick)
	if CURRENT_POLL.has_key(groupchat):
		if not jid in CURRENT_POLL[groupchat]['jids'].keys():
			CURRENT_POLL[groupchat]['jids'][jid]=jid
			CURRENT_POLL[groupchat]['jids'][jid]={}
			CURRENT_POLL[groupchat]['jids'][jid]['isnotified']=1
			CURRENT_POLL[groupchat]['jids'][jid]['isvoted']=0
			poll_text = u'ТЕКУЩЕЕ ГОЛОСОВАНИЕ\nСоздатель: '+ CURRENT_POLL[groupchat]['creator']+u'\nВопрос: '+CURRENT_POLL[groupchat]['question'] + u'\nВарианты ответов:\n'
			for option in CURRENT_POLL[groupchat]['options'].keys():
				poll_text += '   >>> ' + option + '\n'
			poll_text += u'Чтобы проголосовать, напиши в общий чат "мнение твоё_мнение"'
			msg(groupchat+'/'+nick, poll_text)

register_command_handler(handler_vote_vote, 'мнение', ['голосование','мук','все'], 10, 'Для подачи мнения в текущем голосовании.', 'мнение <мнение>', ['мнение да'])
register_command_handler(handler_vote_newpoll, 'голосование', ['голосование','мук','все'], 20, 'Создаёт новое голосование или отправляет готовое голосование в текущий чат, если даны мнения.', 'голосование [вопрос]', ['голосование винды - сакс!', 'голосование'])
register_command_handler(handler_vote_polloption, 'пункт', ['голосование','мук','все'], 20, 'Добавляет пункт (1!) к текущему голосованию.', 'пункт <твой_пункт>', ['пункт да'])
register_command_handler(handler_vote_endpoll, 'итоги', ['голосование','мук','админ','все'], 20, 'Завершает голование и показывает его резалты.', 'итоги', ['итоги'])
register_join_handler(handler_vote_join)
