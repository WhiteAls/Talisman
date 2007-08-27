#===istalismanplugin===
# -*- coding: utf-8 -*-
####### by Als #######

def handler_eye_stick(type, source, parameters):
	groupchat = source[1]
	if parameters:
		args = parameters.split(' ')
		if not parameters == u'себя':
			if len(args)<=1:
				nick = args[0]
				replies = [u'/me облил ' +nick+ u' ледяной водой',u'/me закидал ' +nick+ u' тухлыми помидорами',u'/me шарахнул ' +nick+ u' веслом по голове',u'/me ткнул ' +nick+ u' в глаз',u'/me поставил ' +nick+ u' подножку',u'/me постукал ' +nick+ u' головой апстенку',u'/me дал ' +nick+ u' йаду',u'/me slaps ' +nick+ u' around a bit with a large trout',u'приковал наручниками к кровати '+nick+u' и заставляет слушать Децла. МНОГО ДЕЦЛА!']
				replyy = random.choice(replies)
				msg(source[1],replyy)
				return
			elif len(args)>=2:
				nick = args[0]
				body = ' '.join(args[1:])
				msg(source[1],  u'/me ткнул '+nick+u' '+body)
		else:
			reply(type, source, u'шибко умный, да? ]:->')	
	else:
		reply(type, source, u'мазохист? :D')
		
		
		
def handler_test(type, source, parameters):
	reply(type,source,u'пассед')
	
def handler_clean_conf(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
		for x in range(1, 20):
			msg(source[1], x)
			time.sleep(1.23)

			
def handler_kick_ass(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
		splitdata = string.split(parameters)
		for x in range(1, int(splitdata[1])):
			msg(source[1]+'/'+splitdata[0], x)
			time.sleep(1.2)
	

	
	
register_command_handler(handler_eye_stick, {1: 'тык', 2: 'stick', 3: '!stick'}, ['фан','все'], 10, 'Ткнуть кого-то в глаз или во что-то.', 'stick <ник> <куда>', ['stick qwerty','stick qwerty в живот'])
register_command_handler(handler_test, {1: 'тест', 2: 'test', 3: '!test'}, ['фан','инфо','все'], 0, 'Тупо отвечает пассед.', 'test', ['test'])
register_command_handler(handler_clean_conf, {1: 'фконфу', 2: 'cls', 3: '!clean'}, ['фан','мук','все'], 15, 'Очищает конференцию (считает до 20).', 'cls', ['cls'])
register_command_handler(handler_kick_ass, {1: 'засрать', 2: 'torture', 3: '!ass'}, ['фан','суперадмин','мук','все'], 100, 'Засирает конфожид указанным количеством мессаг.', 'torture [ник] [кол-во]', ['torture Als 100'])
