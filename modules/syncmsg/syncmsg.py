# -*- coding: utf-8 -*-

from conf.dbconfig import TB_MSG
from core import dbmysql
from core.err_code import OCT_SUCCESS, DB_ERR
from core.log import ERROR, WARNING
from models.Agent import getAgentFromCache, Agent, AddAgentToCache
from models.Msg import Msg, getMsgCount


def get_syncmsg(db, arg):
	listObj = {
		"total": 0,
		"list": [],
	}
	
	paras = arg["paras"]
	
	start = arg["paras"].get("start") or 0
	limit = arg["paras"].get("limit") or 100
	
	cond = "WHERE 1=1 "
	ret = db.select(TB_MSG, cond=cond, limit=int(limit), offset=int(start))
	if ret == -1:
		ERROR("get agent list error")
		return (DB_ERR, None)
	
	for dur in db.cur:
		obj = dbmysql.row_to_dict(TB_MSG, dur)
		item = Msg(db, dbObj=obj)
		item.loadFromObj()
		listObj["list"].append(item.toObj())
	
	listObj["total"] = getMsgCount(db)
	
	return (OCT_SUCCESS, listObj)

def addAgent(db, agentId, name, addr):
	agent = Agent(db, agentId)
	agent.name = name
	agent.address = addr
	agent.add()
	return agent.toObj()


def syncmsg(db, env, arg):
	paras = arg["paras"]
	
	agentId = paras["agentId"]
	agentObj = getAgentFromCache(agentId)
	if not agentObj:
		WARNING("agent not exist in cache %s" % agentId)
		agentObj = addAgent(db, agentId, arg["REMOTE_ADDR"], arg["REMOTE_ADDR"])
		AddAgentToCache(agentObj)
	
	msg = Msg(db)
	msg.msg = paras["data"]
	msg.type = paras["type"]
	msg.agentId = agentId
	
	msg.add()
	
	return (OCT_SUCCESS, None)
