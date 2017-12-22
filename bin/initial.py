#!/usr/bin/python
# -*- coding: utf-8 -*-

from fcntl import flock, LOCK_EX, LOCK_UN
import os
import sys

import pickle as pickle
import db_init

sys.path.append(".")
sys.path.append("../")

from conf.dbconfig import DB_NAME

MEMSIZE = 1024 * 128
BankAddr = '../core/membank/%s'
DB_DIR = './'

DBXMLPATH_POOL = { 
	DB_NAME: DB_DIR + "mysql.xml"
}

def save_mem(obj, custom=DB_NAME):
	bankname = BankAddr % custom

	mem = pickle.dumps(obj, protocol=0)

	lenth = len(mem)
	fd = open(bankname, 'w+', encoding="utf-8")

	flock(fd, LOCK_EX)
	fd.write(mem.decode("ascii"))
	fd.write('\0' * (MEMSIZE - lenth))
	flock(fd, LOCK_UN)
	fd.close()
	os.chmod(bankname, 0o777)

def checkpath(filepath):
	if os.access(filepath, os.F_OK):
		try:
			os.remove(filepath)
		except OSError:
			pass
	fd = open(filepath, 'w+')
	fd.close()
	for filename in os.listdir(DB_DIR):
		os.chmod('%s/%s'%(DB_DIR, filename), 0o777)

def init_db():
	tablelist = db_init.db_initcols(DBXMLPATH_POOL)
	mem = {'tablelist': tablelist}
	save_mem(mem, custom=DB_NAME)

	return True

if __name__ == '__main__':
	init_db()
