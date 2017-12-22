#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import traceback

from core import dbmysql
from core.err_code import NO_AUTH_SKEY, INVALID_PARAS, CONNECT_SERVER_ERR, OCT_SUCCESS
from core.log import ERROR, DEBUG, INFO
from models.Account import ROLE_SUPERADMIN
from models.Common import DEFAULT_ACCOUNT_ID
from utils.commonUtil import getUuid, buildRetObj, isSystemWindows
from utils.httpUtil import buildReply, getArgObj, buildFailureReply
from utils.sessionUtil import getSessionObj
from views.api.dispatch import doDispatching, IGNORE_SESSION_APIS

sys.path.append("../")

import tornado
import tornado.httpclient
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.websocket
import tornado.options
from conf.config import *
from views.api.api import API_MODULE_LIST, API_PREFIX, PARAM_TYPE_INT

LISTEN_PORT = 9090
LISTEN_ADDR = "0.0.0.0"

API_PROTOS = {}

API_VIEW_LIST = {}

SERVER_API_PROTOS = {}

MB = 1024 * 1024
GB = 1024 * MB
TB = 1024 * GB
MAX_STREAMED_SIZE = 1 * TB  # Max. size streamed in one request!


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", UserPortalHandler),
			(r"/login/", UserLoginHandler),
			(r"/logout/", UserLogoutHandler),
			(r"/src/templates/(.*)", SrcHandler),
			(r"/api/", ApiHandler),
			(r"/api/test/", ApiTestHandler),
			(r"/files/commonupload/", FileUploadHandler),
		]
		settings = dict(
			cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
			autoreload=True,
			xsrf_cookies=False,
		)
		tornado.web.Application.__init__(self, handlers, **settings)


class SrcHandler(tornado.web.RequestHandler):
	def get(self, filepath=None):
		query = self.request.query
		if (query):
			self.redirect("/static/src/templates/%s?%s" % (filepath, query))
		else:
			self.redirect("/static/src/templates/%s" % filepath)


class ClassUIHandler(tornado.web.RequestHandler):
	def get(self, filepath=None):

		query = self.request.query

		if not filepath:
			self.render("classui.html")
		else:
			if (query):
				self.redirect("/static/classui/%s?%s" % (filepath, query))
			else:
				self.redirect("/static/classui/%s" % filepath)


class UserPortalHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def get(self):

		cookie = self.get_cookie("rvmusercookie", "")
		username = self.get_cookie("username", "")
		userid = self.get_cookie("userid", "")
		accountname = self.get_cookie("accountname", "admin")

		if not cookie:
			self.redirect("/login/")
			return

		self.db = dbmysql.mysqldb()
		session = getSessionObj(self.db, sessionId=cookie)
		del self.db
		if not session:
			self.redirect("/login/")
			return

		self.render("userportal/userportal.html", USER_NAME=username,
		            USER_ID=userid, ACCOUNT_NAME=accountname, SESSION_ID=session["id"])


LOGIN_TYPE_LDAP = "ldap"
LOGIN_TYPE_LOCALDB = "localdb"


class UserLoginHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def get(self):
		error = self.get_argument("error", "")
		if error:
			prompt = "用户名或密码错误！"
		else:
			prompt = ""
		self.render("userportal/login.html", ACTION="error", PROMPT=prompt)

	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def post(self):

		# Step 1, Login with default account
		argObj = getArgObj(self.request)
		paras = {
			"account": self.get_argument("username"),
			"password": self.get_argument("password"),
			"role": 7,
		}
		argObj["api"] = "octlink.quantum.v1.account.APILoginByAccount"
		argObj["paras"] = paras

		self.db = dbmysql.mysqldb()
		session = getSessionObj(self.db, sessionId="00000000000000000000000000000000")
		del self.db

		argObj["session"] = session
		retObj = doDispatching(argObj, session, API_PROTOS)
		if retObj["RetCode"] != OCT_SUCCESS:
			ERROR("login error %s" % str(retObj))
			self.redirect("/login/?error=true")
		else:
			sessionObj = retObj["RetObj"]["session"]
			self.set_cookie("rvmusercookie", sessionObj["id"])
			self.set_cookie("username", retObj["RetObj"]["name"])
			self.set_cookie("userid", retObj["RetObj"]["id"])
			self.redirect("/")


class UserLogoutHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def get(self):
		cookie = self.get_cookie("rvmusercookie", "")
		if cookie:
			self.clear_cookie("rvmusercookie")

		self.redirect("/login/")


class ApiTestHandler(tornado.web.RequestHandler):
	result = {
		"moduleSelected": "account",
		"apiSelected": "octlink.quantum.v1.account.APILoginByAccount",
		"request": "{}",
		"reply": "{}",
		"paras": "{}"
	}

	@tornado.web.asynchronous
	def get(self):

		self.render("testapi.html", moduleList=API_VIEW_LIST,
		            moduleListStr=json.dumps(API_VIEW_LIST, indent=4),
		            result=self.result,
		            resultStr=json.dumps(self.result, indent=4, ensure_ascii=False))

	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def post(self, *args, **kwargs):

		argObj = getArgObj(self.request)
		api = argObj["api"]
		paras = argObj["paras"]
		async = False

		if paras["timeout"] != 0:
			async = True

		api_body = {
			"api": api,
			"paras": paras,
			"async": async,
			"session": {
				"uuid": "00000000000000000000000000000000"
			}
		}

		self.result["paras"] = argObj["paras"]
		self.result["moduleSelected"] = argObj["module"]
		self.result["apiSelected"] = argObj["api"]
		self.result["request"] = json.dumps(argObj, indent=4, ensure_ascii=False)

		client = tornado.httpclient.AsyncHTTPClient()

		url = "http://%s:%d/api/" % ("127.0.0.1", RUNNING_PORT)
		ERROR("%sfff" % url)
		response = yield client.fetch(url, method="POST", request_timeout=10, connect_timeout=10,
		                              body=json.dumps(api_body))
		self.on_response(response)

	def on_response(self, resp):

		body = json.loads(str(resp.body, encoding="utf-8"))
		if body == None:
			result = buildFailureReply(CONNECT_SERVER_ERR)
			self.result["reply"] = json.dumps(result, indent=4, ensure_ascii=False)
			self.write(json.dumps(result, indent=4, ensure_ascii=False))
		else:
			self.result["reply"] = json.dumps(body, indent=4, ensure_ascii=False)
			self.write(body)

		self.redirect("/api/test/")


def getSessionId(argObj):
	session = argObj.get("session")
	if (session):
		return session.get("uuid")
	else:
		return None


class FileUploadHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def post(self):

		try:
			file_metas = self.request.files["file"]
		except:
			file_metas = self.request.files["filename"]

		fileName = file_metas[0].get("filename") or "unknown"
		if isSystemWindows():
			filePath = "var/tmp/" + fileName + ".XXXX" + getUuid()
		else:
			filePath = "/tmp/" + fileName + ".XXXX" + getUuid()

		for meta in file_metas:
			with open(filePath, 'wb') as up:
				up.write(meta['body'])

		retObj = buildRetObj(OCT_SUCCESS, data=filePath)
		self.write(buildReply(retObj))
		self.finish()


class ApiHandler(tornado.web.RequestHandler):
	SUPPORTED_METHODS = ("POST")

	db = None

	def __init__(self, application, request, **kwargs):
		super(ApiHandler, self).__init__(application, request, **kwargs)

		self.db = dbmysql.mysqldb()

	def checkSession(self, argObj):
		apiName = argObj.get("api")

		if (apiName.split(".")[-1] in IGNORE_SESSION_APIS):
			DEBUG("User login API, no need check session")
			return (True, {})
		
		sessionId = getSessionId(argObj)
		if (not sessionId):
			return (False, {})

		DEBUG("got session id %s" % sessionId)

		sessionObj = getSessionObj(self.db, sessionId)
		if not sessionObj:
			return (False, {})

		return (True, sessionObj)

	def getAccountInfo(self, session):

		cookie = session.get("cookie")
		if cookie:
			role = cookie["role"] or ROLE_SUPERADMIN
			if cookie.get("accountId"):
				accountId = cookie["accountId"]
			elif cookie.get("id"):
				accountId = cookie["id"]
			else:
				accountId = DEFAULT_ACCOUNT_ID
		else:
			role = 7
			accountId = DEFAULT_ACCOUNT_ID

		return role, accountId

	@tornado.web.asynchronous
	def post(self, *args, **kwargs):
		argObj = getArgObj(self.request)

		# import time
		# yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 10)

		if (not argObj.get("api")):
			ERROR("not a valid api, no api exist")
			self.write(buildFailureReply(INVALID_PARAS))
			self.finish()
			return

		(status, session) = self.checkSession(argObj)
		if (not status):
			ERROR("check session failed %s " % str(argObj))
			self.write(buildFailureReply(NO_AUTH_SKEY))
			self.finish()
			return

		(role, accountId) = self.getAccountInfo(session)
		argObj["paras"]["role"] = role

		# IF accountId Specified, just use it
		if not argObj["paras"].get("accountId"):
			argObj["paras"]["accountId"] = accountId
		
		if argObj["api"].split(".")[-1] == "APILogOut":
			argObj["centerSessionID"] = self.get_cookie("centerSessionID", "").replace("%22", "")
			DEBUG(argObj)
		
		retObj = doDispatching(argObj, session, API_PROTOS)
		self.write(buildReply(retObj))
		self.finish()


