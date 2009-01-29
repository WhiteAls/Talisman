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

POLLINGS = {}

try:	POLLINGS=eval(read_file('dynamic/vote.dat'))
except:	pass

def handler_vote_vote(type, source, parameters):
	global POLLINGS
	jid=get_true_jid(source)
	if POLLINGS.has_key(source[1]):
		if not POLLINGS[source[1]]['started']:
			reply(type, source, u'голосование ещё не запущено')
			return
		if type=='public' and POLLINGS[source[1]]['options']['closed']==1:
			reply(type, source, u'голосование закрытое, нужно голосовать у меня в привате')
			return		
		if type=='private' and POLLINGS[source[1]]['options']['closed']==0:
			reply(type, source, u'голосование открытое, нужно голосовать в общем чате')
			return				
		if not jid in POLLINGS[source[1]]['jids']:
			POLLINGS[source[1]]['jids'][jid]=jid
			POLLINGS[source[1]]['jids'][jid]={}
			POLLINGS[source[1]]['jids'][jid]['isnotified']=1
			POLLINGS[source[1]]['jids'][jid]['isvoted']=0
		if isadmin(jid) or POLLINGS[source[1]]['jids'][jid]['isvoted']==0:
			parameters=parameters.strip().lower()
			if POLLINGS[source[1]]['opinions'].has_key(parameters):
				POLLINGS[source[1]]['opinions'][parameters]['cnt'] += 1
				if POLLINGS[source[1]]['options']['nicks']:
					POLLINGS[source[1]]['opinions'][parameters]['nicks'].add(source[2])
				POLLINGS[source[1]]['jids'][jid]['isvoted']=1
				
				reply(type, source, u'понял')
				vote_save(source[1])
			else:
				reply(type, source, u'нет такого пункта')
		else:
			reply(type, source, u'ты уже голосовал')
	else:
		reply(type, source, u'сейчас нет никаких голосований')

def handler_vote_newpoll(type, source, parameters):
	global POLLINGS
	if POLLINGS.has_key(source[1]):
		if not POLLINGS[source[1]]['finished']:
			poll_text = u'ТЕКУЩЕЕ ГОЛОСОВАНИЕ\nСоздатель: '+ POLLINGS[source[1]]['creator']['nick']+u'\nВопрос: '+POLLINGS[source[1]]['question'] + u'\nВарианты ответов:\n'
			for opinion in POLLINGS[source[1]]['opinions'].keys():
				poll_text += '   >>> ' + opinion + '\n'
			poll_text += u'Чтобы проголосовать, напиши "мнение твоё_мнение"'
			msg(source[1], poll_text)
			return
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS.has_key(source[1]):
		del POLLINGS[source[1]]
	if parameters:
		POLLINGS = {source[1]: {'started': False, 'finished': False, 'creator': {'jid': jid, 'nick': source[2]}, 'opinions': {}, 'question': parameters, 'options': {'closed': False, 'nicks': False, 'admedit': False, 'time': {'time': 0, 'start': 0}}, 'tick': None, 'jids':{}}}			
		reply(type, source, u'Голосование создано!\nЧтобы добавить пункты напиши "пункт твой_пункт".\nОпции голосования - команда "vote_opt". Начать голосование - команда "vote_start". Посмотреть текущие результаты - команда "мнения". Окончить голосование - команда "итоги".\nЕсли что-то непонятно, то прочитай хелп по командам из категории "голосование"!')
		vote_save(source[1])
	else:
		reply(type,source,u'не вижу вопроса голосования')
			
