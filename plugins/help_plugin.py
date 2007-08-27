#===istalismanplugin===
# -*- coding: utf-8 -*-
####### all by Als and dimichxp #######

def handler_help_help(type, source, parameters):
	comset=COMSET[source[1]]
	ctglist = []
	if parameters and COMMANDS[comset].has_key(parameters.strip()):
		rep = COMMANDS[comset][parameters.strip()]['desc'].decode("utf-8") + u'\nКатегории: '
		for cat in COMMANDS[comset][parameters.strip()]['category']:
			ctglist.append(cat)
		rep += ', '.join(ctglist).decode('utf-8')+u'\nИспользование: ' + COMMANDS[comset][parameters.strip()]['syntax'].decode("utf-8") + u'\nПримеры:'
		for example in COMMANDS[comset][parameters]['examples']:
			rep += u'\n  >>  ' + example.decode("utf-8")
		rep += u'\nНеобходимый уровень доступа: ' + str(COMMANDS[comset][parameters.strip()]['access'])
	else:
		if comset==1:
			comm=u'команды'
			comm1=u'помощь'
		elif comset==2:
			comm=u'commands'
			comm1=u'helpme'
		elif comset==3:
			comm=u'!commands'
			comm1=u'!help'
		rep = u'напиши слово "'+comm+u'" (без кавычек), чтобы получить список команд, '+comm1+u' <команда> для получения помощи по команде, macrolist для получения списка макросов, а также macroacc <макрос> для получения уровня доступа к определёному макросу\np.s. уровень доступа смотрите в привате'
	reply(type, source, rep)

def handler_help_commands(type, source, parameters):
	comset=COMSET[source[1]]
	date=time.strftime('%d %b %Y (%a)', time.gmtime()).decode('utf-8')
	groupchat=source[1]
	if parameters:
		rep = ''
		total = 0
		param=parameters.encode("utf-8")
		catcom=set([((param in COMMANDS[comset][x]['category']) and x) or None for x in COMMANDS[comset]]) - set([None])
		for cat in catcom:
			if has_access(source, COMMANDS[comset][cat]['access'],groupchat):
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
		for x in [COMMANDS[comset][x]['category'] for x in COMMANDS[comset]]:
			cats = cats | set(x)
		cats = ', '.join(cats).decode('utf-8')
		if type == 'public':
			reply(type,source,u'ушли')
		reply('private', source, u'Список категорий на '+date+u'\n'+ cats+u'\n\nДля просмотра списка команд содержащихся в категории наберите "команды категория" без кавычек')
 
 
def handler_commandset(type, source, parameters):
	if parameters:
		CFGPATH='dynamic/'+source[1]+'/config.cfg'
		if check_file(source[1],'config.cfg'):
			cfg = eval(read_file(CFGPATH))
		else:
			reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')
			return
		rep=u''
		comset=parameters.strip()
		if comset=='1':
			rep=u'включен первый набор команд - русские без экранирования'
			desc=u'в данной конференции включен первый набор команд - русские без экранирования'
			comm=u'помощь'
			cfg['comset']=int(parameters.strip())
			if not COMSET.has_key(source[1]):
				COMSET[source[1]]=source[1]
			COMSET[source[1]]=int(parameters.strip())
			write_file(CFGPATH, str(cfg))
		elif comset=='2':
			rep=u'включен второй набор команд - английские без экранирования'
			desc=u'в данной конференции включен второй набор команд - английские без экранирования'
			comm=u'helpme'
			cfg['comset']=int(parameters.strip())
			if not COMSET.has_key(source[1]):
				COMSET[source[1]]=source[1]
			COMSET[source[1]]=int(parameters.strip())
			write_file(CFGPATH, str(cfg))
		elif comset=='3':
			rep=u'включен третий набор команд - английские, экранированные символом !'
			desc=u'в данной конференции включен третий набор команд - английские, экранированные симвоволом (!)'
			comm=u'!help'
			cfg['comset']=int(parameters.strip())
			if not COMSET.has_key(source[1]):
				COMSET[source[1]]=source[1]
			COMSET[source[1]]=int(parameters.strip())
			write_file(CFGPATH, str(cfg))
		else:
			rep=u'этого набора команд не существует'
		reply(type,source,rep)
		nick = get_nick(source[1])
		presence=xmpp.protocol.Presence(source[1]+'/'+nick)		
		presence.setStatus(u'напишите "'+comm+u'" и следуйте указаниям, чтобы понять что к чему!\n'+desc)
		presence.setTag('x',namespace=xmpp.NS_MUC).addChild('history',{'maxchars':'0','maxstanzas':'0'})
		JCON.send(presence)
	else:
		comset=COMSET[source[1]]
		if comset==1:
			num=u'первый'
			desc=u'русские без экранирования'
		elif comset==2:
			num=u'второй'
			desc=u'английские без экранирования'
		elif comset==3:
			num=u'третий'
			desc=u'английские, экранированные симвоволом (!)'
		reply(type,source,u'в данной конфе включен '+num+u' набор команд ('+desc+u')')
		
	



register_command_handler(handler_help_help, {1: 'помощь', 2: 'helpme', 3: '!help'}, ['хелп','инфо','все'], 0, 'Даёт основную справку или посылает информацию об определённой команде.', 'helpme [команда]', ['helpme', 'help версия'])
register_command_handler(handler_help_commands, {1: 'команды', 2: 'commands', 3: '!commands'}, ['хелп','инфо','все'], 0, 'Показывает список всех категорий команд. При запросе категории показывает список команд находящихся в ней.', 'commands [категория]', ['commands','commands все'])
register_command_handler(handler_commandset, {1: 'комсет', 2: 'commset', 3: '!commset'}, ['админ','все'], 30, 'Устанавливает определённый набор команд для текущей конференции. 1 набор - русские команды без экранирования, 2 набор - английские без экранирования, 3 набор - английские, экранированные символом (!).', 'commset [набор]', ['commset','commset 1'])
