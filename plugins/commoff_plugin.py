#===istalismanplugin===
# -*- coding: utf-8 -*-
####### all by Als #######

def handler_commoff(type,source,parameters):
	na=[u'доступ',u'дать_доступ',u'eval',u'логин',u'логаут',u'!stanza',u'unglobacc',u'помощь',u'свал',u'рестарт',u'globacc',u'команды',u'sh',u'exec',u'дать_доступ',u'commoff',u'common']
	valcomm,notvalcomm,alrcomm,npcomm,vcnt,ncnt,acnt,nocnt,commoff,rep=u'',u'',u'',u'',0,0,0,0,{},u''
	if check_file(source[1],'config.cfg'):
		DBPATH='dynamic/'+source[1]+'/config.cfg'
		cfgdb = eval(read_file(DBPATH))
		if cfgdb.has_key('commoff'):
			commoff=cfgdb
		else:
			commoff['commoff']='commoff'
			commoff['commoff']=[]
	else:
		reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')
		return
	if parameters:
		param=string.split(parameters, ' ')
		for y in param:
			if COMMANDS.has_key(y) or y=='*****' or y in MACROS.macrolist[source[1]] or y in MACROS.gmacrolist:
				if not y in na:
					if not y in commoff['commoff']:
						commoff['commoff'].append(y)
						vcnt+=1
						valcomm+=str(vcnt)+u') '+y+u'\n'
					else:
						acnt+=1
						alrcomm+=str(acnt)+u') '+y+u'\n'						
				else:
					ncnt+=1
					npcomm+=str(ncnt)+u') '+y+u'\n'
			else:
				nocnt+=1
				notvalcomm+=str(nocnt)+u') '+y+u'\n'
		if valcomm:
			rep+=u'для этой конфы были отключены следующие команды:\n'+valcomm
		if alrcomm:
			rep+=u'\nследующие команды не были отключены, поскольку они уже отключены:\n'+alrcomm
		if notvalcomm:
			rep+=u'\nперечисленные ниже команды вообще не команды :) :\n'+notvalcomm
		if npcomm:
			rep+=u'\nследующие команды отключать вообще нельзя:\n'+npcomm
		write_file(DBPATH, str(commoff))
		get_commoff(source[1])
	else:
		for x in commoff:
			vcnt+=1
			valcomm+=str(vcnt)+u' '+x+u'\n'
		if valcomm:
			rep=u'в этой конфе отключены следующие команды:\n'+valcomm
		else:
			rep=u'в этой конфе включены все команды\\'
			
		
	reply(type,source,rep[:-1])
		
def handler_common(type,source,parameters):
	na=[u'доступ',u'дать_доступ',u'eval',u'логин',u'логаут',u'!stanza',u'unglobacc',u'помощь',u'свал',u'рестарт',u'globacc',u'команды',u'sh',u'exec',u'дать_доступ',u'commoff',u'common']
	valcomm,notvalcomm,alrcomm,npcomm,vcnt,acnt,nocnt,ncnt,commoff,rep=u'',u'',u'',u'',0,0,0,0,{},u''
	if check_file(source[1],'config.cfg'):
		DBPATH='dynamic/'+source[1]+'/config.cfg'
		cfgdb = eval(read_file(DBPATH))
		if cfgdb.has_key('commoff'):
			commoff=cfgdb
		else:
			commoff['commoff']='commoff'
			commoff['commoff']=[]
	else:
		reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')
		return
	if parameters:
		param=string.split(parameters, ' ')
		for y in param:
			if COMMANDS.has_key(y) or y=='*****' or y in MACROS.macrolist[source[1]] or y in MACROS.gmacrolist:
				if not y in na:
					if y in commoff['commoff']:
						commoff['commoff'].remove(y)
						vcnt+=1
						valcomm+=str(vcnt)+u') '+y+u'\n'
					else:
						acnt+=1
						alrcomm+=str(acnt)+u') '+y+u'\n'						
				else:
					ncnt+=1
					npcomm+=str(ncnt)+u') '+y+u'\n'
			else:
				nocnt+=1
				notvalcomm+=str(nocnt)+u') '+y+u'\n'
		if valcomm:
			rep+=u'для этой конфы были включены следующие команды:\n'+valcomm
		if alrcomm:
			rep+=u'\nследующие команды не были включены, поскольку они не были отключены:\n'+alrcomm
		if notvalcomm:
			rep+=u'\nперечисленные ниже команды вообще не команды :) :\n'+notvalcomm
		if npcomm:
			rep+=u'\nследующие команды не отключаются вообще:\n'+npcomm
		write_file(DBPATH, str(commoff))
		get_commoff(source[1])
	else:
		rep=u'ииии?'
		
	reply(type,source,rep)
	
	
register_command_handler(handler_commoff, 'commoff', ['админ','мук','все'], 30, 'Отключает определённые команды для текущей конфы, без параметров показывает список уже отключенных команд.', 'commoff [команды]', ['commoff','commoff тык диско версия пинг'])
register_command_handler(handler_common, 'common', ['админ','мук','все'], 30, 'Включает определённые команды для текущей конфы.', 'common [команды]', ['common тык диско версия пинг'])
