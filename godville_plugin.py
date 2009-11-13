#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  godville_plugin.py
#  exclusively for godville.net ;)

#  Initial Copyright © Als <als-als@ya.ru>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

from xml.dom.minidom import parse as xmlparse

def handler_godville_hero(type, source, parameters):
	if not parameters:
		reply(type,source,u'ииии?')
		return
	hero=urllib2.quote(parameters.encode('utf8'))
	try:
		req=urllib2.urlopen('http://www.godville.net/gods/api/%s.xml' % hero)
	except urllib2.HTTPError, e:
		if e.code==404:
			reply(type,source,u'кто это?')
			return
		else:
			reply(type,source,str(e))
			return
	hero_xml_info=xmlparse(req)
	hero_info=get_hero_info(hero_xml_info)
	rep=u'%(hname)s - геро%(hgender)s, находящ%(gend1)s под неусыпным надзором бог%(ggender)s %(gname)s, заряженн%(gend2)s на %(prana)d%% праны. %(guild)s с девизом "%(motto)s". Имеет %(level)d уровень и %(nextlvl).2f%% до следующего. Также припас%(gend3)s себе %(invn)d вещичек (из %(invm)d max), здоров%(gend4)s на %(health)d%%. Прош%(gend5)s свой текущий квест на %(quest)d%%' % hero_info
	reply(type,source,rep)

def get_hero_info(raw_info):
	info={}
	info['hname']=get_hero_data(raw_info.getElementsByTagName("name")[0])
	info['hgender']=get_hero_gender(raw_info.getElementsByTagName("gender")[0])
	info['ggender']=get_hero_god_gender(raw_info.getElementsByTagName("gender")[0])
	info['gname']=get_hero_data(raw_info.getElementsByTagName("godname")[0])
	info['prana']=int(get_hero_data(raw_info.getElementsByTagName("godpower")[0]))
	info['guild']=get_hero_data(raw_info.getElementsByTagName("clan")[0])
	info['motto']=get_hero_data(raw_info.getElementsByTagName("motto")[0])
	info['level']=int(get_hero_data(raw_info.getElementsByTagName("level")[0]))
	info['nextlvl']=100-float(get_hero_data(raw_info.getElementsByTagName("exp_progress")[0]))
	info['invn']=int(get_hero_data(raw_info.getElementsByTagName("inventory_num")[0]))
	info['invm']=int(get_hero_data(raw_info.getElementsByTagName("inventory_max_num")[0]))
	info['health']=get_hero_health(raw_info)
	info['quest']=int(get_hero_data(raw_info.getElementsByTagName("quest_progress")[0]))
	info.update(get_more_gender(raw_info.getElementsByTagName("gender")[0]))
	if info['guild']:
		info['guild']=u'Состоит в гильдии "%s"' % info['guild']
	else:
		info['guild']=u'Не состоит в гильдиях'
	return info

def get_gender(gender):
	gender=gender.firstChild.data
	if gender=='male':	return True
	else:	return False

def get_hero_gender(gender):
	gender=get_gender(gender)
	if gender:	return u'й'
	else:	return u'иня'

def get_hero_god_gender(gender):
	gender=get_gender(gender)
	if gender:	return u'а'
	else:	return u'ини'

def get_hero_data(info):
	info=info.firstChild
	if info:
		return info.data

def get_hero_health(info):
	maxh=int(get_hero_data(info.getElementsByTagName("max_health")[0]))
	curh=int(get_hero_data(info.getElementsByTagName("health")[0]))
	perc=curh*100/maxh
	return perc

def get_more_gender(gender):
	if get_gender(gender):
		return {'gend1': u'ийся', 'gend2': u'ый', 'gend3': u'', 'gend4': u'', 'gend5': u'ёл'}
	else:
		return {'gend1': u'аяся', 'gend2': u'ая', 'gend3': u'ла', 'gend4': u'а', 'gend5': u'ла'}

register_command_handler(handler_godville_hero, 'hero', ['фан','мук','все','эксклюзив'], 10, 'Подсматривает инфу о герое на http://godville.net/.\nНе забывайте, что оно "отражает актуальную информацию только в течение часа после посещения страницы героя"!!!', 'hero <ник>', ['hero Godville'])