def handler_vote_pollstart(type, source, parameters):
	global POLLINGS
	if not POLLINGS.has_key(source[1]):
		reply(type,source,u'сейчас нет никаких голосований')
		return
	if POLLINGS[source[1]]['started']:
		reply(type, source, u'голосование уже запущено')
		return
	if POLLINGS[source[1]]['finished']:
		reply(type, source, u'голосование было завершено')
		return	
	if len(POLLINGS[source[1]]['opinions'].keys())==0:
		reply(type, source, u'голосование не имеет пунктов')
		return			
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS[source[1]]['creator']['jid']==jid or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
		POLLINGS[source[1]]['started']=True
		poll_text = u'НОВОЕ ГОЛОСОВАНИЕ\nСоздатель: '+ POLLINGS[source[1]]['creator']['nick']+u'\nВопрос: '+POLLINGS[source[1]]['question'] + u'\nВарианты ответов:\n'
		for opinion in POLLINGS[source[1]]['opinions'].keys():
			poll_text += '   >>> ' + opinion + '\n'
		poll_text += u'Чтобы проголосовать, напиши "мнение твоё_мнение"'
		msg(source[1], poll_text)
		if POLLINGS[source[1]]['options']['time']['time']:
			if POLLINGS[source[1]]['tick']:
				if POLLINGS[source[1]]['tick'].isAlive():	vote_tick(0,source[1])
			vote_tick(POLLINGS[source[1]]['options']['time']['time'],source[1])
			POLLINGS[source[1]]['options']['time']['start']=time.time()
		vote_save(source[1])
	else:
		reply(type, source, u'ага, щаззз')

def handler_vote_pollopinion(type, source, parameters):
	if not parameters:
		reply(type, source, u'ииии?')
		return		
	global POLLINGS
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['started']:
			reply(type, source, u'неприменимо к запущеному голосованию, сначала останови/пересоздай')
			return		
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'неприменимо к оконченному голосованию')
			return					
		parameters=parameters.lower()
		if POLLINGS[source[1]]['creator']['jid']==jid or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
			for opinion in POLLINGS[source[1]]['opinions'].keys():
				if opinion==parameters:
					del POLLINGS[source[1]]['opinions'][parameters]
					reply(type, source, u'пункт удалён')
					return
			POLLINGS[source[1]]['opinions'][parameters] = parameters
			POLLINGS[source[1]]['opinions'][parameters] = {'cnt': 0, 'nicks': set()}
			reply(type, source, u'добавил')
			vote_save(source[1])
		else:
			reply(type, source, u'ага, щаззз')
	else:
		reply(type, source, u'сейчас нет никаких голосований')
		
def handler_vote_pollopinions(type, source, parameters):
	global POLLINGS
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ'+vote_results(source[1]))
			return
		if jid==POLLINGS[source[1]]['creator']['jid'] or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
			if type=='public':
				reply(type, source, u'ушли в приват')
			reply('private', source, u'ТЕКУЩИЕ РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ'+vote_results(source[1]))
		else:
			reply(type, source, u'жди окончания голосования :-p')
	else:
		reply(type, source, u'сейчас нет никаких голосований')
		
def handler_vote_polloptions(type, source, parameters):
	global POLLINGS
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'неприменимо к оконченному голосованию')
			return	
		closed=POLLINGS[source[1]]['options']['closed']
		nicks=POLLINGS[source[1]]['options']['nicks']
		admedit=POLLINGS[source[1]]['options']['admedit']
		timee=POLLINGS[source[1]]['options']['time']['time']
		timest=POLLINGS[source[1]]['options']['time']['start']
		started=POLLINGS[source[1]]['started']
		if parameters:
			if POLLINGS[source[1]]['creator']['jid']==jid or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
				parameters=parameters.split()
				if len(parameters)!=2:
					reply(type,source,u'синтакс инвалид')
					return
				if parameters[0]=='closed':
					if parameters[1]=='1':
						reply(type,source,u'приватный режим голосования включен')
						POLLINGS[source[1]]['options']['closed']=True
					else:
						reply(type,source,u'приватный режим голосования отключен')
						POLLINGS[source[1]]['options']['closed']=False
				elif parameters[0]=='nicks':
					if parameters[1]=='1':
						reply(type,source,u'запись ников включена')
						POLLINGS[source[1]]['options']['nicks']=True
					else:
						reply(type,source,u'запись ников отключена')
						POLLINGS[source[1]]['options']['nicks']=False
				elif parameters[0]=='admedit':
					if parameters[1]=='1':
						reply(type,source,u'теперь администрация может править голосование')
						POLLINGS[source[1]]['options']['admedit']=True
					else:
						reply(type,source,u'теперь администрация не может править голосование')
						POLLINGS[source[1]]['options']['admedit']=False
				elif parameters[0]=='time':
					if not parameters[1]=='0':
						reply(type,source,u'время голосования %s' % timeElapsed(int(parameters[1])))
						POLLINGS[source[1]]['options']['time']['time']=int(parameters[1])
						POLLINGS[source[1]]['options']['time']['start']=time.time()
						if started:
							vote_tick(int(parameters[1]),source[1])
					else:
						reply(type,source,u'время голосования - до ручного завершения')
						POLLINGS[source[1]]['options']['time']['time']=0
						if started:
							vote_tick(int(parameters[1]),source[1],False)
				else:
					reply(type,source,u'синтакс инвалид')
				vote_save(source[1])
			else:
				reply(type, source, u'ага, щаззз')				
		else:
			rep=u'ПАРАМЕТРЫ ГОЛОСОВАНИЯ:\n'
			if closed:
				rep += u'голосование проводится приватно, '
			else:
				rep += u'голосование проводится открыто, '
			if nicks:
				rep += u'ники отвечающих записываются, '
			else:
				rep += u'ники отвечающих не записываются, '
			if admedit:
				rep += u'администрация конференции имеет право редактировать голосование и просматривать его результаты, '
			else:
				rep += u'администрация конференции не имеет права редактировать голосование и просматривать его результаты, '
			if timee:
				if started:
					rep += u'голосование будет длиться %s, осталось %s' % (timeElapsed(timee), timeElapsed(timee-(time.time()-timest)))
				else:
					rep += u'голосование будет длиться %s' % timeElapsed(timee)
			else:
				rep += u'голосование будет длиться до его ручного завершения'
			reply(type, source, rep)
	else:
		reply(type, source, u'сейчас нет никаких голосований')			

