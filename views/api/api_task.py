# -*- coding: utf-8 -*-

from views.api.api import *

moduleName = "task"

funcList = {

	"APIShowTask": {
		"name": "获取单个API或任务信息",
		"serviceName": "api.api_web.web_get_api",
		"paras": {
			"id": {
				"type": PARAM_TYPE_STRING,
				"desc": "Task or API's UUID",
				"descCN": "API或任务的UUID",
				"default": "NotNull"
			}
		}
	},

	"APIShowAllTask": {
		"name": "获取所有API或任务信息",
		"serviceName": "api.api_web.web_get_apis",
		"paras": {
			"start": {
				"type": PARAM_TYPE_INT,
				"desc": "start from",
				"descCN": "开始位置",
				"default": 0
			},
			"limit": {
				"type": PARAM_TYPE_INT,
				"desc": "limitation",
				"descCN": "获取条目",
				"default": 15
			},
			"keyword": {
				"type": PARAM_TYPE_STRING,
				"desc": "keywords",
				"descCN": "关键字",
				"default": ""
			},
			"apiName": {
				"type": PARAM_TYPE_STRING,
				"desc": "Api Name",
				"descCN": "Api Name",
				"default": ""
			},
			"type": {
				"type": PARAM_TYPE_STRING,
				"desc": "api or task",
				"descCN": "API类型，api or task",
				"default": ""
			},
			"serverTaskId": {
				"type": PARAM_TYPE_STRING,
				"desc": "Server Task Id",
				"descCN": "Server Task Id",
				"default": ""
			}
		}
	}
}
