#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom

def init_cols(xmlpath):
	singlefile = {}
	try:
		xmldoc = minidom.parse(xmlpath)
	except:
		return singlefile

	filelist = xmldoc.getElementsByTagName('file')

	for index in range(len(filelist)):
		table = filelist[index]
		tablename = table.attributes['name'].value
		fieldlist = table.getElementsByTagName('field')
		columnlist = []

		for i in range(len(fieldlist)):
			name = fieldlist[i].attributes['name'].value
			columnlist.append(name)

		singlefile[tablename]=columnlist

	return singlefile

def db_initcols(xmlpathlist):
	cols = {}
	for dbname, xmlpath in list(xmlpathlist.items()):
		cols[dbname] = init_cols(xmlpath)
	return cols
