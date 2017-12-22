# -*- coding: utf-8 -*-

from modules.api.api_web import web_get_api


def getApiResult(db, argObj):
	return web_get_api(db, {}, argObj)