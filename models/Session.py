# -*- coding: utf-8 -*-

from conf.dbconfig import TB_SESSION
from core.err_code import DB_ERR, OCT_SUCCESS
from core.log import WARNING,DEBUG
from utils.commonUtil import getUuid, transToStr, transToObj
from utils.timeUtil import get_current_time, getStrTime

SESSION_EXPIRE_TIME = 86400 * 30 * 1000  # one month


class Session:
	db = None
	username = ""
	myId = 0

	cookie = { }

	createTime = 0
	expireTime = 0

	dbObj = None

	def __init__(self, db=None, myId=None, dbObj=None):

		self.db = db
		self.myId = myId
		self.userId = ""
		self.username = ""
		self.role = 3

		self.dbObj = dbObj

		if (self.dbObj):
			self.loadFromObj()

	def init(self):

		cond = "WHERE ID='%s' AND S_ExpireTime > %ld " % (self.myId, get_current_time())

		dbObj = self.db.fetchone(TB_SESSION, cond)
		if (not dbObj):
			return -1

		self.dbObj = dbObj
		self.loadFromObj()

		return 0

	def add(self):

		self.myId = getUuid()
		self.createTime = get_current_time()
		self.expireTime = get_current_time() + SESSION_EXPIRE_TIME

		obj = {
			"ID": self.myId,
			"S_UserId": self.userId,
			"S_UserName": self.username,
			"S_UserType": self.role,
			"S_Cookie": transToStr(self.cookie),
			"S_CreateTime": self.createTime,
			"S_ExpireTime": self.expireTime,
		}

		ret = self.db.insert(TB_SESSION, obj)
		if ret == -1:
			WARNING("add session %s error for db operation" % self.myId)
			return DB_ERR

		return OCT_SUCCESS

	def delete(self):

		cond = "WHERE ID='%s'" % self.myId

		DEBUG("to delete session %s" % (self.myId))

		ret = self.db.delete(TB_SESSION, cond=cond)
		if ret == -1:
			WARNING("delete session %s error for db operation" % self.myId)
			return DB_ERR

		return 0

	def update(self):

		obj = {
			"S_ExpireTime": get_current_time() + SESSION_EXPIRE_TIME,
		}

		cond = "WHERE ID='%s'" % self.myId
		ret = self.db.update(TB_SESSION, obj, cond=cond)
		if ret == -1:
			WARNING("update session %s error for db operation" % self.myId)
			return DB_ERR

		return 0

	def loadFromObj(self):

		self.myId = self.dbObj["ID"]
		self.username = self.dbObj["S_UserName"]
		self.role = self.dbObj["S_UserType"]
		self.userId = self.dbObj["S_UserId"]
		self.cookie = transToObj(self.dbObj["S_Cookie"])
		self.createTime = self.dbObj["S_CreateTime"]
		self.expireTime = self.dbObj["S_ExpireTime"]

		return 0

	def toObj(self):

		return {
			"id": self.myId,
			"user": self.username,
			"userId": self.userId,
			"userRole":self.role,
			"cookie": self.cookie,
			"creatTime": getStrTime(self.createTime),
			"expireTime": getStrTime(self.expireTime)
		}
