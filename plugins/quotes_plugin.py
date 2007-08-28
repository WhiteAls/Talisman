#===istalismanplugin===
# -*- coding: utf-8 -*-
####### It is translated and modified by Als #######

import urllib2,re,urllib

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')

def handler_bashorg_get(type, source, parameters):
    if parameters.strip():
        req = urllib2.Request('http://bash.org/?'+parameters.strip())
    else:
        req = urllib2.Request('http://bash.org/?random')
    req.add_header = ('User-agent', 'Mozilla/5.0')
    r = urllib2.urlopen(req)
    target = r.read()
    od = re.search('<p class="qt">',target)
    message = target[od.end():]
    message = message[:re.search('</p>',message).start()]
    message = decode(message)
    message='\n' + message.strip()
    reply(type,source,unicode(message,'windows-1251'))

def handler_bashorgru_get(type, source, parameters):
	if parameters.strip()=='':
		req = urllib2.Request('http://bash.org.ru/random')
	else:
		req = urllib2.Request('http://bash.org.ru/quote/'+parameters.strip())
		req.add_header = ('User-agent', 'Mozilla/5.0')
	try:
		r = urllib2.urlopen(req)
		target = r.read()
		"""link to the quote"""
		od = re.search('<div class="vote">',target)
		b1 = target[od.end():]
		b1 = b1[:re.search('</a>',b1).start()]
		b1 = strip_tags.sub('', b1.replace('\n', ''))
		b1 = 'http://bash.org.ru/quote/'+b1+'\n'
		"""quote"""
		od = re.search('bayan"',target)
		b2 = target[od.end():]
		b2 = b2[:re.search('<div class="q">',b2).start()]
		message = b1+b2
		message = decode(message)
		message = '\n' + message.strip()
		reply(type,source,unicode(message,'windows-1251'))#.decode('utf-8')
	except:
		reply(type,source,u'очевидно, они опять сменили разметку')
        
        
def handler_bashorgru_abyss_get(type, source, parameters):
    if parameters.strip()=='':
        req = urllib2.Request('http://bash.org.ru/abyss')
    else:
        reply(type,source,u'извиняй, с номерами бездна не дружит :(')
        return
    req.add_header = ('User-agent', 'Mozilla/5.0')
    try:
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('bayan"',target)
        message = target[od.end():]
        message = message[:re.search('<hr class="iq">',message).start()]
        message = decode(message)
        message = '\n' + message.strip()
        reply(type,source,unicode(message,'windows-1251'))
    except:
        reply(type,source,u'аблом какой-то')        

def handler_linuxorgru_get(type, source, parameters):
    req = urllib2.Request('http://linux.org.ru/index.jsp')
    req.add_header = ('User-agent', 'Mozilla/5.0')
    r = urllib2.urlopen(req)
    target = r.read()
    od = re.search('<hr noshade class="news-divider">',target)
    message = target[od.end():]
    message = message[:re.search('<div class=sign>',message).start()]
    message = decode(message)
    message = '\n' + message.strip()
    reply(type,source,unicode(message,'koi8-r'))

#=======
def handler_linuxorgru_get(type, source, parameters):
    req = urllib2.Request('http://linux.org.ru/index.jsp')
    req.add_header = ('User-agent', 'Mozilla/5.0')
    r = urllib2.urlopen(req)
    target = r.read()
    od = re.search('<hr noshade class="news-divider">',target)
    message = target[od.end():]
    message = message[:re.search('<hr noshade class="news-divider">',message).start()]
    message = decode(message)
    message = '\n' + message.strip()
    reply(type, source, unicode(message, 'koi8-r'))

def decode(text):
    return strip_tags.sub('', text.replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')

register_command_handler(handler_bashorgru_get, 'бор', ['фан','инфо','все'], 0, 'Показывает случайную цитату из бора (bash.org.ru). Также может по заданному номеру вывести.', 'бор', ['бор 223344','бор'])
register_command_handler(handler_bashorgru_abyss_get, 'борб', ['фан','инфо','все'], 0, 'Показывает случпйную цитату из бездны бора (bash.org.ru).', 'борб', ['борб'])
register_command_handler(handler_linuxorgru_get, 'лор', ['фан','инфо','все'], 0, 'Показывает  последнюю новость с лора (linux.org.ru). Параметры игнорируются.', 'лор', ['лор'])
register_command_handler(handler_bashorg_get, 'бо', ['фан','инфо','все'], 0, 'Показывает случайную цитату из бора (bash.org). Также может по заданному номеру вывести.', 'бо', ['бо','бо 123456'])
