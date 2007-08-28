#===istalismanplugin===
# -*- coding: utf-8 -*-
####### It is translated by Als #######

CURRENT_POLL = {}

def handler_vote_vote(type, source, parameters):
	global CURRENT_POLL
	if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(source[2]):
		if CURRENT_POLL.has_key(source[1]):
			if isadmin(GROUPCHATS[source[1]][source[2]]['jid']) or not GROUPCHATS[source[1]][source[2]]['jid'] in CURRENT_POLL[source[1]]['jids']:
				if CURRENT_POLL[source[1]]['options'].has_key(parameters.strip().lower()):
					CURRENT_POLL[source[1]]['options'][parameters.strip().lower()] += 1
					CURRENT_POLL[source[1]]['jids'].append(GROUPCHATS[source[1]][source[2]]['jid'])
					reply(type, source, u'понял')
				else:
					reply(type, source, u'мнения не свои, а предопределённые)')
			else:
				reply(type, source, u'ты уже голосовал')
		else:
			reply(type, source, u'щас нету никаких голосований')
	else:
		reply(type, source, u'а в чат ответить не дано?')

def handler_vote_newpoll(type, source, parameters):
	global CURRENT_POLL
	if CURRENT_POLL.has_key(source[1]):
		poll_text = u'НОВОЕ ГОЛОСОВАНИЕ\nСоздатель: '+ source[2]+u'\nВопрос: '+CURRENT_POLL[source[1]]['question'] + u'\nВарианты ответов:\n'
		for option in CURRENT_POLL[source[1]]['options'].keys():
			poll_text += '   >>> ' + option + '\n'
		poll_text += u'Чтобы проголовать, напиши : мнение <твоё_мнение>'
		msg(source[1], poll_text)
	else:
		if parameters:
			CURRENT_POLL = {source[1]: {'creator': source[2], 'options': {}, 'question': parameters, 'jids': []}}
			reply(type, source, u'создал голование. чтобы добавить пункты напиши "пункт <пункт>"')
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
		CURRENT_POLL = {}
	else:
		reply(type, source, u'упс... нет голования')

register_command_handler(handler_vote_vote, 'мнение', ['голосование','мук','все'], 10, 'Для подачи мнения в текущем голосовании.', 'мнение <мнение>', ['мнение да'])
register_command_handler(handler_vote_newpoll, 'голосование', ['голосование','мук','все'], 20, 'Создаёт новое голосование или отправляет готовое голосование в текущий чат, если даны мнения.', 'голосование [вопрос]', ['голосование винды - сакс!', 'голосование'])
register_command_handler(handler_vote_polloption, 'пункт', ['голосование','мук','все'], 20, 'Добавляет пункт (1!) к текущему голосованию.', 'пункт <твой_пункт>', ['пункт да'])
register_command_handler(handler_vote_endpoll, 'итоги', ['голосование','мук','админ','все'], 20, 'Завершает голование и показывает его резалты.', 'итоги', ['итоги'])
