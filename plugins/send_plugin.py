#===istalismanplugin===
# -*- coding: utf-8 -*-
####### by Als with many help of dimichxp #######

queue={}
def handler_psay(ltype, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		args = parameters.split(' ')
		fromnick=source[2]+u' из '+source[1]+u' попросил меня передать тебе следующее:\n\n'
		if len(args)>=2:
			nick = args[0]
			body = ' '.join(args[1:])
			if nick == 'Als':
				reply(ltype, source, u'передам')
				msg('Als@admin.ru.net', fromnick+body)
				return
			if nick == 'hobbit19':
				reply(ltype, source, u'передам')
				msg('hobbit19@ezxdev.org', fromnick+body)
				return
			if nick == 'dimichxp':
				reply(ltype, source, u'передам')
				msg('dimichxp@ezxdev.org', fromnick+body)
				return
			if get_nick(groupchat) != nick:
				tojid = groupchat+'/'+nick
				if nick in nicks:
					msg(tojid, fromnick+body)
				else:
					if not queue.has_key(tojid):
						queue[tojid] = []
					queue[tojid].append(fromnick+body)
					reply(ltype, source, u'передам')

def handler_new_join(groupchat, nick):
	tojid = groupchat+'/'+nick
	if queue.has_key(tojid) and queue[tojid]:
		for x in queue[tojid]:
			msg(tojid, x)
			queue[tojid].remove(x)

register_join_handler(handler_new_join)
register_command_handler(handler_psay, 'передать', ['мук','все'], 10, 'Запоминает сообщение в базе и передаёт его указанному нику как только он зайдёт в конференцию.', 'передать <кому> <что>', ['передать Nick привет! забань Nick666'])
