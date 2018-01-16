# -*- coding: utf-8 -*-

from conf.dbconfig import TB_MSG
from core.err_code import DB_ERR, OCT_SUCCESS
from core.log import WARNING
from utils.commonUtil import transToObj
from utils.timeUtil import getStrTime, get_current_time

MSG_TYPE_BASIC = "basicInfo"
MSG_TYPE_CPU = "cpuInfo"
MSG_TYPE_MEMORY = "memoryInfo"
MSG_TYPE_DISK = "diskInfo"
MSG_TYPE_NET = "netInfo"


def getMsgCount(db, cond=""):
	return db.rowcount(TB_MSG, cond=cond)


class Msg:
	def __init__(self, db=None, dbObj=None):
		
		self.db = db
		self.dbObj = dbObj
		
		self.type = ""
		self.agentId = ""
		self.msg = {}
		self.time = 0
	
	def loadFromObj(self):
		
		self.type = self.dbObj["M_Type"]
		self.msg = transToObj(self.dbObj["M_Msg"])
		self.agentId = self.dbObj["M_AgentId"]
		self.time = self.dbObj["M_Time"]
		
		return 0
	
	def add(self):
		dbObj = {
			"M_Type": self.type,
			"M_AgentId": self.agentId,
			"M_Msg": self.msg,
			"M_Time": get_current_time()
		}
		
		ret = self.db.insert(TB_MSG, dbObj)
		if (ret == -1):
			WARNING("add msg error for db operation")
			return DB_ERR
		
		return OCT_SUCCESS
	
	def delete(self):
		# cond = "WHERE ID='%s'" % (self.myId)
		# self.db.delete(TB_MSG, cond=cond)
		return 0
	
	def toObj(self):
		obj = {
			"type": self.type,
			"msg": self.msg,
			"agentId": self.agentId,
			"time": getStrTime(self.time)
		}
		
		return obj
