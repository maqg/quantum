#!/usr/bin/python
# -*- coding: utf-8 -*-

from conf.dbconfig import TB_SESSION
from core import dbmysql
from core.log import ERROR
from models.Session import Session
from utils.commonUtil import getUuid
from utils.timeUtil import get_current_time


def clearSession(db=None):
	if (not db):
		db = dbmysql.mysqldb()

	cond = "WHERE S_ExpireTime < %ld" % get_current_time()
	db.delete(TB_SESSION, cond=cond)


def newSession(db, userObj):
	session = Session(db, getUuid())
	session.username = userObj["name"]
	session.cookie = {
		"accountId": userObj["accountId"],
		"id": userObj["id"],
		"name": userObj["name"],
		"role": userObj["role"]
	}
	session.role = userObj["role"]
	session.username = userObj["name"]
	session.userId = userObj["id"]

	session.add()

	return session.toObj()


def getSessionObj(db, sessionId=None):
	session = Session(db, sessionId)
	if (session.init()):
		ERROR("get session error %s" % sessionId)
		return {}

	session.update()

	return session.toObj()


def getSession(db, sessionId=None):
	session = Session(db, sessionId)
	if (session.init()):
		ERROR("get session error %s" % sessionId)
		return None
	return session


def removeSession(db, sessionId):
	session = Session(db, sessionId)
	return session.delete()