def handler_vote_endpoll(type, source, parameters):
	global POLLINGS
	jid=get_true_jid(source[1]+'/'+source[2])
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['creator']['jid']==jid or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
			POLLINGS[source[1]]['finished']=True
			POLLINGS[source[1]]['started']=False
			msg(source[1], u'РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ'+vote_results(source[1]))
			vote_save(source[1])
		else:
			reply(type, source, u'ага, щаззз')
	else:
		reply(type, source, u'сейчас нет никаких голосований')

def handler_vote_endpoll_tick(gch):
	global POLLINGS
	POLLINGS[gch]['finished']=True
	POLLINGS[gch]['started']=False
	msg(gch, u'РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ'+vote_results(gch))
	vote_save(gch)

def handler_vote_join(groupchat, nick, aff, role):
	global POLLINGS
	jid=get_true_jid(groupchat+'/'+nick)
	if POLLINGS.has_key(groupchat):
		if POLLINGS[groupchat]['finished']:
			return	
		if POLLINGS[groupchat]['started']:
			if not jid in POLLINGS[groupchat]['jids'].keys():
				POLLINGS[groupchat]['jids'][jid]=jid
				POLLINGS[groupchat]['jids'][jid]={}
				POLLINGS[groupchat]['jids'][jid]['isnotified']=1
				POLLINGS[groupchat]['jids'][jid]['isvoted']=0
				poll_text = u'ТЕКУЩЕЕ ГОЛОСОВАНИЕ\nСоздатель: '+ POLLINGS[groupchat]['creator']['nick']+u'\nВопрос: '+POLLINGS[groupchat]['question'] + u'\nВарианты ответов:\n'
				for opinion in POLLINGS[groupchat]['opinions'].keys():
					poll_text += '   >>> ' + opinion + '\n'
				poll_text += u'Чтобы проголосовать, напиши в общий чат "мнение твоё_мнение"'
				msg(groupchat+'/'+nick, poll_text)
				vote_save(groupchat)
			
def handler_vote_stoppoll(type, source, parameters):
	global POLLINGS
	if POLLINGS.has_key(source[1]):
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'неприменимо к оконченному голосованию')
			return	
		jid=get_true_jid(source[1]+'/'+source[2])
		if POLLINGS[source[1]]['creator']['jid']==jid or POLLINGS[source[1]]['options']['admedit']==1 and has_access(jid,20,source[1]):
			started=POLLINGS[source[1]]['started']
			if started:
				POLLINGS[source[1]]['started']=False
				timee=POLLINGS[source[1]]['options']['time']['time']
				timest=POLLINGS[source[1]]['options']['time']['start']
				if POLLINGS[source[1]]['options']['time']['time']:
					vote_tick(0,source[1],False)
					POLLINGS[source[1]]['options']['time']['time']=int(timee-(time.time()-timest))
				reply(type, source, u'голосование приостановлено')
				vote_save(source[1])
			else:
				reply(type, source, u'голосование уже приостановлено')
		else:
			reply(type, source, u'ага, щаззз')
			return
	else:
		reply(type, source, u'сейчас нет никаких голосований')
			
