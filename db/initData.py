#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time

sys.path.append("../")

from utils.commonUtil import fileToObj, getUuid, transToStr

now = int(time.time() * 1000)

def createSql(productType, obj):

	header = "INSERT INTO tb_product (ID, P_Name, P_Type, P_TypeName, P_Info, "
	header += "P_Description, P_LastSync, P_CreateTime) VALUES ("

	typeName = obj["name"]
	products = obj["products"]

	for product in products:
		sql = "'%s'" % getUuid()
		sql += ",'%s'" % product["name"]
		sql += ",'%s'" % productType
		sql += ",'%s'" % typeName
		sql += ",'%s'" % transToStr(product)
		sql += ",'%s'" % product.get("desc") or ""
		sql += ",'%ld'" % now
		sql += ",'%ld'" % now

		print(header + sql + ");")


if __name__ == '__main__':
	prices = fileToObj("../prices.json")
	for (k, v) in prices.items():
		createSql(k, v)