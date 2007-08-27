#===istalismanplugin===
# -*- coding: utf-8 -*-
####### It is translated and modified by Als #######


def admin_groupchat_invite_handler(source, groupchat, body):
	if has_access(get_true_jid(source),COMMANDS[u'зайти']['access'],source[1]):
		join_groupchat(groupchat, DEFAULT_NICK)

def popups_check(gch):
	DBPATH='dynamic/'+gch+'/config.cfg'
	if check_file(gch,'config.cfg'):
		gchconfdb = eval(read_file(DBPATH))
		if gchconfdb.has_key('popups'):
			if gchconfdb['popups'] == 1:
				return 1
			else:
				return 0
		else:
			gchconfdb['popups']=1
			write_file(DBPATH,str(gchconfdb))
			return 1
				
def handler_admin_join(type, source, parameters):
	if parameters:
		nick = DEFAULT_NICK
		args = parameters.split(' ')
		if len(args)>1:
			#(groupchat, reason) = string.split(parameters.lstrip(), ' ', 1)
			groupchat = args[0]
			reason = ' '.join(args[1:])
		else:
			groupchat = parameters
			reason = ''
		join_groupchat(str(groupchat), nick)
		reply(type, source, u'я зашёл в -> <' + groupchat + '>')
		if popups_check(groupchat):
			if reason:
				msg(groupchat, u'меня привёл '+source[2]+u' по причине:\n'+reason)
			else:
				msg(groupchat, u'меня привёл '+source[2])
	else:
		reply(type, source, u'необходимо написать конфу, а потом причину (не обязательно)')

def handler_admin_leave(type, source, parameters):
	args = parameters.split(' ')
	groupchat = args[0]
	if len(args)>=2:
		reason = ' '.join(args[1:])
		if not GROUPCHATS.has_key(groupchat):
			reply(type, source, u'а меня там нету')
			return
	elif len(args)==1 and not args[0]=='':
		if not GROUPCHATS.has_key(args[0]):
			reply(type, source, u'а меня там нету')
			return
		reason = ''
	elif not parameters:
			groupchat = source[1]
			reason = ''
	if popups_check(groupchat):
		if reason:
			msg(groupchat, u'меня уводит '+source[2]+u' по причине:\n'+reason)
		else:
			msg(groupchat, u'меня уводит '+source[2])
	leave_groupchat(groupchat)
	reply(type, source, u'я ушёл из -> <' + groupchat + '>')


def handler_admin_msg(type, source, parameters):
	msg(string.split(parameters)[0], string.join(string.split(parameters)[1:]))
	reply(type, source, u'мессага ушла')
	
def handler_glob_msg_help(type, source, parameters):
	total = '0'
	totalblock='0'
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
		for x in gch:
			if popups_check(x):
				msg(x, u'Новости от '+source[2]+u':\n'+parameters+u'\nНапоминаю, что как всегда все помощь можно получить написав "помощь".\nО всех глюках, ошибках, ляпях, а также предложения и конструктивную критику прошу направлять мне таким образом: пишем "передать '+source[2]+u' и тут ваше сообщение", естественно без кавычек.\nСПАСИБО ЗА ВНИМАНИЕ!')
				totalblock = int(totalblock) + 1
			total = int(total) + 1
		reply(type, source, 'мессага ушла в '+str(totalblock)+' конференций (из '+str(total)+')')
		
def handler_glob_msg(type, source, parameters):
	total = '0'
	totalblock='0'
	if parameters:
		if GROUPCHATS:
			gch=GROUPCHATS.keys()
			for x in gch:
				if popups_check(x):
					msg(x, u'Новости от '+source[2]+':\n'+parameters)
					totalblock = int(totalblock) + 1
				total = int(total) + 1
			reply(type, source, 'мессага ушла в '+str(totalblock)+' конференций (из '+str(total)+')')
	

def handler_admin_say(type, source, parameters):
	if parameters:
		args=string.split(parameters)
		if not args[0] in COMMANDS.keys():
			msg(source[1], parameters)
		else:
			reply(type, source, u'нееее')
			return
	else:
		reply(type, source, u'мессагу написать не забыл?')

def handler_admin_restart(type, source, parameters):
	if parameters:
		reason = parameters
	else:
		reason = ''
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
	if reason:
		for x in gch:
			if popups_check(x):
				msg(x, u'меня перезагружает '+source[2]+u' по причине:\n'+reason)
	else:
		for x in gch:
			if popups_check(x):
				msg(x, u'меня перезагружает '+source[2])
	JCON.disconnect()
	os.execv('./neutron.py', sys.argv)

