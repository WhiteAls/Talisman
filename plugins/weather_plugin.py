#===istalismanplugin===
# -*- coding: utf-8 -*-
####### It is translated by Als #######

import pymetar

WEATHERCODE_FILE = 'static/weather.txt'

def handler_weather_weather(type, source, parameters):
	if not parameters:
		reply(type, source, u'чё-то ты не то написал...')
		return
	info = pymetar.MetarReport(str(parameters).strip())
	try:
		location = info.getStationName()
		celsius = str(round(info.getTemperatureCelsius(), 1))
		fahrenheit = str(round(info.getTemperatureFahrenheit(), 1))
		#humidity = str(round(info.getHumidity(), 1))
		results = location + ' - ' + str(info.getWeather()) + ' -- ' + celsius + 'Ц -- ' + fahrenheit + 'Ф' # + ' - ' + humidity + '% Humdity'
	except Exception, ex:
		results = u'моя твоя не понимай :)'
		print ex.__str__
	reply(type, source, results)

def handler_weather_weathercode(type, source, parameters):
	if not parameters:
		reply(type, source, u'чё-то ты не то написал...')
		return
	if len(parameters)<=2:
		reply(type, source, u'какая-то фигня...')
		return
	results = ''
	query = string.lower(parameters)
	fp = open(WEATHERCODE_FILE, 'r')
	lines = fp.readlines()
	for line in lines:
		if string.count(string.lower(line), query):
			results += string.split(line, '=> ')[0]
	if results:
		reply(type, source, results)
	else:
		reply(type, source, u'хз')

register_command_handler(handler_weather_weather, 'погода', ['инфо','все'], 10, 'Смотрит погоду из NOAA', 'погодп <4буквенный_код_города>', ['погода ukhh'])
register_command_handler(handler_weather_weathercode, 'код', ['инфо','все'], 10, 'Показывает код города для просмотра погоды', 'код <город>', ['код orel'])
