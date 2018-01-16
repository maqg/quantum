#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from core.err_code import err_desc_ch, OCT_SUCCESS, err_desc_en
from core.log import ERROR
from views.api.api import PARAM_NOT_NULL, PARAM_TYPE_INT


def appendBaseArg(argObj, request):
	if (not argObj):
		argObj = {}

	argObj["LAST_ADDR"] = request.remote_ip
	argObj["REMOTE_ADDR"] = request.headers.get("X-Real-Ip") or argObj["LAST_ADDR"]

	if ("paras" not in argObj.keys()):
		argObj["paras"] = {}

	return argObj


def getArgObj(request):
	argObj = {}
	arg = str(request.body, encoding="utf-8")

	if (len(arg) == 0 or arg[:1] not in ("{", "]")):
		return appendBaseArg(argObj, request)

	try:
		if (type(arg) != type("a")):
			arg = arg.encode("utf-8")
		argObj = json.loads(arg)

	except:
		ERROR("got bad json request")

	return appendBaseArg(argObj, request)


def buildFailureReply(errorNo, errorMsg=None):
	retObj = {
		"errorObj": {
			"errorNo": errorNo,
			"errorMsg": errorMsg or err_desc_ch.get(errorNo),
			"errorMsgEN": err_desc_en.get(errorNo),
		},
		"data": None
	}
	return json.JSONEncoder().encode(retObj)


def buildAsyncReply(res):
	data = res["RetObj"]
	errorNo = res["RetCode"]

	retObj = {
		"errorObj": {
			"errorNo": errorNo,
			"errorMsg": res.get("RetMsg") or err_desc_ch.get(errorNo),
			"errorMsgEN": err_desc_en.get(errorNo),
		},
		"session": {
			"uuid": res["session"]["id"],
		},
		"createTime": data["createTime"],
		"finishTime": data["finishTime"],
		"apiId": data["id"],
		"apiName": data["apiName"],
		"state": data["state"],
		"result": data["result"]
	}

	return json.JSONEncoder().encode(retObj)


# if param has no default value, it must be specified,
# or else set default value to it.
def checkParas(paras, apiProto):
	for (k, v) in list(apiProto["paras"].items()):

		if (v["default"] != PARAM_NOT_NULL and k not in paras):
			paras[k] = v["default"]

		inV = paras.get(k)
		if (v["default"] == PARAM_NOT_NULL and not inV):
			errorMsg = "paras '%s' must be specified" % k
			return False, errorMsg

		if (v["type"] == PARAM_TYPE_INT and v["type"]):
			if not paras[k]:
				paras[k] = 0
			paras[k] = int(paras[k])

	return True, None

def buildReply(res):
	errorNo = res["RetCode"]

	retObj = {
		"errorObj": {
			"errorNo": errorNo,
			"errorMsg": res.get("RetMsg") or err_desc_ch.get(errorNo),
			"errorMsgEN": err_desc_en.get(errorNo),
			"errorLog": res["ErrorLog"]
		},
		"data": res["RetObj"],
		"apiId": res.get("apiId")
	}

	if (errorNo == OCT_SUCCESS):

		if (res.get("session")):
			retObj["session"] = {
				"uuid": res["session"].get("id")
			}

	return json.JSONEncoder().encode(retObj)
