#===istalismanplugin===
# -*- coding: utf-8 -*-
####### all by Als #######

seendb={}

def time_conv(time):
	rep = ''
	seconds = int(time) % 60
	minutes = int(time) / 60
	hours = minutes / 60
	minutes %= 60
	days = hours / 24
	months = days / 30
	years = months / 12
	hours %= 24
	if years:
		if int(years)>4:
			rep += str(years) + u' год '
			for x in range(int(years)):
				months = months-12
		else:
			rep += str(years) + u' лет '
	if months:
		rep += str(months) + u' мес '
		for x in range(int(months)):
			days = days-30
	if days: rep += str(days) + u' дн '
	if hours: rep += str(hours) + u' час '
	if minutes: rep += str(minutes) + u' мин '
	rep += str(seconds) + u' сек'
	return rep


def handler_seen(type,source,parameters):
	groupchat=source[1]
	DB='dynamic/'+groupchat+'/seendb.txt'
	if check_file(groupchat,'seendb.txt'):
		seendb = eval(read_file(DB))
	else:
		reply(type,source,u'ошибка при создании базы. скажите об этом админу бота')
		return
	if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(parameters):
		reply(type, source, u'глазки протри')
		return
	if not parameters:
		reply(type, source, u'и чё?')
		return
	if seendb.has_key(parameters):
		seen=time_conv(time.time() - seendb[parameters]['time'])
		reply(type, source, u'последний раз '+parameters+u' был тут '+seen+u' назад')
	else:
		keys=seendb.keys()
		for x in keys:
			if seendb[x]['nicks']:
				for y in seendb[x]['nicks']:
					if y==parameters:
						seen=time_conv(time.time() - seendb[y]['time'])
						reply(type, source, u'последний раз '+parameters+u' был тут '+seen+u' назад')
						return
		reply(type, source, u'я тут ни разу не видел '+parameters)
		
def seen_rec(groupchat, nick):
	DB='dynamic/'+groupchat+'/seendb.txt'
	if check_file(groupchat,'seendb.txt'):
		seendb = eval(read_file(DB))
	else:
		reply(type,nick,u'ошибка при создании базы. скажите об этом админу бота')
		return
	jid=get_true_jid(groupchat+'/'+nick)
	if seendb.has_key(jid):
		alr=seendb[jid]
		if not seendb[alr]['nicks']=='':
			for x in seendb[alr]['nicks']:
				if not nick==x:
					seendb[alr]['nicks'].append(nick)
		else:
			seendb[alr]['nicks'].append(nick)	
	if not seendb.has_key(nick):
		seendb[nick]=nick
		seendb[nick]={}
		seendb[nick]['nicks']=[]
		seendb[nick]['nicks']=nick
		seendb[jid]=nick
	seendb[nick]['time']=time.time()
	if not seendb[nick]['nicks']=='':
		for x in seendb[nick]['nicks']:
			if not nick==x:
				seendb[nick]['nicks'].append(nick)
	else:
		seendb[nick]['nicks'].append(nick)
	time.sleep(2)
	write_file(DB, str(seendb))


def nick_change(prs):
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	DB='dynamic/'+groupchat+'/seendb.txt'
	if check_file(groupchat,'seendb.txt'):
		seendb = eval(read_file(DB))
	else:
		reply(type,nick,u'ошибка при создании базы. скажите об этом админу бота')
		return
	time.sleep(1)
	jid=get_true_jid(groupchat+'/'+nick)
	if seendb.has_key(jid):
		alr=seendb[jid]		
		if not seendb[alr]['nicks']=='':
			for x in seendb[alr]['nicks']:
				if not nick==x:
					seendb[alr]['nicks'].append(nick)
		else:
			seendb[nick]['nicks'].append(nick)
	time.sleep(2)
	write_file(DB, str(seendb))
	

register_presence_handler(nick_change)
register_leave_handler(seen_rec)
register_command_handler(handler_seen, {1: 'син', 2: 'see', 3: '!seen'}, ['инфо','мук','все'], 10, 'Показывает когда ник был последний раз в конфе.', 'see <ник>', ['see guy'])