def runWebServer(addr, port):
	tornado.options.parse_command_line()
	app = Application()
	app.listen(port, addr)
	tornado.ioloop.IOLoop.instance().start()


def loadFunction(apiProto):
	serviceName = apiProto["serviceName"]
	if (not serviceName):
		apiProto["func"] = None
		return True

	funcName = serviceName.split(".")[-1]
	modulePath = serviceName.split(".")[:-1]

	try:
		service = __import__("modules." + ".".join(modulePath), fromlist=["from modules import"])
	except Exception as e:
		print(('Import module failed. [%s]' % funcName))
		print(('Import module failed. [%s]' % e))
		print(('Import module failed. [%s]' % traceback.format_exc()))
		return False

	if hasattr(service, funcName):
		funcObj = getattr(service, funcName)
		apiProto["func"] = funcObj
	else:
		print(('There is no %s in %s' % (funcName, modulePath)))
		del service
		return False

	return True


def loadAPIs():
	global API_PROTOS

	for moduleName in API_MODULE_LIST:
		module = __import__("views.api.api_" + moduleName, fromlist=["from views import"])
		for (k, v) in list(module.funcList.items()):
			key = API_PREFIX + "." + moduleName + "." + k
			if (not loadFunction(v)):
				print("load function error")
				return False
			API_PROTOS[key] = v

	print("Loaded all APIs OK!")

	return True


def loadViewAPIs():
	def copy_paras(paras):

		copyed_paras = {}
		for (k, v) in list(paras.items()):
			copyed_paras[k] = v

		append_extra_paras(copyed_paras)

		return copyed_paras

	def append_extra_paras(paras):

		if (not paras.get("paras")):
			paras["timeout"] = {
				"default": 0,
				"type": PARAM_TYPE_INT,
				"desc": "Timeout Value",
				"descCN": "超时时间，0表示同步调用",
			}

	global API_VIEW_LIST

	for moduleName in API_MODULE_LIST:

		API_VIEW_LIST[moduleName] = []

		module = __import__("views.api.api_" + moduleName, fromlist=["from views import"])
		for (k, v) in list(module.funcList.items()):
			key = API_PREFIX + "." + moduleName + "." + k
			apiProto = {
				"name": v["name"],
				"key": key,
				"paras": copy_paras(v.get("paras") or {})
			}
			API_VIEW_LIST[moduleName].append(apiProto)
		API_VIEW_LIST[moduleName].sort(key=lambda x:x["name"])

	print("Loaded all APIs OK!")


def init():
	if (not loadAPIs()):
		return False

	loadViewAPIs()

	return True


if __name__ == "__main__":

	if (float(tornado.version.split(".")[0]) < 3.0):
		print(("Version of tornado [%s] is too low, we need 3.0 above" % (tornado.version)))
		sys.exit(1)

	if (not init()):
		print("init Center API Engine Failed")
		exit(1)

	if (len(sys.argv) != 3):
		addr = LISTEN_ADDR
		port = LISTEN_PORT
	else:
		addr = sys.argv[1]
		port = int(sys.argv[2])

	global RUNNING_PORT

	RUNNING_PORT = port

	print("To start to run webServer in %s:%d" % (addr, port))

	INFO("To start to run webServer in %s:%d" % (addr, port))

	runWebServer(addr, port)