def handler_admin_exit(type, source, parameters):
	if parameters:
		reason = parameters
	else:
		reason = ''
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
	if reason:
		for x in gch:
			if popups_check(x):
				msg(x, u'меня выключает '+source[2]+u' по причине:\n'+reason)
	else:
		for x in gch:
			if popups_check(x):
				msg(x, u'меня выключает '+source[2])
	global AUTO_RESTART
	JCON.disconnected()
	sys.exit(1)


def handler_popups_startstop(type, source, parameters):
	if parameters:
		args = parameters.split(' ')
		if GROUPCHATS.has_key(args[0]):
			DBPATH='dynamic/'+args[0]+'/config.cfg'
			if check_file(args[0],'config.cfg'):
				gchconfdb = eval(read_file(DBPATH))
				if args[1]=='1':
					gchconfdb['popups']=1
					reply(type,source,u'глобальные оповещения включены')
				else:
					gchconfdb['popups']=0
					reply(type,source,u'глобальные оповещения выключены')
				write_file(DBPATH,str(gchconfdb))
			else:
				reply(type,source,u'ошибка при создании базы')
		else:
			reply(type,source,u'ты уверен, что я там есть?')
	else:
		DBPATH='dynamic/'+source[1]+'/config.cfg'
		if check_file(source[1],'config.cfg'):
			gchconfdb = eval(read_file(DBPATH))
		ison=gchconfdb['popups']
		if ison==1:
			reply(type,source,u'здесь глобальные оповещения включены')
		else:
			reply(type,source,u'здесь глобальные оповещения выключены')




register_command_handler(handler_admin_join, {1: 'зайти', 2: 'rjoin', 3: '!join'}, ['суперадмин','мук','все'], 40, 'Зайти в определённую конфу.', 'rjoin <конфа> [причина]', ['rjoin ы@conference.jabber.aq', 'rjoin ы@conference.jabber.aq уря'])
register_command_handler(handler_admin_leave, {1: 'свал', 2: 'rleave', 3: '!leave'}, ['админ','мук','все'], 20, 'Заставляет выйти из текущей или определённой конфы.', 'rleave <конфа> [причина]', ['rleave ы@conference.jabber.aq спать', 'rleave спать','rleave'])
register_command_handler(handler_admin_msg, {1: 'мессага', 2: 'msg', 3: '!msg'}, ['админ','мук','все'], 30, 'Отправляет мессагу от имени бота определённому JID-у.', 'msg <jid> <мессага>', ['msg guy@jabber.aq здорово чувак!'])
register_command_handler(handler_admin_say, {1: 'сказать', 2: 'say', 3: '!say'}, ['админ','мук','все'], 20, 'Отправляет мессагу в текущую конфу или на определённый JID конфы.', 'say <мессага>', ['say салют пиплы'])
register_command_handler(handler_admin_restart, {1: 'рестарт', 2: 'restart', 3: '!restart'}, ['суперадмин','все'], 100, 'Рестартит бота.', 'restart [причина]', ['restart','restart гы'])
register_command_handler(handler_admin_exit, {1: 'пшёл', 2: 'switchoff', 3: '!switchoff'}, ['суперадмин','все'], 100, 'Полный выход.', 'switchoff [причина]', ['switchoff','switchoff глюки'])
register_command_handler(handler_glob_msg, {1: 'globmsg', 2: 'globmsg', 3: '!globmsg'}, ['суперадмин','мук','все'], 100, 'Разослать сообщение по всем конфам, в которых сидит бот.', 'globmsg [мессага]', ['globmsg всем привет!'])
register_command_handler(handler_glob_msg_help, {1: 'hglobmsg', 2: 'hglobmsg', 3: '!hglobmsg'}, ['суперадмин','мук','все'], 100, 'Разослать сообщение по всем конфам, в которых сидит бот.', 'globmsg [мессага]', ['globmsg всем привет!'])
register_command_handler(handler_popups_startstop, {1: 'popups', 2: 'popups', 3: '!popups'}, ['админ','мук','все'], 30, 'Отключает (0) или включает (1) сообщения о входах/выходах, рестартах/выключениях, а также глобальные новости для определённой конфы. Без параметра покажет текущее состояние.', 'popups [конфа] [1|0]', ['popups chat@conference.jabber.aq 1','popups chat@conference.jabber.aq 0','popups'])

register_groupchat_invite_handler(admin_groupchat_invite_handler)
