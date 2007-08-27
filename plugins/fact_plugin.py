#===istalismanplugin===
# -*- coding: utf-8 -*-
####### It is translated by Als #######

TLD_FILE = 'static/tlds.txt'

def fact_tld(query):
	fp = open(TLD_FILE, u'r')
	while 1:
		line = fp.readline()
		if not line:
			return u'не нашёл :('
		(key, value) = string.split(line, ': ', 1)
		if string.lower(query).strip() == string.lower(key).strip():
			return value.strip()

def handler_fact_tld(type, source, parameters):
	result = fact_tld(parameters.strip())
	reply(type, source, result)


register_command_handler(handler_fact_tld, {1: 'нахождение', 2: 'nethost', 3: '!tld'}, ['инфо','все'], 10, 'Показвает нахождение домена первого уровня (географическое).', 'nethost <название/сокращение>', ['nethost ru', 'nethost russia'])
