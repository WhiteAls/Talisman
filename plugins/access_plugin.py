#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  access_plugin.py

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


def handler_access_login(type, source, parameters):
	if type == 'public':
		reply(type, source, u'тормоз, это надо было делать в привате')
	elif type == 'private':
		jid = get_true_jid(source)
		if parameters.strip() == ADMIN_PASSWORD:
			change_access_temp(source[1], jid, 100)
			reply(type, source, u'угу, точняк')
		else:
			reply(type, source, u'пшёл вон, я хз кто ты >)')

def handler_access_logout(type, source, parameters):
	jid = get_true_jid(source)
	change_access_temp(source[1], jid, 10)
	reply(type, source, u'бб')

def handler_access_view_access(type, source, parameters):
	accdesc={'-1':'(заблокирован)','0':'(никто)','1':'(лол)','10':'(юзер)','11':'(мембер)','15':'(модер)','16':'(модер)','20':'(админ)','30':'(овнер)','40':'(джойнер)','100':'(админ бота)'}
	if parameters==u'!desc':
		reply('private',source,u'-1 - не сможет сделать ничего\n0 - очень ограниченное кол-во команд и макросов, автоматически присваивается визиторам (visitor)\n10 - стандартный набор команд и макросов, автоматически присваивается партисипантам (participant)\n11 - расширенный набор команд и макросов (например доступ к !!!), автоматически присваивается мемберам (member)\n15 (16) - модераторский набор команд и макросов, автоматически присваевается модераторам (moderator)\n20 - админский набор команд и макросов, автоматически присваивается админам (admin)\n30 - овнерский набор команд и макросов, автоматически присваиватся овнерам (owner)\n40 - не реализовано сейчсас толком, позволяет юзеру с этим доступом заводить и выводить бота из конференций\n100 - администратор бота, может всё')
		return
	if not parameters:
		level=str(user_level(source[1]+'/'+source[2], source[1]))
		if level in accdesc.keys():
			levdesc=accdesc[level]
		else:
			levdesc=''		
		reply(type, source, level+' '+levdesc)
	else:
		nicks = GROUPCHATS[source[1]].keys()
		if parameters.strip() in nicks:
			level=str(user_level(source[1]+'/'+parameters.strip(),source[1]))
			if level in accdesc.keys():
				levdesc=accdesc[level]
			else:
				levdesc=''
			reply(type, source, level+' '+levdesc)
		else:
			reply(type, source, u'а он тут? :-O')

def handler_access_set_access(type, source, parameters):
	splitdata = string.split(parameters)
	if not splitdata[1].strip() is types.IntType:
		reply(type, source, u'что это было?')
		return
	nicks=GROUPCHATS[source[1]]
	if len(splitdata) > 4:
		if not splitdata[0:1].strip() in nicks:
			reply(type, source, u'а он тут? :-O')
			return
	else:
		if not splitdata[0].strip() in nicks:
			reply(type, source, u'а он тут? :-O')
			return
	tjidto=get_true_jid(source[1]+'/'+splitdata[0].strip())
	tjidsource=get_true_jid(source)
	groupchat=source[1]
	jidacc=user_level(source, groupchat)
	if tjidsource in ADMINS:
		pass
	elif int(splitdata[1]) > int(jidacc):
		reply(type, source, u'ага, щаззз')
		return
	if len(splitdata) == 2:
		change_access_temp(source[1], tjidto, splitdata[1].strip())
		reply(type, source, u'дал временно')
	elif len(splitdata) == 3:
		change_access_perm(source[1], tjidto, splitdata[1].strip())
		reply(type, source, u'дал навсегда')
	else:
		reply(type, source, u'прочитай хелп по команде')
		
		
def handler_access_set_access_glob(type, source, parameters):
	if parameters:
		splitdata = string.split(parameters)
		if len(splitdata)<2:
			reply(type, source, u'эээ?')
			return
		nicks=GROUPCHATS[source[1]].keys()
		if not splitdata[0].strip() in nicks:
			reply(type, source, u'а он тут? :-O')
			return
		tjidto=get_true_jid(source[1]+'/'+splitdata[0])
		change_access_perm_glob(tjidto, splitdata[1])
		reply(type, source, u'дал')

def handler_access_unset_access_glob(type, source, parameters):
	splitdata = string.split(parameters)
	tjidto=get_true_jid(source[1]+'/'+splitdata[0])
	change_access_perm_glob(tjidto)
	reply(type, source, u'снял')


register_command_handler(handler_access_login, 'логин', ['доступ','админ','все'], 0, 'Залогиниться как админ.', 'логин <пароль>', ['логин мой_пароль'])
register_command_handler(handler_access_login, 'логаут', ['доступ','админ','все'], 0, 'Разлогиниться.', 'логаут', ['логаут'])
register_command_handler(handler_access_view_access, 'доступ', ['доступ','админ','все'], 0, 'Показывает уровень доступа определённого ника.', 'доступ [ник]', ['доступ', 'доступ guy'])
register_command_handler(handler_access_set_access, 'дать_доступ', ['доступ','админ','все'], 15, 'Устанавливает уровень доступа для определённого ника на определённый уровень. Если указываеться третий параметр, то изменение происходит навсегда, иначе установленный уровень будет действовать до выхода бота из конфы.', 'дать_дотсуп <ник> <уровень> [навсегда]', ['дать_дотсуп guy 100', 'дать_дотсуп guy 100 что-нить там'])
register_command_handler(handler_access_set_access_glob, 'globacc', ['доступ','суперадмин','все'], 100, 'Устанавливает уровень доступа для определённого ника на определённый уровень ГЛОБАЛЬНО.', 'globacc <ник> <уровень>', ['globacc gay 100'])
register_command_handler(handler_access_unset_access_glob, 'unglobacc', ['доступ','суперадмин','все'], 100, 'Снимает глобальный уровень доступа с ЖИДА.', 'unglobacc <жид> ', ['globacc guy'])
