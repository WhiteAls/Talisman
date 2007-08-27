#===istalismanplugin===
# -*- coding: utf-8 -*-

def handler_stanza(source, type, parameters):
	if parameters:
		node=xmpp.simplexml.XML2Node(unicode(parameters).encode('utf8'))
#		JCON.SendAndCallForResponse(node, handler_stanza_answ,{'type': type, 'source': source})
		JCON.send(node)
		return
	rep = u'ты что посылать собралсо?'
	reply(source, type, rep)
	
#def handler_stanza_answ(coze, res, type, source):
#	if res:
#		reply(source, type, res.getData())
#		return
#	reply(source, type, u'глюк')

register_command_handler(handler_stanza, {1: '!stanza', 2: '!stanza', 3: '!stanza'}, ['суперадмин','все','мук'], 100, 'топка', '!stanza <payload>', ['!stanza aaabbb'])

