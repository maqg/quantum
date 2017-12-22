# -*- coding: utf-8 -*-

import traceback

import base64
import struct
from core import dbmysql

from core.err_code import SYSTEM_ERR, err_desc_en
from core.log import ERROR,DEBUG
from modules.api.api_web import web_add_apiresult

def server_web_get_env():
	env = {}
	return env

def web_get_env(session):
	env = {
		"USERNAME": session.get("user"),
		"SESSIONID": session.get("id"),
	}

	if (session.get("cookie")):
		env["ROLE"] = session["cookie"].get("role")
		env["USERID"] = session["cookie"].get("id")

	return env


def makeFunctionResult(funret):
	RetCode = funret.get('RetCode')
	if type(RetCode) != int:
		errorLog = "Wrong formatstr in function return data ret[%s]" % (funret)
		ERROR(errorLog)
		return buildResult(SYSTEM_ERR, errorLog=errorLog)

	return buildResult(RetCode, funret.get("RetObj"), funret.get("ErrorLog"))


def writeApiWithResult(db, env, arg, result, apiProto, server=False):

	if arg["api"].split(".")[3] == "task":
		return result

	if (apiProto.get("isTask")):
		result["apiId"] = result["RetObj"]
	else:
		retObj = web_add_apiresult(db, env, arg, result)

		result["apiId"] = retObj["RetObj"]["id"]

	return result


def callWebServiceEX(*args):

	function = args[-4]
	session = args[-3]
	arg = args[-2]
	apiProto = args[-1]

	if (apiProto):
		arg["apiName"] = apiProto["name"]

	env = web_get_env(session)
	arg["env"] = env
	db = dbmysql.mysqldb()

	try:
		funret = function(db, env, arg)
	except Exception as e:
		errorLog = "Error in %s: [%s],\n Import module failed. [%s]" % (function, e, traceback.format_exc(limit=100))
		errorLog = errorLog.replace("\n", "")
		errorLog = errorLog.replace("\"", "\\\"")
		ERROR(errorLog)

		retObj = buildResult(SYSTEM_ERR, errorLog=errorLog)
		if (arg.get("async") != True):
			retObj = writeApiWithResult(db, env, arg, retObj, apiProto, False)
			retObj["session"] = session

		del db, env
		return retObj

	retObj = makeFunctionResult(funret)
	if (arg.get("async") != True):
		retObj = writeApiWithResult(db, env, arg, retObj, apiProto, False)
		retObj["session"] = session
	del db, env

	return retObj

def callServerWebServiceEX(*args):
	function = args[-3]
	arg = args[-2]
	apiProto = args[-1]

	if (apiProto):
		arg["apiName"] = apiProto["name"]

	env = server_web_get_env()
	db = dbmysql.mysqldb()

	try:
		funret = function(db, env, arg)
	except Exception as e:
		errorLog = "Error in %s: [%s],\n Import module failed. [%s]" % (function, e, traceback.format_exc(limit=100))
		errorLog = errorLog.replace("\n", "")
		errorLog = errorLog.replace("\"", "\\\"")
		ERROR(errorLog)

		retObj = buildResult(SYSTEM_ERR, errorLog=errorLog)
		if (arg.get("async") != True):
			retObj = writeApiWithResult(db, env, arg, retObj, apiProto, True)

		del db, env
		return retObj

	retObj = makeFunctionResult(funret)
	if (arg.get("async") != True):
		retObj = writeApiWithResult(db, env, arg, retObj, apiProto, True)
	del db, env

	return retObj

def buildResult(RetCode, data=None, errorLog=""):
	return {
		"RetObj": data,
		"RetCode": RetCode,
		"ErrorLog": errorLog
	}


def callWebServiceDir(function, session, args, apiProto):
	return callWebServiceEX(function, session, args, apiProto)


def callServerWebServiceDir(function, args, apiProto):
	return callServerWebServiceEX(function, args, apiProto)

def tsh_get_env(arg):
	env = {}
	newarg = base64.b64decode(arg) 
	envList = struct.unpack('bbbxhbb16s253sx', newarg)
	env['pri'] = envList[1]
	env['opflg'] = envList[2]
	env['modid'] = envList[3]
	env['lang'] = envList[4]
	env['node'] = envList[5]
	env['modname'] = envList[6].decode('utf-8').strip('\x00')
	env['__USER_NAME__'] = envList[7].decode('utf-8').strip('\x00')

	return env

def handleTshService(s_name, env, arg):

	calllist = s_name.split('.')
	modulepath = calllist[:-1]
	funname = calllist[-1]

	db = dbmysql.mysqldb()

	DEBUG("Function name %s" % funname)

	try:
		service = __import__('modules'+'.'+'.'.join(modulepath), fromlist=['from modules import',])
	except Exception as e:
		ERROR('Import module failed. [%s]' % s_name)
		ERROR('Import module failed. [%s]' % e)
		ERROR('Import module failed. [%s]' % traceback.format_exc())
		del db, env
		return buildResult(SYSTEM_ERR)

	if hasattr(service, funname):
		funobj = getattr(service, funname)
	else:
		ERROR('There is no %s in %s' % (funname, modulepath))
		del db, env, service
		return buildResult(SYSTEM_ERR)

	del service

	try:
		funret = funobj(db, env, arg)
		DEBUG(funret)
	except Exception as arg:
		ERROR('Error in %s: [%s]' % (s_name, arg))
		ERROR('Import module failed. [%s]' % traceback.format_exc())
		del funobj, db, env
		return buildResult(SYSTEM_ERR)

	del funobj, db, env

	RetCode = funret.get('RetCode')
	if type(RetCode) != int:
		ERROR('Wrong formatstr in function return data %s: [%s],ret[%s]' % (s_name, arg, funret))
		return buildResult(SYSTEM_ERR)
	
	retObj = buildResult(RetCode, funret.get('RetObj'))
	retObj["RetMsg"] = err_desc_en.get(RetCode, '')

	return retObj


def tsh_call(ns_name, args):
	args = list(args)
#	env = tsh_get_env(args[1])
	env = tsh_get_env(args[1].encode(encoding="utf-8"))
	return handleTshService(ns_name, env, args)
