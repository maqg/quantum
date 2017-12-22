# -*- coding: utf-8 -*-

from hashlib import md5 as MD5

from conf.dbconfig import TB_ACCOUNT
from core.err_code import DB_ERR, OCT_SUCCESS, NOT_ENOUGH_PARAS, USER_PASSWD_ERR
from core.log import DEBUG, ERROR, WARNING
from utils.commonUtil import getUuid
from utils.timeUtil import get_current_time, howLongAgo, getStrTime

ROLE_SUPERADMIN = 7
ROLE_ADMIN = 3
ROLE_AUDIT = 1
ROLE_TERMINALUSER = 0
ROLE_CLASSADMIN = 11
ROLE_CLASSTEACHER = 12

roleMap = {
	ROLE_SUPERADMIN: "超级管理员",
	ROLE_ADMIN: "管理员",
	ROLE_AUDIT: "审计员",
	ROLE_TERMINALUSER: "用户"
}

ROLE_ALL = [
	ROLE_SUPERADMIN,
	ROLE_ADMIN,
	ROLE_AUDIT,
	ROLE_TERMINALUSER,
	ROLE_CLASSADMIN,
	ROLE_CLASSTEACHER
]


def getEncPass(str):
	m = MD5()
	m.update("Octopus".encode())
	m.update(str.encode())
	m.update("Link".encode())
	return m.hexdigest()


def getAccountCount(db):
	return db.rowcount(TB_ACCOUNT, cond="")


def getAccount(db, userId=None, userName=None, uid=None):
	if (not userId and not userName and not uid):
		return None
	
	if (userId):
		cond = "WHERE ID='%s'" % (userId)
	elif userName:
		cond = "WHERE U_Name='%s'" % (userName)
	else:
		cond = "WHERE U_LdapUid='%s'" % (uid)
	
	dbObj = db.fetchone(TB_ACCOUNT, cond=cond)
	if (not dbObj):
		WARNING("user %s not exist" % cond)
		return None
	
	user = Account(db, dbObj=dbObj)
	user.loadFromObj()
	
	return user


def userState_d2s(state):
	stateList = ["禁用", "正常"]
	if (state > len(stateList) - 1):
		return "未知"
	else:
		return stateList[int(state)]


def userRole_d2s(role):
	return roleMap.get(role) or "None"


