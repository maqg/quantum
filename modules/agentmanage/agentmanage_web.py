# -*- coding: utf-8 -*-

from modules.agentmanage.agentmanage import get_agents, get_agent, add_agent, remove_agent
from utils.commonUtil import buildRetObj


def web_remove_agent(db, env, arg):
	(ret, data) = remove_agent(db, arg)
	return buildRetObj(ret, data)


def web_show_agent(db, env, arg):
	(ret, data) = get_agent(db, arg)
	return buildRetObj(ret, data)


def web_show_all_agent(db, env, arg):
	(ret, data) = get_agents(db, arg)
	return buildRetObj(ret, data)


def web_add_agent(db, env, arg):
	(ret, data) = add_agent(db, arg)
	return buildRetObj(ret, data)