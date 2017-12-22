# -*- coding: utf-8 -*-

from core import dbmysql
from core.err_code import USER_ALREADY_EXIST, INVALID_PARAS, USER_NOT_EXIST
from models.Account import *
from models.Common import DEFAULT_ACCOUNT
from utils.commonUtil import b64_decode

AUTHKEY_TIMEOUT = 24 * 30 * 60


def get_userlist(db):
	user_list = []
	
	ret = db.select(TB_ACCOUNT, cond="")
	if ret == -1:
		ERROR("get user list error")
		return (DB_ERR, None)
	
	for dur in db.cur:
		obj = dbmysql.row_to_dict(TB_ACCOUNT, dur)
		temp = {
			"id": obj["ID"],
			"name": obj["U_Name"],
		}
		user_list.append(temp)
	
	DEBUG(user_list)
	
	return (OCT_SUCCESS, user_list)


def get_alluser(db, arg):
	listObj = {
		"total": 0,
		"users": [],
	}
	
	start = arg["paras"].get("start") or 0
	limit = arg["paras"].get("limit") or 100
	
	cond = "WHERE 1=1 "
	ret = db.select(TB_ACCOUNT, cond=cond, limit=int(limit), offset=int(start))
	if ret == -1:
		ERROR("get user list error")
		return (DB_ERR, None)
	
	for dur in db.cur:
		obj = dbmysql.row_to_dict(TB_ACCOUNT, dur)
		user = Account(db, dbObj=obj)
		user.loadFromObj()
		
		listObj["users"].append(user.toObj())
	
	listObj["total"] = getAccountCount(db)
	
	return (OCT_SUCCESS, listObj)


def get_user(db, userId):
	user = Account(db, userId)
	
	if (user.init() != 0):
		ERROR("user %s not exist" % userId)
		return (USER_NOT_EXIST, None)
	
	return (OCT_SUCCESS, user.toObj())


def add_user(db, arg):
	paras = arg["paras"]
	
	account = paras["account"]
	
	user = getAccount(db, userName=account)
	if (user):
		WARNING("user %s already exist" % account)
		return USER_ALREADY_EXIST
	
	user = Account(db)
	
	user.name = account
	user.password = b64_decode(paras["password"])
	
	if (not user.name or not user.password):
		ERROR("not username or password specified")
		return NOT_ENOUGH_PARAS
	
	user.email = paras["email"]
	user.phone = paras["phoneNumber"]
	
	ret = user.add()
	
	return ret


def delete_user(db, args):
	userId = args["paras"]["id"]
	
	user = getAccount(db, userId=userId)
	if (not user):
		ERROR("account %s not exist" % (userId))
		return USER_NOT_EXIST
	
	if (user.name == DEFAULT_ACCOUNT):
		ERROR("account %s is super admin, forbid delete." % (userId))
		return INVALID_PARAS
	
	return user.delete()


def reset_password(db, arg):
	paras = arg["paras"]
	
	user = getAccount(db, userId=paras["id"])
	if (not user):
		ERROR("user %s not exist" % (paras["id"]))
		return USER_NOT_EXIST
	
	return user.resetPassword(b64_decode(paras["password"]))


def update_user(db, arg):
	user = getAccount(db, userId=arg["paras"].get("id"))
	if (not user):
		ERROR("user %s not exist" % (arg["paras"].get("id")))
		return USER_NOT_EXIST
	
	user.email = arg["paras"].get("email") or ""
	user.phone = arg["paras"].get("phoneNumber") or ""
	user.desc = arg["paras"].get("desc") or ""
	
	return user.update()


def change_password(db, arg):
	paras = arg["paras"]
	
	user = getAccount(db, userId=paras["id"])
	if (not user):
		ERROR("user %s not exist" % (paras["id"]))
		return USER_NOT_EXIST
	
	return user.changePassword(b64_decode(paras["oldPassword"]),
	                           b64_decode(paras["newPassword"]))


def getAccountByName(db, name):
	return getAccount(db, userName=name)