class Account:
	def __init__(self, db=None, uid=None, name=None, dbObj=None):
		
		self.db = db
		self.myId = uid
		self.name = name
		self.dbObj = dbObj
		
		self.role = 0
		self.email = ""
		self.password = ""
		self.phone = ""
		self.state = 1
		self.stateCN = ""
		self.roleCN = ""
		
		self.lastLogin = 0
		self.lastSync = 0
		self.createTime = 0
		
		self.desc = ""
		
		self.ukey = ""
		self.ldapUid = ""
	
	def init(self):
		
		if (self.myId != 0):
			cond = "WHERE ID='%s' " % (self.myId)
		else:
			cond = "WHERE U_Name='%s' " % (self.name)
		
		dbObj = self.db.fetchone(TB_ACCOUNT, cond)
		if (not dbObj):
			return -1
		
		self.dbObj = dbObj
		
		self.loadFromObj()
		
		return 0
	
	def loadFromObj(self):
		
		self.myId = self.dbObj["ID"]
		self.name = self.dbObj["U_Name"]
		self.email = self.dbObj["U_Email"]
		self.phone = self.dbObj["U_PhoneNumber"]
		self.password = self.dbObj["U_Password"]
		self.state = self.dbObj["U_State"]
		self.stateCN = userState_d2s(self.dbObj["U_State"])
		self.role = self.dbObj["U_Type"]
		self.roleCN = userRole_d2s(self.dbObj["U_Type"])
		self.lastLogin = self.dbObj["U_LastLogin"]
		self.lastSync = self.dbObj["U_LastSync"]
		self.createTime = self.dbObj["U_CreateTime"]
		self.ukey = self.dbObj["U_UKey"]
		self.desc = self.dbObj["U_Description"]
		self.ldapUid = self.dbObj["U_LdapUid"]
		
		return 0
	
	def updateLogin(self):
		
		userObj = {
			"U_LastLogin": get_current_time(),
		}
		
		cond = "WHERE ID='%s'" % self.myId
		ret = self.db.update(TB_ACCOUNT, userObj, cond=cond)
		if (ret == -1):
			WARNING("update user %s error for db operation" % self.name)
			return DB_ERR
	
	def bindLdapUid(self):
		
		userObj = {
			"U_LdapUid": self.ldapUid,
			"U_LastSync": get_current_time(),
		}
		
		cond = "WHERE ID='%s'" % self.myId
		ret = self.db.update(TB_ACCOUNT, userObj, cond=cond)
		if (ret == -1):
			WARNING("update user %s error for db operation" % self.name)
			return DB_ERR
		
		return 0
	
	def unbindLdapUid(self):
		
		userObj = {
			"U_LdapUid": "",
			"U_LastSync": get_current_time(),
		}
		
		cond = "WHERE ID='%s'" % self.myId
		ret = self.db.update(TB_ACCOUNT, userObj, cond=cond)
		if (ret == -1):
			WARNING("update user %s error for db operation" % self.name)
			return DB_ERR
		
		return 0
	
	def bindUkey(self):
		
		userObj = {
			"U_Ukey": self.ukey,
			"U_LastSync": get_current_time(),
		}
		
		cond = "WHERE ID='%s'" % self.myId
		ret = self.db.update(TB_ACCOUNT, userObj, cond=cond)
		if (ret == -1):
			WARNING("update user %s error for db operation" % self.name)
			return DB_ERR
		
		return 0
	
	def unbindUkey(self):
		
		userObj = {
			"U_Ukey": "",
			"U_LastSync": get_current_time(),
		}
		
		cond = "WHERE ID='%s'" % self.myId
		ret = self.db.update(TB_ACCOUNT, userObj, cond=cond)
		if (ret == -1):
			WARNING("update user %s error for db operation" % self.name)
			return DB_ERR
		
		return 0
	
	def update(self):
		
		userObj = {
			"U_Email": self.email,
			"U_PhoneNumber": self.phone,
			"U_UKey": self.ukey,
			"U_LastSync": get_current_time(),
			"U_Description": self.desc
		}
		
		cond = "WHERE ID='%s'" % self.myId
		ret = self.db.update(TB_ACCOUNT, userObj, cond=cond)
		if (ret == -1):
			WARNING("update user %s error for db operation" % self.name)
			return DB_ERR
		
		return 0
	
	def add(self):
		
		self.myId = getUuid()
		
		userObj = {
			"ID": self.myId,
			"U_Name": self.name,
			"U_Password": getEncPass(self.password),
			"U_Email": self.email,
			"U_PhoneNumber": self.phone,
			"U_CreateTime": get_current_time(),
			"U_LastSync": get_current_time(),
			"U_UKey": self.ukey,
		}
		
		ret = self.db.insert(TB_ACCOUNT, userObj)
		if (ret == -1):
			WARNING("add user %s error for db operation" % self.name)
			return DB_ERR
		
		DEBUG(userObj)
		
		return OCT_SUCCESS
	
	def resetPassword(self, newPassword):
		if (not newPassword):
			ERROR("new password not specified when doing password reset operation")
			return NOT_ENOUGH_PARAS
		
		userObj = {
			"U_Password": getEncPass(newPassword),
			"U_LastSync": get_current_time(),
		}
		
		cond = "WHERE ID='%s'" % self.myId
		ret = self.db.update(TB_ACCOUNT, userObj, cond=cond)
		if (ret == -1):
			WARNING("update user %s error for db operation" % self.name)
			return DB_ERR
		
		return OCT_SUCCESS
	
	def auth(self, password):
		cond = "WHERE ID='%s' AND U_Password='%s'" % (self.myId, getEncPass(password))
		userObj = self.db.fetchone(TB_ACCOUNT, cond=cond)
		if (not userObj):
			return USER_PASSWD_ERR
		
		self.updateLogin()
		
		return OCT_SUCCESS
	
	def authUkey(self, ukey):
		cond = "WHERE ID='%s' AND U_UKey='%s'" % (self.myId, ukey)
		userObj = self.db.fetchone(TB_ACCOUNT, cond=cond)
		if (not userObj):
			return USER_PASSWD_ERR
		
		self.updateLogin()
		
		return OCT_SUCCESS
	
	def changePassword(self, oldPassword, newPassword):
		
		if (not newPassword or not oldPassword):
			ERROR("new password or old password not specified when doing password change operation")
			return NOT_ENOUGH_PARAS
		
		ret = self.auth(oldPassword)
		if (ret != OCT_SUCCESS):
			ERROR("old password %s not right" % oldPassword)
			return USER_PASSWD_ERR
		
		ret = self.resetPassword(newPassword)
		if (ret != 0):
			ERROR("modify password error,mayby old pass not right")
			return USER_PASSWD_ERR
		
		return OCT_SUCCESS
	
	def delete(self):
		
		if (self.myId != 0):
			cond = "WHERE ID='%s'" % (self.myId)
		elif (self.name):
			cond = "WHERE U_Name='%s'" % (self.name)
		else:
			ERROR("delete user error, both of id and username not specified")
			return NOT_ENOUGH_PARAS
		
		self.db.delete(TB_ACCOUNT, cond=cond)
		
		return 0
	
	def toObj(self):
		account = {
			"id": self.myId,
			"name": self.name,
			"email": self.email,
			"phone": self.phone,
			"state": self.state,
			"lastLogin": howLongAgo(self.lastLogin),
			"lastSync": getStrTime(self.lastSync),
			"createTime": getStrTime(self.createTime),
			"ukey": self.ukey,
			"ldapUid": self.ldapUid,
			"desc": self.desc,
			"role": self.role,
			"roleCN": self.roleCN,
			"stateCN": self.stateCN
		}
		
		return account
	
	def toObjBrief(self):
		
		return {
			"id": self.myId,
			"name": self.name,
		}
