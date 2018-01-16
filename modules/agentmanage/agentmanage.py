# -*- coding: utf-8 -*-

from conf.dbconfig import TB_AGENT
from core import dbmysql
from core.err_code import OCT_SUCCESS, DB_ERR, SEGMENT_NOT_EXIST
from core.log import ERROR
from models.Agent import Agent, getAgent
from models.Agent import getAgentCount


def get_agent(db, arg):
	agentId = arg["paras"]["id"]
	agent = getAgent(db, agentId)
	if not agent:
		ERROR("agent %s not exist" % agentId)
		return (SEGMENT_NOT_EXIST, None)
	return (OCT_SUCCESS, agent.toObj())


def get_agents(db, arg):
	listObj = {
		"total": 0,
		"list": [],
	}
	
	start = arg["paras"].get("start") or 0
	limit = arg["paras"].get("limit") or 100
	
	cond = "WHERE 1=1 "
	ret = db.select(TB_AGENT, cond=cond, limit=int(limit), offset=int(start))
	if ret == -1:
		ERROR("get agent list error")
		return (DB_ERR, None)
	
	for dur in db.cur:
		obj = dbmysql.row_to_dict(TB_AGENT, dur)
		item = Agent(db, dbObj=obj)
		item.loadFromObj()
		
		listObj["list"].append(item.toObj())
	
	listObj["total"] = getAgentCount(db)
	
	return (OCT_SUCCESS, listObj)


def add_agent(db, arg):
	paras = arg["paras"]
	
	agent = Agent(db)
	agent.name = paras["name"]
	agent.address = paras["address"]
	ret = agent.add()
	
	return (ret, None)


def remove_agent(db, arg):
	paras = arg["paras"]
	agent = getAgent(db, paras["id"])
	if not agent:
		ERROR("no agent to remove %s" % paras["id"])
		return SEGMENT_NOT_EXIST
	
	ret = agent.delete()
	
	return (ret, None)
