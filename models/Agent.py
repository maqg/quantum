# -*- coding: utf-8 -*-

from conf.dbconfig import TB_AGENT
from core.err_code import DB_ERR, OCT_SUCCESS
from core.log import WARNING, DEBUG, ERROR
from utils.commonUtil import getUuid
from utils.timeUtil import getStrTime, get_current_time


def getAgentCount(db):
	return db.rowcount(TB_AGENT, cond="")


def getAgent(db, agentId):
	cond = "WHERE ID='%s'" % (agentId)
	
	dbObj = db.fetchone(TB_AGENT, cond=cond)
	if (not dbObj):
		WARNING("agent %s not exist" % cond)
		return None
	
	agent = Agent(db, dbObj=dbObj)
	agent.loadFromObj()
	
	return agent


class Agent:
	agents = {}
	
	def __init__(self, db=None, myId=None, dbObj=None):
		
		self.db = db
		self.myId = myId
		self.dbObj = dbObj
		
		self.name = ""
		self.hostname = ""
		self.status = ""
		self.address = ""
		
		self.lastSync = 0
		self.createTime = 0
	
	def init(self):
		cond = "WHERE ID='%s' " % (self.myId)
		dbObj = self.db.fetchone(TB_AGENT, cond)
		if (not dbObj):
			return -1
		
		self.dbObj = dbObj
		self.loadFromObj()
		
		return 0
	
	def loadFromObj(self):
		
		self.myId = self.dbObj["ID"]
		self.name = self.dbObj["A_Name"]
		self.address = self.dbObj["A_Address"]
		self.hostname = self.dbObj["A_HostName"]
		self.lastSync = self.dbObj["A_LastSync"]
		self.createTime = self.dbObj["A_CreateTime"]
		
		return 0
	
	def add(self):
		self.myId = getUuid()
		dbObj = {
			"ID": self.myId,
			"A_Name": self.name,
			"A_Address": self.address,
			"U_CreateTime": get_current_time(),
			"U_LastSync": get_current_time(),
		}
		
		ret = self.db.insert(TB_AGENT, dbObj)
		if (ret == -1):
			WARNING("add agent %s error for db operation" % self.name)
			return DB_ERR
		
		DEBUG(dbObj)
		
		return OCT_SUCCESS
	
	def delete(self):
		cond = "WHERE ID='%s'" % (self.myId)
		self.db.delete(TB_AGENT, cond=cond)
		return 0
	
	def toObj(self):
		account = {
			"id": self.myId,
			"name": self.name,
			"address": self.address,
			"hostname": self.hostname,
			"lastSync": getStrTime(self.lastSync),
			"createTime": getStrTime(self.createTime),
		}
		
		return account
	
	def toObjBrief(self):
		
		return {
			"id": self.myId,
			"name": self.name,
		}
