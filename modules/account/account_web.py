# -*- coding: utf-8 -*-

from core.err_code import OCT_SUCCESS, USER_PASSWD_ERR, USER_NOT_EXIST
from core.log import ERROR
from modules.account import account as userService
from utils.commonUtil import buildRetObj, b64_decode
from utils.sessionUtil import newSession, getSession


def web_get_user(db, env, arg):
	userId = arg["paras"].get("id")
	if userId == None:
		ret, data = userService.get_alluser(db, arg)
	else:
		ret, data = userService.get_user(db, userId)
	
	return buildRetObj(ret, data)


def web_get_userlist(db, env, arg):
	(ret, data) = userService.get_userlist(db)
	return buildRetObj(ret, data)


def web_add_user(db, env, arg):
	ret = userService.add_user(db, arg)
	return buildRetObj(ret)


def web_del_user(db, env, arg):
	ret = userService.delete_user(db, arg)
	return buildRetObj(ret)


def web_login(db, env, arg):
	paras = arg["paras"]
	user = userService.getAccountByName(db, paras.get("account"))
	if (not user):
		return buildRetObj(USER_NOT_EXIST, None)
	
	ret = user.auth(b64_decode(paras.get("password")))
	if ret == 0:
		data = {
			"id": user.myId,
			"name": user.name,
			"role": user.role,
			"accountId": user.myId,
		}
		sessionObj = newSession(db, data)
		data["session"] = sessionObj
		
		return buildRetObj(OCT_SUCCESS, data)
	else:
		return buildRetObj(USER_PASSWD_ERR)


def web_logout(db, env, arg):
	sessionId = arg.get("centerSessionID")
	if not sessionId:
		ERROR("no session uuid to logout %s" % str(arg))
		return buildRetObj(OCT_SUCCESS)
	
	session = getSession(db, sessionId)
	if not session:
		ERROR("get session error to logout %s" % sessionId)
		return buildRetObj(OCT_SUCCESS)
	
	return buildRetObj(OCT_SUCCESS)


def web_modify_password(db, env, arg):
	ret = userService.change_password(db, arg)
	return buildRetObj(ret)


def web_reset_password(db, env, arg):
	ret = userService.reset_password(db, arg)
	return buildRetObj(ret)


def web_update_user(db, env, arg):
	ret = userService.update_user(db, arg)
	return buildRetObj(ret)
