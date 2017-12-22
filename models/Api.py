# -*- coding: utf-8 -*-

from conf.dbconfig import TB_APITRACE
from core.err_code import DB_ERR, OCT_SUCCESS
from core.log import WARNING
from models.Common import DEFAULT_ACCOUNT_ID
from utils.commonUtil import getUuid, transToStr, transToObj, CRC32
from utils.timeUtil import get_current_time, getStrTime

API_STATE_NEW = "New"
API_STATE_RUNNING = "Running"
API_STATE_SERVERRUNNING = "ServerRunning"
API_STATE_FAILED = "Failed"
API_STATE_FINISHED = "Finished"


class Api:
	dbObj = None

	def __init__(self, db=None, myId=None, dbObj=None):

		self.db = db
		self.myId = myId
		self.dbObj = dbObj

		self.user = ""
		self.accountId = ""
		self.apiId = ""
		self.type = "api"
		self.name = ""
		self.request = { }
		self.serverRequest = { }
		self.reply = { }
		self.state = API_STATE_NEW
		self.startTime = 0
		self.finishTime = 0

		if (self.dbObj):
			self.loadFromObj()

	def init(self):

		cond = "WHERE ID='%s' " % (self.myId)

		dbObj = self.db.fetchone(TB_APITRACE, cond)
		if (not dbObj):
			return -1

		self.dbObj = dbObj
		self.loadFromObj()

		return 0

	def add(self):
		
		self.myId = getUuid()
		self.startTime = get_current_time()
		self.finishTime = get_current_time()

		obj = {
			"ID": self.myId,
			"AT_AccountId": self.accountId or DEFAULT_ACCOUNT_ID,
			"AT_ApiId": self.apiId,
			"AT_Type": self.type,
			"AT_Name": self.name,
			"AT_State": self.state,
			"AT_User": self.user or "",
			"AT_Request": transToStr(self.request),
			"AT_ServerRequest": transToStr(self.serverRequest),
			"AT_Reply": transToStr(self.reply),
			"AT_StartTime": get_current_time(),
			"AT_CreateTime": get_current_time(),
		}

		if (self.state == API_STATE_FINISHED or self.state == API_STATE_FAILED):
			obj["AT_FinishTime"] = get_current_time()

		ret = self.db.insert(TB_APITRACE, obj)
		if ret == -1:
			WARNING("add api %s error for db operation" % self.myId)
			return DB_ERR

		return OCT_SUCCESS

	def delete(self):

		cond = "WHERE ID='%s'" % self.myId
		ret = self.db.delete(TB_APITRACE, cond=cond)
		if ret == -1:
			WARNING("delete api %s error for db operation" % self.apiId)
			return DB_ERR

		return 0

	def updateReply(self):

		obj = {
			"AT_Reply": transToStr(self.reply),
			"AT_State": self.state,
			"AT_FinishTime": get_current_time()
		}

		cond = "WHERE ID='%s'" % self.myId
		ret = self.db.update(TB_APITRACE, obj, cond=cond)
		if ret == -1:
			WARNING("update api request %s error for db operation" % self.apiId)
			return DB_ERR

		return 0

	def loadFromObj(self):

		self.myId = self.dbObj["ID"]
		self.accountId = self.dbObj["AT_AccountId"]
		self.state = self.dbObj["AT_State"]
		self.name = self.dbObj["AT_Name"]
		self.type = self.dbObj["AT_Type"]
		self.user = self.dbObj["AT_User"]
		self.apiId = self.dbObj["AT_ApiId"]
		self.request = transToObj(self.dbObj["AT_Request"])
		self.serverRequest = transToObj(self.dbObj["AT_ServerRequest"])
		self.reply = transToObj(self.dbObj["AT_Reply"])
		self.startTime = self.dbObj["AT_StartTime"]
		self.finishTime = self.dbObj["AT_FinishTime"]

		return 0

	def simpleObj(self):
		return {
			"id": self.myId,
			"api": self.apiId,
			"state": self.state,
			"type": self.type,
			"startTime": getStrTime(self.startTime),
		}

	def toObj(self):
		return {
			"id": self.myId,
			"api": self.apiId,
			"state": self.state,
			"type": self.type,
			"user": self.user,
			"name": self.name,
			"request": self.request,
			"reply": self.reply,
			"hashValue": CRC32(self.myId + self.state),
			"serverRequest": self.serverRequest,
			"startTime": getStrTime(self.startTime),
			"finishTime": getStrTime(self.finishTime)
		}
