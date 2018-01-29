#!/usr/bin/python
# -*- coding: utf-8 -*-

import http.client
import json
import ssl
import sys
import time

sys.path.append("../")  # for test in dev env, will delete later
from views.api.api import PARAM_NOT_NULL

sys.path.append("/OCT/OCTFrame")

from core.err_code import CONNECT_SERVER_ERR


def api_result(address, port, task_id, https=False):
	conn = http.client.HTTPConnection(address, port)
	conn.request("GET", "/api/result/%s/" % task_id)
	response = conn.getresponse()
	if response.status != 200:
		return (1, None)

	rsp_body = response.read()
	try:
		rsp = json.loads(rsp_body)
	except:
		return (2, None)

	return (0, rsp)


def api_call(address, port, api_id, api_content, session_key, async=False, server=False, https=False):

	if https:
		if hasattr(ssl, '_create_unverified_context'):
			sslContext = ssl._create_unverified_context()
		else:
			sslContext = None
		conn = http.client.HTTPSConnection(address, port, context=sslContext, check_hostname=None, timeout=30)
	else:
		conn = http.client.HTTPConnection(address, port, timeout=30)

	api_body = {
		"api": api_id,
		"paras": api_content,
		"async": async,
	}

	if session_key:
		if (server):
			api_body["session"] = {
				"skey": session_key
			}
		else:
			api_body["session"] = {
				"uuid": session_key
			}

	try:
		conn.request("POST", "/api/", json.dumps(api_body))
	except:
		return (CONNECT_SERVER_ERR, None)

	response = conn.getresponse()

	if response.status != 200:
		return (1, None)

	rsp_body = response.read()
	if type(rsp_body) == type(b'a'):
		rsp_body = rsp_body.decode()

	try:
		rsp = json.loads(rsp_body)
	except:
		return (2, None)

	if (not async or rsp["data"]["state"] in ["Finished", "Failed"]):
		return (0, rsp)

	task_id = rsp["apiId"]

	def query_until_done():
		conn.request("GET", "/api/result/%s" % task_id)
		response = conn.getresponse()
		if response.status != 200:
			return (3, None)

		rsp_body = response.read()
		rsp = json.loads(rsp_body)
		if (rsp["data"]["state"] in ["Finished", "Failed"]):
			return json.loads(0, rsp)

		time.sleep(1)
		return query_until_done()

	return query_until_done()


def parse_paras(paras, api_proto):
	for (k, v) in list(api_proto["paras"].items()):

		inV = paras.get(k)
		if (v["default"] == PARAM_NOT_NULL and not inV):
			errorMsg = "paras \"%s\" must be specified" % k
			return False, errorMsg
	return 0, None


if __name__ == "__main__":
	api = "octlink.quantum.v1.sync.APISyncMsg"
	paras = {
		"agentId": "123456",
		"type": "CpuInfo",
		"data": "hehe",
		"timeout": 0
	}
	session_uuid = "00000000000000000000000000000000"

	(retCode, retObj) = api_call("10.11.30.168", "9999", api, paras, session_key=session_uuid, async=False, https=False)
	if (retCode):
		print("connect to server error")
	else:
		print((json.dumps(retObj, indent=4)))
