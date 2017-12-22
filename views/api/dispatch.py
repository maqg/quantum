# -*- coding: utf-8 -*-

from core.err_code import SEGMENT_NOT_EXIST, INVALID_PARAS, PERMISSION_NOT_ENOUGH
from core.log import ERROR
from core.service import callWebServiceDir, callServerWebServiceDir
from modules.api.api_web import web_add_api
from utils.commonUtil import buildRetObj
from utils.httpUtil import checkParas

IGNORE_SESSION_APIS = ["APILoginByAccount", "APILogOut", "APILoginByLdap", "APIEnduserLoginByLdap"]


def writeApi(arg, session, apiProto):
	retObj = callWebServiceDir(web_add_api, session, arg, apiProto)
	retObj["session"] = session
	retObj["apiId"] = retObj["RetObj"]["id"]
	return retObj


def writeServerApi(arg, apiProto):
	retObj = callServerWebServiceDir(web_add_api, arg, apiProto)
	retObj["apiId"] = retObj["RetObj"]["id"]
	return retObj


def checkRoles(paras, apiProto):
	if True:
		return True, None
	
	inRole = paras["role"]
	protoRoles = apiProto.get("roles") or []
	if (not protoRoles or inRole in protoRoles):
		return True, None
	
	return False, "Permission Not Enough"


def doDispatching(arg, session, API_LIST):
	apiProto = API_LIST.get(arg.get("api"))
	if (not apiProto):
		ERROR("func of %s not exist" % arg.get("api"))
		return buildRetObj(SEGMENT_NOT_EXIST)
	
	ret, errorMsg = checkParas(arg.get("paras"), apiProto)
	if (not ret):
		ERROR("check paras error [%s]" % errorMsg)
		return buildRetObj(INVALID_PARAS, errorLog=errorMsg)
	
	ret, errorMsg = checkRoles(arg.get("paras"), apiProto)
	if (not ret):
		ERROR("check roles error [%s]" % errorMsg)
		return buildRetObj(PERMISSION_NOT_ENOUGH, errorLog=errorMsg)
	
	arg["async"] = False  # TBD
	
	if (arg.get("async")):
		return writeApi(arg, session, apiProto)
	else:
		return callWebServiceDir(apiProto["func"], session, arg, apiProto)


def doServerDispatching(arg, API_LIST):
	apiProto = API_LIST.get(arg.get("api"))
	if (not apiProto):
		ERROR("func of %s not exist" % arg.get("api"))
		return buildRetObj(SEGMENT_NOT_EXIST)
	
	ret, errorMsg = checkParas(arg.get("paras"), apiProto)
	if (not ret):
		ERROR("check paras error [%s]" % errorMsg)
		return buildRetObj(INVALID_PARAS, errorLog=errorMsg)
	
	arg["async"] = False  # TBD
	
	if (arg.get("async")):
		return writeServerApi(arg, apiProto)
	else:
		return callServerWebServiceDir(apiProto["func"], arg, apiProto)
