#===istalismanplugin===
# -*- coding: utf-8 -*-
####### all by Als and dimichxp #######

def handler_help_help(type, source, parameters):
	ctglist = []
	if parameters and COMMANDS.has_key(parameters.strip()):
		rep = COMMANDS[parameters.strip()]['desc'].decode("utf-8") + u'\nКатегории: '
		for cat in COMMANDS[parameters.strip()]['category']:
			ctglist.append(cat)
		rep += ', '.join(ctglist).decode('utf-8')+u'\nИспользование: ' + COMMANDS[parameters.strip()]['syntax'].decode("utf-8") + u'\nПримеры:'
		for example in COMMANDS[parameters]['examples']:
			rep += u'\n  >>  ' + example.decode("utf-8")
		rep += u'\nНеобходимый уровень доступа: ' + str(COMMANDS[parameters.strip()]['access'])
	else:
		rep = u'напиши слово "команды" (без кавычек), чтобы получить список команд, "помощь <команда>" для получения помощи по команде, macrolist для получения списка макросов, а также macroacc <макрос> для получения уровня доступа к определёному макросу\np.s. уровень доступа смотрите в привате'
	reply(type, source, rep)

def handler_help_COMMANDS(type, source, parameters):
	date=time.strftime('%d %b %Y (%a)', time.gmtime()).decode('utf-8')
	groupchat=source[1]
	if parameters:
		rep = ''
		total = 0
		param=parameters.encode("utf-8")
		catcom=set([((param in COMMANDS[x]['category']) and x) or None for x in COMMANDS]) - set([None])
		if not catcom:
			reply(type,source,u'а есть и такая? :-O')
			return
		for cat in catcom:
			if has_access(source, COMMANDS[cat]['access'],groupchat):
				rep += cat+' '
				total = total + 1
		if rep:
			if type == 'public':
				reply(type,source,u'ушли')
			reply('private', source, u'Список команд в категории <'+parameters+u'> на '+date+u':\n\n' + rep+u' ('+str(total)+u' штук)')
		else:
			reply(type,source,u'плохая шутка ]:->')
	else:
		cats = set()
		for x in [COMMANDS[x]['category'] for x in COMMANDS]:
			cats = cats | set(x)
		cats = ', '.join(cats).decode('utf-8')
		if type == 'public':
			reply(type,source,u'ушли')
		reply('private', source, u'Список категорий на '+date+u'\n'+ cats+u'\n\nДля просмотра списка команд содержащихся в категории наберите "команды категория" без кавычек, например "команды все"')


register_command_handler(handler_help_help, 'помощь', ['хелп','инфо','все'], 0, 'Даёт основную справку или посылает информацию об определённой команде.', 'помощь [команда]', ['помощь', 'помощь пинг'])
register_command_handler(handler_help_COMMANDS, 'команды', ['хелп','инфо','все'], 0, 'Показывает список всех категорий команд. При запросе категории показывает список команд находящихся в ней.', 'команды [категория]', ['команды','команды все'])
