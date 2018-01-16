# -*- coding: utf-8 -*-

from modules.syncmsg.syncmsg import syncmsg, get_syncmsg
from utils.commonUtil import buildRetObj


def web_show_syncmsg(db, env, arg):
	(ret, data) = get_syncmsg(db, arg)
	return buildRetObj(ret, data)


def web_syncmsg(db, env, arg):
	(ret, data) = syncmsg(db, env, arg)
	return buildRetObj(ret, data)