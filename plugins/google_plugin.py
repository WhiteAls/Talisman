#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  google_plugin.py

#  Initial Copyright © 2009 Als <Als@admin.ru.net>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

google_results={}

def google_cache_results(gch, results):
	if gch in google_results:
		google_results[gch]=results
	else:
		google_results[gch]=gch
		google_results[gch]=results

def google_remove_html(text):
	nobold = text.replace('<b>', '').replace('</b>', '')
	nobreaks = nobold.replace('<br>', ' ')
	noescape = nobreaks.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
	return noescape

def google_get_results(results, first):
	if first:
		titleNoFormatting=results[0]['titleNoFormatting']
		content=results[0]['content']
		url=results[0]['unescapedUrl']
		return titleNoFormatting+u'\n'+content+u'\n'+url
	else:
		temp=[]
		for result in xrange(1,len(results)):
			if result<4:
				titleNoFormatting=results[result]['titleNoFormatting']
				content=results[result]['content']
				url=results[result]['unescapedUrl']
				temp.append(str(result)+u': '+titleNoFormatting+u'\n'+content+u'\n'+url)
		return u'\n\n'.join(temp)

def google_search(query, gch):
	if query=='+':
		if gch in google_results:
			return google_remove_html(google_get_results(google_results[gch], 0))
	try:
		req = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s' % urllib2.quote(query.encode('utf-8')))
	except urllib2.HTTPError, e:
		return str(e)
	answ=json.load(req)
	if answ['responseStatus']!=200:
		return str(answ['responseStatus'])+': '+answ['responseDetails']
	elif answ['responseData']:
		results=answ['responseData']['results']
		if results:
			google_cache_results(gch, results)
			return google_remove_html(google_get_results(results, 1))
	else:
		return u'неизвестная ошибка'


def handler_google_google(type, source, parameters):
	results = google_search(parameters, source[1])
	if results:
		reply(type, source, results)
	else:
		reply(type, source, u'ничего не найдено')

try:
	import json
	register_command_handler(handler_google_google, 'гугль', ['инфо','все'], 10, 'Поискать с помощью Google. Для отображения трёх ответов по предыдущему запросу, используйте знак "+" в качестве запроса.', 'гугль <запрос>', ['гугль что-то','гугль +'])
except ImportError:
	try:
		import simplejson as json
		register_command_handler(handler_google_google, 'гугль', ['инфо','все'], 10, 'Поискать с помощью Google. Для отображения трёх ответов по предыдущему запросу, используйте знак "+" в качестве запроса.', 'гугль <запрос>', ['гугль что-то','гугль +'])
	except:
		print '====================================================\nYou need Python 2.6.x or simple_json package installed to use google_plugin.py!!!\n====================================================\n'
