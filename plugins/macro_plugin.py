#===istalismanplugin===
# -*- coding: utf-8 -*-


def macroadd_handler(type, source, parameters):
	pl = MACROS.parse_cmd(parameters)
	if (len(pl)<2):
		rep = u'мало аргументофф'
	else:
		MACROS.add(pl[0], pl[1], source[1])
#		write_file('dynamic/'+source[1]+'macros.txt', str(MACROS.macrolist[source[1]]))
		MACROS.flush()
		rep = u'добавил'
	reply(type, source, rep)
	
def gmacroadd_handler(type, source, parameters):
	pl = MACROS.parse_cmd(parameters)
	if (len(pl)<2):
		rep = u'мало аргументофф'
	else:
		MACROS.add(pl[0], pl[1])
		write_file('dynamic/macros.txt', str(MACROS.gmacrolist))
		rep = u'добавил'
	reply(type, source, rep)

def macrodel_handler(type, source, parameters):
	if parameters:
		answ=MACROS.remove(parameters, source[1])
#		write_file('dynamic/'+source[1]+'macros.txt', str(MACROS.macrolist[source[1]]))
		MACROS.flush()
		rep = u'убил'
	else:
		rep = u'мало аргументофф'
	reply(type, source, rep)
	
def gmacrodel_handler(type, source, parameters):
	if parameters:
		answ=MACROS.remove(parameters)
		write_file('dynamic/macros.txt', str(MACROS.gmacrolist))
		rep = u'убил'
	else:
		rep = u'мало аргументофф'
	reply(type, source, rep)

def macroexpand_handler(type, source, parameters):
	if parameters:
		rep=MACROS.comexp(parameters, source)
		if not rep:
			rep = u'не экспандится. прав маловато?'
	else:
		rep = u'мало аргументофф'
	reply(type, source, rep)
	
def gmacroexpand_handler(type, source, parameters):
	if parameters:
		rep=MACROS.comexp(parameters, source, '1')
	else:
		rep = u'мало аргументофф'
	reply(type, source, rep)

def macroinfo_handler(type, source, parameters):
	rep=''
	if parameters:
		try:
			if MACROS.macrolist[source[1]].has_key(parameters):
				rep = parameters+' -> '+MACROS.macrolist[source[1]][parameters]
		except:
			rep = u'нет такого макроса'
	elif parameters == 'allmac':
		rep += '\n'.join([x+' -> '+ MACROS.macrolist[source[1]][x] for x in MACROS.macrolist[source[1]]])
	reply(type, source, rep)
	
def gmacroinfo_handler(type, source, parameters):
	rep=''
	if parameters:
		try:
			if MACROS.macrolist[source[1]].has_key(parameters):
				rep = parameters+' -> '+MACROS.macrolist[source[1]][parameters]
			elif MACROS.gmacrolist.has_key(parameters):
				rep = parameters+' -> '+MACROS.gmacrolist[parameters]
		except:
			rep = u'нет такого макроса'
	elif parameters == 'allmac':
		rep += '\n'.join([x+' -> '+ MACROS.macrolist[source[1]][x] for x in MACROS.macrolist[source[1]]])
		rep += '\n'.join([x+' -> '+ MACROS.macrolist[x] for x in MACROS.macrolist])
	reply(type, source, rep)
	
def macrolist_handler(type, source, parameters):
	rep=u'Cписок макросов:'
	try:
		if MACROS.macrolist[source[1]]:
			rep += u'\nЛОКАЛЬНЫЕ\n'+', '.join(MACROS.macrolist[source[1]].keys())
	except:
		rep+=u'\nнет локальных макросов'
	rep += u'\nГЛОБАЛЬНЫЕ\n'+', '.join(MACROS.gmacrolist.keys())
	if type=='public':
		reply(type, source, u'ушёл')
	reply('private', source, rep)
	
def macroaccess_handler(type, source, parameters):
	if parameters:
		args = parameters.split(' ')
		if len(args)==2:
			macro = args[0]
			access = args[1]
			MACROS.give_access(macro,access,source[1])
			reply(type,source,u'дал')
			time.sleep(1)
#			write_file('dynamic/'+source[1]+'macroaccess.txt', str(MACROS.accesslist[source[1]]))
			MACROS.flush()
		else:
			reply(type,source,u'что за бред?')
			
def gmacroaccess_handler(type, source, parameters):
	if parameters:
		args = parameters.split(' ')
		if len(args)==2:
			macro = args[0]
			access = args[1]
			MACROS.give_access(macro,access)
			reply(type,source,u'дал')
			time.sleep(1)
			write_file('dynamic/macroaccess.txt', str(MACROS.accesslist))
		else:
			reply(type,source,u'что за бред?')


register_command_handler(macroadd_handler, 'macroadd', ['админ','макро','все'], 20, 'Добавить макро. Само макро должно быть заключено в апострофы `` !!!', 'macroadd [название] [`макро`]', ['macroadd глюк `сказать /me подумал, что все глючат`'])
register_command_handler(gmacroadd_handler, 'gmacroadd', ['суперадмин','макро','все'], 100, 'Добавить макро глобально. Само макро должно быть заключено в апострофы `` !!!', 'gmacroadd [название] [`макро`]', ['gmacroadd глюк `сказать /me подумал, что все глючат`'])

register_command_handler(macrodel_handler, 'macrodel', ['админ','макро','все'], 20, 'Удалить макро.', 'macrodel [название]', ['macrodel глюк'])
register_command_handler(gmacrodel_handler, 'gmacrodel', ['суперадмин','макро','все'], 100, 'Удалить глобальное макро.', 'macrodel [название]', ['macrodel глюк'])

register_command_handler(macroexpand_handler, 'macroexp', ['админ','макро','инфо','все'], 20, 'Развернуть макро, т.е. посмотреть на готовое макро в сыром виде.', 'macroexp [название] [параметры]', ['macroexp админ бот'])
register_command_handler(gmacroexpand_handler, 'gmacroexp', ['суперадмин','макро','инфо','все'], 100, 'Развернуть макро, т.е. посмотреть на него в сыром виде.', 'gmacroexp [название] [параметры]', ['gmacroexp админ бот'])

register_command_handler(macroinfo_handler, 'macroinfo', ['админ','макро','инфо','все'], 20, 'Открыть макро, т.е. просто посмотреть как выглядит макро. Чтобы посмотреть на все макро напишите вместо названия определённого макро "allmac" без кавычек.', 'macroinfo [название]', ['macroinfo глюк','macroinfo allmac'])
register_command_handler(gmacroinfo_handler, 'gmacroinfo', ['суперадмин','макро','инфо','все'], 100, 'Открыть макро (любое), т.е. просто посмотреть как выглядит макро. Чтобы посмотреть на все макро напишите вместо названия определённого макро "allmac" без кавычек.', 'macroinfo [название]', ['macroinfo глюк','macroinfo allmac'])

register_command_handler(macrolist_handler, 'macrolist', ['хелп','макро','инфо','все'], 10, 'Список макро.', 'macrolist', ['macrolist'])

register_command_handler(macroaccess_handler, 'macroaccess', ['админ','макро','все'], 20, 'Изменить доступ к определённому макро.', 'macroaccess [макро] [доступ]', ['macroaccess глюк 10'])
register_command_handler(macroaccess_handler, 'gmacroaccess', ['суперадмин','макро','все'], 100, 'Изменить доступ к определённому макро (любому).', 'gmacroaccess [макро] [доступ]', ['macroaccess админ 20'])
