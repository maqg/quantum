# -*- coding: utf-8 -*-
from views.api.api import PARAM_TYPE_STRING, PARAM_NOT_NULL, PARAM_TYPE_INT

moduleName = "agent"

funcList = {
	"APIAddAgent": {
		"name": "添加代理端",
		"serviceName": "agentmanage.agentmanage_web.web_add_agent",
		"paras": {
			"name": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "名称",
				"default": PARAM_NOT_NULL
			},
			"address": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "Agent Address",
				"default": PARAM_NOT_NULL
			}
		}
	},
	
	"APIShowAgent": {
		"name": "查看单个代理端",
		"serviceName": "agentmanage.agentmanage_web.web_show_agent",
		"paras": {
			"id": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "Agent ID",
				"default": PARAM_NOT_NULL
			}
		}
	},
	
	"APIRemoveAgent": {
		"name": "删除代理端",
		"serviceName": "agentmanage.agentmanage_web.web_remove_agent",
		"paras": {
			"id": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "Agent ID",
				"default": PARAM_NOT_NULL
			}
		}
	},
	
	"APIShowAllAgent": {
		"name": "查看所有代理端",
		"serviceName": "agentmanage.agentmanage_web.web_show_all_agent",
		"paras": {
			"sName": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "名称关键字",
				"default": ""
			},
			"sHostName": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "主机名关键字",
				"default": ""
			},
			"start": {
				"type": PARAM_TYPE_INT,
				"desc": "",
				"descCN": "开始位置",
				"default": 0
			},
			"limit": {
				"type": PARAM_TYPE_INT,
				"desc": "",
				"descCN": "获取条目",
				"default": 15
			}
		}
	},
}
