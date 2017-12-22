# -*- coding: utf-8 -*-

import time

from conf.config import MAX_USING_TIMEOUT, LVL_DEBUG
from core.modules_code import MOD_WEBUI
from utils.commonUtil import isSystemWindows
from utils.octlog import get_debug_level


def getSystemConf():
	SystemConf.init()
	return SystemConf


class SystemConf():
	version = "5.0"
	debugLevel = -1
	system = "center"
	lastLevelUpdateTime = 0
	isStoreApiRecord = False
	
	def __init__(self):
		pass
	
	@staticmethod
	def init():
		now = int(time.time())
		if (abs(now - SystemConf.lastLevelUpdateTime) >= MAX_USING_TIMEOUT or SystemConf.debugLevel == -1):
			if (isSystemWindows()):
				SystemConf.debugLevel = LVL_DEBUG
			else:
				SystemConf.debugLevel = get_debug_level(MOD_WEBUI)
			SystemConf.lastLevelUpdateTime = now
	
	@staticmethod
	def toObj():
		
		return {
			"version": SystemConf.version,
			"system": SystemConf.system,
			"debugLevel": SystemConf.debugLevel,
			"lastLevelUpdateTime": SystemConf.lastLevelUpdateTime
		}
