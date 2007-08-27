#===istalismanplugin===
# -*- coding: utf-8 -*-
####### It is translated by Als #######

import socket

def dns_query(query):
	try:
		int(query[-1])
	except ValueError:
		try:
			return socket.gethostbyname(query)
		except socket.gaierror:
			return 'не нахожу что-то :('
	else:
		try:
			(hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(query)
		except socket.herror:
			return 'не нахожу что-то :('
		return hostname + ' ' + string.join(aliaslist) + ' ' + string.join(aliaslist)

def handler_dns_dns(type, source, parameters):
	if parameters.strip():
		result = dns_query(parameters)
		reply(type, source, result)
	else:
		reply(type, source, 'чё-то ты не то написал...')

register_command_handler(handler_dns_dns, {1: 'днс', 2: 'nslookup', 3: '!dns'}, ['инфо','все'], 10, 'Показывает ответ от DNS для определённого хоста или IP адреса.', 'nslookup <хост/IP>', ['nslookup jabber.aq', 'nslookup 127.0.0.1'])
