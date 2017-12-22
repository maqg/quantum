# -*- coding: utf-8 -*-

from modules.dashboard import dashboard as dbService
from utils.commonUtil import buildRetObj


def web_get_systeminfo(db, env, arg):
	(ret, data) = dbService.get_systeminfo(db, arg)
	return buildRetObj(ret, data)
