#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import traceback
import struct
import socket
import platform
from logging.handlers import RotatingFileHandler

from conf.config import *
from models.SystemConf import getSystemConf, SystemConf
from utils.commonUtil import toString

LVL_EMERG = 0
LVL_ALERT = 1
LVL_CRIT = 2
LVL_ERROR = 3
LVL_WARN = 4
LVL_NOTIFY = 5
LVL_INFO = 6
LVL_DEBUG = 7

LOG_LEVELS = ["Emerg", "Alert", "Crit", "Error", "Warn", "Notify", "Info", "Debug"]

currentLevel = -1
lastLevelUpdateTime = 0

MAX_USING_TIMEOUT = 10  # seconds

currentLogLevels = {}
lastUpdateTime = 0

LOG_HOST = "127.0.0.1"
LOG_PORT = 62514

MSGID_LOG = 1000
MSGID_ALARM = 1001
MSGID_CONFIG_AR = 1002
MSGID_CONFIG_AM = 1003
MSGID_CONFIG_RL = 1004


def getDebugLevel():
	return getSystemConf().debugLevel


def create_file(logfile):
	if not os.path.exists(LOG_FILE_PATH):
		os.mkdir(LOG_FILE_PATH)
	
	if not os.path.exists(logfile):
		fp = open(logfile, "w+")
		fp.close()
		os.chmod(logfile, 0o666)


def loginit(trace):
	trace_len = len(trace)
	trace = trace[trace_len - 2][:2]
	
	system = SystemConf.system
	if (system == "center"):
		log_suffix = ".log"
	else:
		log_suffix = "_server.log"
	
	sysstr = platform.system()
	if (sysstr == "Windows"):
		file_name = LOG_FILE_PATH + ((trace[0].split('\\'))[-1]).split("/")[-1].split(".")[0] + log_suffix
	else:
		file_name = LOG_FILE_PATH + ((trace[0].split('/'))[-1]).split("/")[-1].split(".")[0] + log_suffix
	create_file(file_name)
	
	logger = logging.getLogger()
	
	handle = RotatingFileHandler(file_name, "a", OCTFRAME_LOG_MAX_LEN, 2) # with backup counts 2
	formatter = logging.Formatter('%(funcName)s [%(asctime)s %(lineno)d]: %(message)s')
	handle.setFormatter(formatter)
	logger.addHandler(handle)
	logger.setLevel(logging.NOTSET)
	
	return (logger, handle)


def DEBUG(msg, *args):
	if getDebugLevel() < LVL_DEBUG:
		return
	logger, handle = loginit(traceback.extract_stack())
	logger.info(msg, *args)
	_close(handle, logger)


def INFO(msg, *args):
	if getDebugLevel() < LVL_INFO:
		return
	logger, handle = loginit(traceback.extract_stack())
	logger.info(msg, *args)
	_close(handle, logger)


def WARNING(msg, *args):
	if getDebugLevel() < LVL_WARN:
		return
	logger, handle = loginit(traceback.extract_stack())
	logger.warning(msg, *args)
	_close(handle, logger)


def ERROR(msg, *args):
	if getDebugLevel() < LVL_ERROR:
		return
	logger, handle = loginit(traceback.extract_stack())
	logger.error(msg, *args)
	_close(handle, logger)


def CRITICAL(msg, *args):
	if getDebugLevel() < LVL_CRIT:
		return
	logger, handle = loginit(traceback.extract_stack())
	logger.critical(msg, *args)
	_close(handle, logger)


def _close(handle, logger):
	try:
		handle.flush()
		logger.removeHandler(handle)
		logging.shutdown()
	except Exception:
		pass


def get_tuple(msg):
	if (type(msg) == int):
		return (msg)
	
	if (not msg):
		return ()
	
	if (type(msg) == tuple):
		tempList = []
		for item in msg:
			if (type(item) == int):
				tempList.append(item)
			else:
				tempList.append(toString(item).decode())
		return tuple(tempList)
	else:
		return (toString(msg).decode())


# object_tuple=(type, objectid, objectname)
def oct_audit(eid, level, user, object_tuple, msg_tuple=None, errorCode=0):
	pass


def oct_logging(eid, level, user, msg=None, errorCode=0):
	pass
