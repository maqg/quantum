# -*- coding: utf-8 -*-
from views.api.api import PARAM_TYPE_STRING, PARAM_NOT_NULL, PARAM_TYPE_INT

moduleName = "sync"

funcList = {
	"APISyncMsg": {
		"name": "同步信息",
		"serviceName": "syncmsg.syncmsg_web.web_syncmsg",
		"paras": {
			"type": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "类型如NetInfo,DiskInfo,CpuInfo,MemoryInfo,SysInfo",
				"default": PARAM_NOT_NULL
			},
			"agentId": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "Agent ID",
				"default": PARAM_NOT_NULL
			},
			"data": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "消息内容",
				"default": PARAM_NOT_NULL
			}
		}
	},
	
	"APIShowMsg": {
		"name": "查看信息",
		"serviceName": "syncmsg.syncmsg_web.web_show_syncmsg",
		"paras": {
			"type": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "类型如NetInfo,DiskInfo,CpuInfo,MemoryInfo,BasicInfo",
				"default": ""
			},
			"keyword": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "过滤关键字",
				"default": ""
			},
			"agent": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "Agent地址或主机名",
				"default": ""
			},
			"agentId": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "Agent ID",
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
