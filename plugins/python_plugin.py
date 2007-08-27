#===istalismanplugin===
# -*- coding: utf-8 -*-
####### It is translated by Als #######


def handler_python_eval(type, source, parameters):
	try:
		return_value = str(eval(parameters))
	except:
		return_value = str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
	reply(type, source, return_value)

def handler_python_exec(type, source, parameters):
	if '\n' in parameters and parameters[-1] != '\n':
		parameters += '\n'
	try:
		exec parameters in globals()
		return_value = u'получилось'
	except:
		return_value = str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
	reply(type, source, return_value)

def handler_python_sh(type, source, parameters):
	pipe = os.popen('sh -c ' + parameters)
	#time.sleep(0.5)
	return_value = pipe.read(1024)
	reply(type, source, return_value)
	
def handler_python_calc(type, source, parameters):
	parameters = parameters.strip()
	if re.sub('([' + string.digits +']|[\+\-\/\*\^\.])','',parameters).strip() == '':
	    try:
    		return_value = str(eval(parameters))
		time.sleep(1)
	    except:
		return_value = u'научи меня это делать :)'#str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
	else:
		return_value = u'ты глюк'
	reply(type, source, return_value)

register_command_handler(handler_python_eval, {1: 'eval', 2: 'eval', 3: '!eval'}, ['суперадмин','все'], 100, 'Расчитывает и показывает заданное выражение питона.', 'eval <выражение>', ['eval 1+1'])
register_command_handler(handler_python_exec, {1: 'exec', 2: 'exec', 3: '!exec'}, ['суперадмин','все'], 100, 'Выполняет выражение питона.', 'exec <выражение>', ['eval pass'])
register_command_handler(handler_python_sh, {1: 'sh', 2: 'sh', 3: '!sh'}, ['суперадмин','все'], 100, 'Выполняет шелл команду.', 'sh <команда>', ['sh ls'])
register_command_handler(handler_python_calc, {1: 'калк', 2: 'calcul', 3: '!calc'}, ['инфо','все'], 10, 'Калькулятор.', 'calcul <выражение>', ['calcul 1+2'])
