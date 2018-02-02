#!/usr/bin/python3

import os
import sys
sys.path.append("../../../")

from core import dbmysql
from core.log import ERROR, WARNING
from core.membank import memcache
from utils.commonUtil import OCT_SYSTEM, transToStr


tablelist = {}
def row_to_dict(tabname, row, dbname):
	obj = {}
	list(map(obj.__setitem__, tablelist[dbname][tabname], row))
	return obj 


def get_log(db, dbname):
	logList = []

	ret = db.select("tb_log", limit=100, dbname=dbname)
	if ret == -1:
		ERROR("select tb_log db error")
		return logList

	for dur in db.cur:
		obj = row_to_dict("tb_log", dur, dbname)
		logList.append(obj)

	return logList	


if __name__ == '__main__':

	if not os.path.exists("/OCT/etc/version"):
		ERROR("file /OCT/etc/version not exist")
		sys.exit(1)

	if not os.path.exists("/OCT/etc/internal_version"):
		ERROR("file /OCT/etc/internal_version not exist")
		sys.exit(1)

	with open("/OCT/etc/version", "r") as fd:
		content = fd.readline()

		VERSION = content.split('.')[0]
		if VERSION != '5' and VERSION != '3':
			ERROR("unsupport version rvm[%s]" %VERSION)
			sys.exit(1)

	with open("/OCT/etc/internal_version", "r") as fd:
		content = fd.readline()

		if "center" in content or "RVMCenter" in content:
			PLATFORM = "center"
		elif "allinone" in content:
			PLATFORM = "allinone"
		else:
			PLATFORM = "server"

	if PLATFORM == "server":
		WARNING("rvm server no need get log info")
		sys.exit(1)

	if VERSION == '3':
		DB_NAME = 'octlog'
	else: 
		DB_NAME = 'dbcenter'

	BANK_ADDR = "/OCT/OCTFrame/core/membank/%s"
	membody = memcache.get_mem(DB_NAME, BANK_ADDR)
	tablelist = membody.get('tablelist', {}) 

	db = dbmysql.mysqldb()
	loginfo = get_log(db, DB_NAME)
	print(loginfo)

	del db
