# -*- coding: utf-8 -*-

from modules.api.api import *
from core.err_code import OCT_SUCCESS
from utils.commonUtil import buildRetObj


def web_get_apis(db, env, arg):
    ret, data = getApis(db, arg)
    return buildRetObj(ret, data)

def web_get_api(db, env, arg):
    apiId = arg["paras"].get('id')
    if not apiId:
        return buildRetObj(SEGMENT_NOT_EXIST, None)

    api = getApi(db, apiId)
    if (not api):
        return buildRetObj(SEGMENT_NOT_EXIST, None)

    return buildRetObj(OCT_SUCCESS, api.toObj())

def web_delete_api(db, env, arg):
    ret = deleteApi(db, arg)
    return buildRetObj(ret, None)

def web_add_api(db, env, arg):
    paras = arg["paras"]
    (ret, data) = addApi(db, arg, paras)
    return buildRetObj(ret, data)

def web_add_apiresult(db, env, arg, result=None):
    (ret, data) = addApiResult(db, env, arg, result)
    return buildRetObj(ret, data)