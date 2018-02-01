#!/usr/bin/python3

import os
import sys
sys.path.append("../../../")

from core import dbmysql
from core.log import ERROR
from core.membank import memcache
from utils.commonUtil import OCT_SYSTEM, transToStr


DB_NAME = ""
BANK_ADDR = "/OCT/OCTFrame/core/membank/%s"
tablelist = {}

def row_to_dict(tabname, row, dbname):
	obj = {}
	list(map(obj.__setitem__, tablelist[dbname][tabname], row))
	return obj 


def get_log(db, limit=100):
	logList = []

	ret = db.select("tb_log", limit=int(limit), dbname=DB_NAME)
	if ret == -1:
		ERROR("select tb_log db error")
		return logList

	for dur in db.cur:
		obj = row_to_dict("tb_log", dur, DB_NAME)
		logList.append(obj)

	return logList	


if __name__ == '__main__':

	if not os.path.exists("/OCT/etc/internal_version"):
		ERROR("file /OCT/etc/internal_version not exist")
		sys.exit(1)

	fd = open("/OCT/etc/internal_version", "r")
	content = fd.readline()

	if "allinone" in content or "center" in content:
		DB_NAME = "dbcenter"
	elif "RVMCenter" in content:
		DB_NAME = "octlog"
	else:
		ERROR("This host is not center or allinone")
		fd.close()
		sys.exit(1)

	fd.close()

	membody = memcache.get_mem(DB_NAME, BANK_ADDR)
	tablelist = membody.get('tablelist', {}) 

	db = dbmysql.mysqldb()
	loginfo = get_log(db)
	print(loginfo)

	del db
