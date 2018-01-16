# -*- coding: utf-8 -*-

from conf.dbconfig import TB_AGENT
from core.log import WARNING
from utils.timeUtil import howLongAgo, getStrTime


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
		
		self.hostname = ""
		self.status = ""
		self.address = ""
		
		self.lastSync = 0
		self.createTime = 0
		
		self.desc = ""
	
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
		self.hostname = self.dbObj["U_HostName"]
		self.lastSync = self.dbObj["U_LastSync"]
		self.createTime = self.dbObj["U_CreateTime"]
		self.desc = self.dbObj["U_Description"]
		
		return 0
	
	def toObj(self):
		account = {
			"id": self.myId,
			"lastSync": getStrTime(self.lastSync),
			"createTime": getStrTime(self.createTime),
			"desc": self.desc,
		}
		
		return account
	
	def toObjBrief(self):
		
		return {
			"id": self.myId,
			"name": self.hostname,
		}
