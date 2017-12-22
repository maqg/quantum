#!/usr/bin/python
# -*- coding: utf-8 -*-

from conf.dbconfig import TB_APITRACE
from core import dbmysql
from core.err_code import SEGMENT_NOT_EXIST, OCT_SUCCESS, err_desc_ch
from core.log import ERROR, WARNING
from models.Api import Api, API_STATE_NEW, API_STATE_FINISHED
from models.Common import DEFAULT_ACCOUNT_ID
from utils.commonUtil import CRC32


def getApiCount(db, cond=""):
	return db.rowcount(TB_APITRACE, cond=cond)


def addTask(db, arg, taskParas, state=API_STATE_NEW):

	api = Api(db)
	api.accountId = arg["paras"].get("accountId")
	api.user = arg["env"].get("USERNAME")
	api.state = state
	api.apiId = arg["api"]
	api.type = "task"

	api.name = arg.get("apiName") or ""
	if (taskParas.get("object")):
		api.name = api.name + "[%s]" % str(taskParas.get("object"))

	api.request = taskParas
	ret = api.add()

	return (ret, api.myId)


def addApi(db, arg, taskParas):
	api = Api(db)
	api.accountId = arg["paras"].get("accountId")
	api.user = arg["session"].get("username")
	api.state = API_STATE_NEW
	api.apiId = arg["api"]

	api.name = arg.get("apiName") or ""
	if (taskParas.get("object")):
		api.name = api.name + "[%s]" % str(taskParas.get("object"))

	api.request = arg

	ret = api.add()

	return (ret, api.simpleObj())

def buildApiResult(res):
	errorNo = res["RetCode"]
	return {
		"errorObj": {
			"errorNo": errorNo,
			"errorMsg": err_desc_ch.get(errorNo),
		},
		"data": res["RetObj"]
	}

def addApiResult(db, env, arg, result=None):

	api = Api(db)
	api.accountId = arg["paras"].get("accountId")
	api.user = env["USERNAME"]
	api.state = API_STATE_FINISHED
	api.apiId = arg["api"]
	api.name = arg.get("apiName") or ""
	api.request = arg
	api.reply = buildApiResult(result)

	ret = api.add()

	return (ret, api.simpleObj())


def deleteApi(db, arg):
	apiId = arg["paras"].get("id")
	api = getApi(db, apiId=apiId)
	if (not api):
		WARNING("api %s not exist" % apiId)
		return SEGMENT_NOT_EXIST

	return api.delete()


def updateApiReply(db, apiId, state, reply={}):
	api = getApi(db, apiId=apiId)
	if (not api):
		WARNING("api %s not exist" % apiId)
		return SEGMENT_NOT_EXIST
	
	api.state = state
	api.reply = reply
	return api.updateReply()


def getApis(db, arg):
	listObj = {
		"data": [],
		"total": 0
	}
	cond = "WHERE 1=1 "

	accountId = arg["paras"].get("accountId")
	start = arg["paras"].get("start") or 0
	limit = arg["paras"].get("limit") or 10
	keyword = arg["paras"].get("keyword") or ""
	type = arg["paras"].get("type")
	apiName = arg["paras"].get("apiName")
	serverTaskId = arg["paras"].get("serverTaskId")

	if (accountId and accountId != DEFAULT_ACCOUNT_ID):
		cond += "AND AT_AccountId='%s' " % (accountId)

	if (type):
		cond += "AND AT_Type='%s' " % type

	if (apiName):
		cond += "AND AT_Name LIKE '%%%s%%' " % (apiName)

	if (keyword):
		cond += "AND AT_ApiId LIKE '%%%s%%' " % (keyword)

	if (serverTaskId):
		cond += "AND AT_ServerTaskId='%s' " % serverTaskId

	cond += "ORDER BY AT_StartTime DESC"

	ret = db.select(TB_APITRACE, cond=cond, limit=int(limit), offset=int(start))
	if ret == -1:
		ERROR("get modules list error")
		return (OCT_SUCCESS, listObj)

	hashStr = ""
	for dur in db.cur:
		obj = dbmysql.row_to_dict(TB_APITRACE, dur)
		api = Api(db, dbObj=obj)
		api.loadFromObj()
		obj = api.toObj()
		hashStr += api.myId
		hashStr += api.state
		listObj["data"].append(obj)

	listObj["total"] = getApiCount(db, cond=cond)
	listObj["hashValue"] = CRC32(hashStr)

	return (OCT_SUCCESS, listObj)


def getApi(db, apiId=None, apiName=None, submoduleId=None):
	if (not apiId):
		return None

	cond = "WHERE ID='%s'" % (apiId)

	dbObj = db.fetchone(TB_APITRACE, cond=cond)
	if (not dbObj):
		WARNING("module %s not exist" % cond)
		return None

	api = Api(db, dbObj=dbObj)
	api.loadFromObj()

	return api
