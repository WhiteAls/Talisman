#===istalismanplugin===
# -*- coding: utf-8 -*-
####### It is translated by Als #######

import rwhois

def handler_domain_domain(type, source, parameters):
	rec = rwhois.WhoisRecord(parameters)
	try:
		rec.whois()
		rep = u'зареган уже'
	except 'NoSuchDomain', reason:
		rep = u'хватай, пока доступен :)'
	except socket.error, (ecode,reason):
		rep = u'что-то глючит...'
	except "TimedOut", reason:
		rep = u'не дождался :('
	reply(type, source, rep)

#register_command_handler(handler_domain_domain, 'домен', ['инфо','все'], 10, 'Показывает инфу об определённом домене.', 'домен <домен>', ['домен motofan.ru'])
