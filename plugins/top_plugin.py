#===istalismanplugin===
# -*- coding: utf-8 -*-
#######  by Als. megathanks for dimichxp #######


LOCALDB_FILE = 'dynamic/topdb.txt'


def handler_new_join(groupchat, nick):
	localdb = eval(read_file(LOCALDB_FILE))
	top=0
	datetime=time.strftime('%d.%m.%Y&%H:%M:%S UTC', time.gmtime())
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		for x in nicks:
			if x:
				top = top + 1
		if localdb.has_key(string.lower(groupchat)):
			if localdb[string.lower(groupchat)] == '0':
				localdb[groupchat] = str(top)+'&'+datetime
				write_file(LOCALDB_FILE, str(localdb))
			else:
				grouptop = string.split(localdb[string.lower(groupchat)], '&', 2)
				val = string.lower(grouptop[0]).strip()
				if val < top:
					return
				elif val > top:
					localdb[groupchat] = str(top)+'&'+datetime
					write_file(LOCALDB_FILE, str(localdb))
		else:
			localdb[groupchat] = 0
			write_file(LOCALDB_FILE, str(localdb))


def handler_get_top_users(type, source, parameters):
	localdb = eval(read_file(LOCALDB_FILE))
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		if localdb.has_key(groupchat):
			if localdb[string.lower(groupchat)] == '0':
				reply (type, source, u'топ ещё не посчитан')
			else:
				grouptop = string.split(localdb[string.lower(groupchat)], '&', 2)
				topval = string.lower(grouptop[0]).strip()
				topdate = grouptop[1].strip()
				toptime = grouptop[2].strip()
				reply (type, source, 'рекорд посещаемости '+topval+' юзеров одновременно. рекорд установлен '+topdate+' в '+toptime)
		else:
			reply (type, source, u'конфа ещё не прописалась в топе. нужно, чтобы в неё вошло как min два человека для регистрации')



register_join_handler(handler_new_join)
register_command_handler(handler_get_top_users, {1: 'топ', 2: 'muctop', 3: '!top'}, ['инфо','мук','все'], 10, 'Показывает рекорд посещаемости конфы. Сколько было юзеров одновременно онлайн и когда. ВРЕМЯ В UTC!!!', 'muctop', ['muctop'])
