# -*- coding: utf-8 -*-

import pymysql as mysql

from conf.dbconfig import DB_USER, DB_PASSWORD, DB_NAME, DB_SERVER, get_sock_file
from core.membank import memcache
from utils.commonUtil import isSystemWindows, getSystemType, SYSTEM_TYPE_LINUX

membody = memcache.get_mem()
tablelist = membody.get('tablelist', {})
SQL_ERROR = -1
SQL_SUCCESS = 0


def row_to_dict(tabname, row, dbname=DB_NAME):
	obj = {}
	list(map(obj.__setitem__, tablelist[dbname][tabname], row))
	return obj


class mysqldb():
	def __init__(self):
		self.connlist = {}

	def __del__(self):
		for conn in list(self.connlist.values()):
			conn.close()

	def connect(self, dbname):
		conn = self.connlist.get(dbname, None)
		if conn == None:
			if (getSystemType() != SYSTEM_TYPE_LINUX):
				conn = mysql.Connect(user=DB_USER,
				                     passwd=DB_PASSWORD,
				                     host=DB_SERVER,
				                     charset='utf8',
				                     db=dbname)
			else:
				sockFile = get_sock_file()
				conn = mysql.Connect(user=DB_USER,
				                     passwd=DB_PASSWORD,
				                     unix_socket=sockFile,
				                     charset='utf8',
				                     db=dbname)
			conn.autocommit(True)
			self.connlist[dbname] = conn
		return conn
	
	def select(self, table, cond='', field='*', offset=0, limit=1000000, dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		
		self.cur = conn.cursor()
		sql = 'SELECT %s FROM %s %s LIMIT %d OFFSET %d' % (field, table, cond, limit, offset)
		try:
			self.cur.execute(sql)
		except mysql.OperationalError:
			return SQL_ERROR
		return SQL_SUCCESS
	
	def LOCK(self, table, pri="READ", dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		self.cur = conn.cursor()
		try:
			self.cur.execute("LOCK TABLE %s %s" % (table, pri))
		except mysql.OperationalError:
			return SQL_ERROR
		return SQL_SUCCESS
	
	def UNLOCK(self, dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		self.cur = conn.cursor()
		try:
			self.cur.execute("UNLOCK TABLES")
		except mysql.OperationalError:
			return SQL_ERROR
		return SQL_SUCCESS
	
	def SELECT(self, sql, dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		self.cur = conn.cursor()
		try:
			self.cur.execute(sql)
		except mysql.OperationalError:
			return SQL_ERROR
		return SQL_SUCCESS
	
	def SELECTONE(self, sql, dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return None
		self.cur = conn.cursor()
		try:
			self.cur.execute(sql)
			objs = self.cur.fetchall()
			if (len(objs) == 0):
				self.cur.close()
				return None
			else:
				self.cur.close()
		except mysql.OperationalError:
			return None
		
		return objs[0]
	
	def FETCHONE(self, sql, dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return None
		self.cur = conn.cursor()
		try:
			self.cur.execute(sql)
			objs = self.cur.fetchall()
			if (len(objs) == 0):
				self.cur.close()
				return None
			else:
				self.cur.close()
		except mysql.OperationalError:
			return None
		
		return objs[0]
	
	def fetchone(self, table, cond='', field='*', dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return None
		self.cur = conn.cursor()
		sql = 'SELECT %s FROM %s %s LIMIT 1;' % (field, table, cond)
		try:
			self.cur.execute(sql)
			for dur in self.cur:
				obj = row_to_dict(table, dur, dbname=dbname)
				self.cur.close()
				return obj
		except mysql.OperationalError:
			return None
		
		self.cur.close()
		return None
	
	def rowcount(self, table, cond='', dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return -1
		self.cur = conn.cursor()
		sql = 'SELECT COUNT(*) FROM %s %s' % (table, cond)
		try:
			self.cur.execute(sql)
		except mysql.OperationalError:
			return SQL_ERROR
		count = self.cur.fetchall()[0][0]
		self.cur.close()
		
		return count
	
	def insert(self, table, obj, dbname=DB_NAME):
		
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		
		self.cur = conn.cursor()
		columns = tablelist[dbname][table]
		columnlist = [k for k in list(obj.keys()) if k in columns]
		
		sql = 'INSERT INTO %s (%s) VALUES(%s)' % (table,
		                                          ','.join(columnlist),
		                                          ','.join(['%%(%s)s' % k for k in columnlist]))
		try:
			self.cur.execute(sql, obj)
		except mysql.OperationalError:
			conn.rollback()
			return SQL_ERROR
		
		rowid = self.cur.lastrowid
		if rowid == None:
			conn.rollback()
			return SQL_ERROR
		conn.commit()
		return rowid
	
	def delete(self, table, obj=None, limit=1000000, cond='', dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		self.cur = conn.cursor()
		if obj != None:
			if 'id' in obj:
				cond = 'WHERE id=%(id)s'
			else:
				cond = 'WHERE %s' % ' AND '.join(['%s=%%(%s)s' % (k, k) for k in list(obj.keys())])
		
		cond += " LIMIT %d " % (limit)
		
		sql = 'DELETE FROM %s %s' % (table, cond)
		if obj == None: obj = {}
		try:
			self.cur.execute(sql, obj)
		
		except mysql.OperationalError:
			conn.rollback()
			return SQL_ERROR
		conn.commit()
		return SQL_SUCCESS
	
	def update(self, table, obj=None, cond='', field='', dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		self.cur = conn.cursor()
		
		if obj != None:
			columns = tablelist[dbname][table]
			columnlist = [k for k in list(obj.keys()) if k in columns]
			field = 'SET %s' % ','.join(['%s=%%(%s)s' % (k, k) for k in columnlist])
		if cond == '':
			if 'id' in obj:
				cond = 'WHERE id=%(id)s'
		
		sql = 'UPDATE %s %s %s' % (table, field, cond)
		if obj == None: obj = {}
		try:
			self.cur.execute(sql, obj)
		except mysql.OperationalError:
			conn.rollback()
			return SQL_ERROR
		conn.commit()
		return SQL_SUCCESS
	
	def execute(self, table, sql, dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		self.cur = conn.cursor()
		try:
			self.cur.execute(sql)
		except mysql.OperationalError:
			conn.rollback()
			return SQL_ERROR
		conn.commit()
		return SQL_SUCCESS
	
	def insert_ex(self, table, obj, dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		self.cur = conn.cursor()
		columns = tablelist[dbname][table]
		columnlist = [k for k in list(obj.keys()) if k in columns]
		
		sql = 'INSERT INTO %s (%s) VALUES(%s)' % (table, ','.join(columnlist),
		                                          ','.join(['%(%s)s' % k for k in columnlist]))
		try:
			self.cur.execute(sql, obj)
		except mysql.OperationalError:
			return SQL_ERROR
		
		rowid = self.cur.lastrowid
		if rowid == None:
			return SQL_ERROR
		return rowid
	
	def delete_ex(self, table, obj=None, limit=1000000, cond='', dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		self.cur = conn.cursor()
		if obj != None:
			if 'id' in obj:
				cond = 'WHERE id=%(id)s'
			else:
				cond = 'WHERE %s' % ' AND '.join(['%s=%%(%s)s' % (k, k) for k in list(obj.keys())])
		
		cond += " LIMIT %d " % (limit)
		
		sql = 'DELETE FROM %s %s' % (table, cond)
		if obj == None: obj = {}
		try:
			self.cur.execute(sql, obj)
		except mysql.OperationalError:
			return SQL_ERROR
		return SQL_SUCCESS
	
	def update_ex(self, table, obj=None, cond='', field='', dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		self.cur = conn.cursor()
		
		if obj != None:
			columns = tablelist[dbname][table]
			columnlist = [k for k in list(obj.keys()) if k in columns]
			field = 'SET %s' % ','.join(['%s=%%(%s)s' % (k, k) for k in columnlist])
		if cond == '':
			if 'id' in obj:
				cond = 'WHERE id=%(id)s'
		
		sql = 'UPDATE %s %s %s' % (table, field, cond)
		if obj == None: obj = {}
		try:
			self.cur.execute(sql, obj)
		except mysql.OperationalError:
			return SQL_ERROR
		return SQL_SUCCESS
	
	def execute_ex(self, table, sql, dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		self.cur = conn.cursor()
		try:
			self.cur.execute(sql)
		except mysql.OperationalError:
			return SQL_ERROR
		return SQL_SUCCESS
	
	def create_function(self, name, num_params, func, dbname=DB_NAME):
		conn = self.connect(dbname)
		if (conn == None):
			return SQL_ERROR
		conn.create_function(name, num_params, func)
		return SQL_SUCCESS
	
	def rollback(self, dbname=DB_NAME):
		self.connlist.get(dbname).rollback()
	
	def commit(self, dbname=DB_NAME):
		self.connlist.get(dbname).commit()
