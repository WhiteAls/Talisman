#===istalismanplugin===
# -*- coding: utf-8 -*-


def macroadd_handler(type, source, parameters):
	pl = MACROS.parse_cmd(parameters)
	if (len(pl)<2):
		rep = u'мало аргументофф'
	else:
		MACROS.add(pl[0], pl[1])
		write_file('dynamic/macros.txt', str(MACROS.macrolist))
		rep = u'добавил'
	reply(type, source, rep)

def macrodel_handler(type, source, parameters):
	if parameters:
		MACROS.remove(parameters)
		write_file('dynamic/macros.txt', str(MACROS.macrolist))
		rep = u'убил'
	else:
		rep = u'мало аргументофф'
	reply(type, source, rep)

def macroexpand_handler(type, source, parameters):
	if parameters:
		rep=MACROS.expand(parameters, source)
	else:
		rep = u'мало аргументофф'
	reply(type, source, rep)

def macroinfo_handler(type, source, parameters):
	if parameters:
		if MACROS.macrolist[parameters]:
			rep = parameters+' -> '+MACROS.macrolist[parameters]
		else:
			rep = u'нет такого макроса'
	else:
		rep = '\n'.join([x+' -> '+ MACROS.macrolist[x] for x in MACROS.macrolist])
	reply(type, source, rep)
	
def macrolist_handler(type, source, parameters):
	rep = u'Cписок макросов:\n'+', '.join(MACROS.macrolist.keys());
	if type=='public':
		reply(type, source, u'ушёл')
	reply('private', source, rep)
	
	
def macroaccess_handler(type, source, parameters):
	if parameters:
		args = parameters.split(' ')
		if len(args)==2:
			macro = args[0]
			access = args[1]
			MACROS.give_access(macro,access)
			reply(type,source,u'дал')
			time.sleep(1)
			MACROS.flush()
		else:
			reply(type,source,u'что за бред?')


register_command_handler(macroadd_handler, {1: 'macroadd', 2: 'macroadd', 3: '!macroadd'}, ['админ','макро','все'], 100, 'Добавить макро.', 'macroadd a `b`', ['macrodd a `b`'])
register_command_handler(macrodel_handler, {1: 'macrodel', 2: 'macrodel', 3: '!macrodel'}, ['админ','макро','все'], 100, 'Удалить макро.', 'macrodel a', ['macrodel a'])
register_command_handler(macroexpand_handler, {1: 'macroexp', 2: 'macroexp', 3: '!macroexp'}, ['админ','макро','инфо','все'], 100, 'Развернуть макро.', 'macroexp a b', ['macroexp a b'])
register_command_handler(macroinfo_handler, {1: 'macroinfo', 2: 'macroinfo', 3: '!macroinfo'}, ['админ','макро','инфо','все'], 100, 'Открыть макро.', 'macroinfo', ['macroinfo','macroinfo a'])
register_command_handler(macrolist_handler, {1: 'macrolist', 2: 'macrolist', 3: '!macrolist'}, ['хелп','макро','инфо','все'], 10, 'Список макро.', 'macrolist', ['macrolist'])
register_command_handler(macroaccess_handler, {1: 'macroaccess', 2: 'macroaccess', 3: '!macroaccess'}, ['админ','макро','все'], 100, 'Доступ к определённому макро.', 'macroaccess [макро] [доступ]', ['macroaccess модер 20'])
