#===istalismanplugin===
# -*- coding: utf-8 -*-
####### It is translated by Als #######

def handler_temperature_temperature(type, source, parameters):
	if parameters:
		splitdata = string.split(parameters)
		try:
			input_value = float(splitdata[0])
			if len(splitdata) > 1:
				unit_system = splitdata[1][0]
			else:
				unit_system = 'f'
		except ValueError:
			try:
				input_value = float(splitdata[0][:-1])
			except ValueError:
				reply(type, source, u'чё-то ты не то написал...')
				return
			unit_system = splitdata[0][-1]
		unit_system = string.lower(unit_system)
		if unit_system == 'c':
			rep = str(round(input_value * 9 / 5 + 32, 1)) + ' F'
		else:
			rep = str(round((input_value - 32) * 5 / 9, 1)) + ' C'
	else:
		rep = u'на, переводи сам, раз хелпы юзать не хочешь :D\nC=(F-32)*5/9 F=C*9/5+32'
	reply(type, source, rep)

register_command_handler(handler_temperature_temperature, 'температура', ['фан','инфо','все'], 10, 'Конвертирует температуру из Целий в Фаренгейты и наоборот', 'температура <#> <C/F>', ['температура 10 F', 'температура 29 C'])