def vote_tick(timee,gch,start=True):
	global POLLINGS
	if start:
		if timee:
			if POLLINGS[gch]['tick']:
				if POLLINGS[gch]['tick'].isAlive():	POLLINGS[gch]['tick'].cancel()
			POLLINGS[gch]['tick']=threading.Timer(timee, handler_vote_endpoll_tick,(gch,))
			POLLINGS[gch]['tick'].start()
		else:
			POLLINGS[gch]['tick'].start()
	else:
		POLLINGS[gch]['tick'].cancel()
	vote_save(gch)
		
def vote_save(gch):
	global POLLINGS
	DBPATH='dynamic/vote.dat'
	if check_file(file='vote.dat'):
		write_file(DBPATH, str(POLLINGS))
	else:
		print 'Error saving vote for',gch
		
def vote_results(gch):
	global POLLINGS
	poll_text = u'\nСоздатель: '+ POLLINGS[gch]['creator']['nick']+u'\nВопрос: '+POLLINGS[gch]['question'] + u'\nИтоги:\n'
	for opinion in POLLINGS[gch]['opinions'].keys():
		if POLLINGS[gch]['options']['nicks']:
			poll_text += opinion+u' - '+str(POLLINGS[gch]['opinions'][opinion]['cnt'])+u' голосов ('+u', '.join(POLLINGS[gch]['opinions'][opinion]['nicks']) + ')\n'
		else:
			poll_text += opinion+u' - '+str(POLLINGS[gch]['opinions'][opinion]['cnt'])+u' голосов\n'
	return poll_text

register_command_handler(handler_vote_polloptions, 'vote_opt', ['голосование','мук','все'], 10, 'Управление опциями голосования. Всего 4 опции:\n1) closed - определяет, будет ли голосование открытым (только в общем чате) или закрытым (только приват)\n2) nicks - определяет, будут ли записывать ники голосующих, для последующей их выдачи вместе с результатами голосования\n3) admedit - определяет, будет ли администрация конференции иметь возможность редактировать голосование\n4) time - для определения времени (в секундах) в течении которого будет длиться голосование. 0 - ручная остановка', 'опции <опция> <состояние>', ['опции nicks 1','опции time 600'])
register_command_handler(handler_vote_stoppoll, 'vote_stop', ['голосование','мук','все'], 11, 'Останавливает голосование, все данные сохраняются до продолжения голосования.', 'опции <опция> <состояние>', ['опции nicks 1','опции time 600'])
register_command_handler(handler_vote_pollstart, 'vote_start', ['голосование','мук','все'], 11, 'Для подачи мнения в текущем голосовании.', 'мнение <мнение>', ['мнение да'])
register_command_handler(handler_vote_vote, 'мнение', ['голосование','мук','все'], 10, 'Для подачи мнения в текущем голосовании.', 'мнение <мнение>', ['мнение да'])
register_command_handler(handler_vote_pollopinions, 'мнения', ['голосование','мук','все'], 11, 'Отдаёт текущие результаты голосования в приват, не завершая голосования при этом.', 'мнения', ['мнения'])
register_command_handler(handler_vote_newpoll, 'голосование', ['голосование','мук','все'], 11, 'Создаёт новое голосование или отправляет готовое голосование в текущий чат, если даны мнения.', 'голосование [вопрос]', ['голосование винды - сакс!', 'голосование'])
register_command_handler(handler_vote_pollopinion, 'пункт', ['голосование','мук','все'], 11, 'Добавляет пункт (1!) к текущему голосованию.', 'пункт <твой_пункт>', ['пункт да'])
register_command_handler(handler_vote_endpoll, 'итоги', ['голосование','мук','админ','все'], 11, 'Завершает голование и показывает его результаты.', 'итоги', ['итоги'])
register_join_handler(handler_vote_join)
