# -*- coding: utf-8 -*-

from views.api.api import *

moduleName = "account"

funcList = {

	"APIAddAccount": {
		"name": "添加账号",
		"serviceName": "account.account_web.web_add_user",
		"paras": {
			"account": {
				"type": PARAM_TYPE_STRING,
				"desc": "Account Name",
				"descCN": "账号名称",
				"default": "NotNull"
			},
			"password": {
				"type": PARAM_TYPE_STRING,
				"desc": "Password in PlainText mode",
				"descCN": "密码（明文），base64ed",
				"default": "NotNull"
			},
			"email": {
				"type": PARAM_TYPE_STRING,
				"desc": "email address for account",
				"descCN": "账号名称",
				"default": ""
			},
			"phoneNumber": {
				"type": PARAM_TYPE_STRING,
				"desc": "phone number for account",
				"descCN": "电话号码",
				"default": ""
			}
		}
	},

	"APILoginByAccount": {
		"name": "根据账号登录",
		"serviceName": "account.account_web.web_login",
		"paras": {
			"account": {
				"type": PARAM_TYPE_STRING,
				"desc": "Account Name",
				"descCN": "账号名称",
				"default": "NotNull"
			},
			"password": {
				"type": PARAM_TYPE_STRING,
				"desc": "Password in PlainText mode",
				"descCN": "密码（明文，使用Base64编码）",
				"default": "NotNull"
			}
		}
	},
	
	"APIShowAccount": {
		"name": "获取单个账号信息",
		"serviceName": "account.account_web.web_get_user",
		"paras": {
			"id": {
				"type": PARAM_TYPE_STRING,
				"desc": "Account's UUID",
				"descCN": "账号的UUID",
				"default": "NotNull"
			}
		}
	},

	"APIShowAllAccount": {
		"name": "获取所有账号信息",
		"serviceName": "account.account_web.web_get_user",
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
			}
		}
	},

	"APIShowAccountList": {
		"name": "获取账号列表",
		"serviceName": "account.account_web.web_get_userlist",
		"paras": {}
	},

	"APIDeleteAccount": {
		"name": "删除单个账号信息",
		"serviceName": "account.account_web.web_del_user",
		"paras": {
			"id": {
				"type": PARAM_TYPE_STRING,
				"desc": "Account's UUID",
				"descCN": "账号的UUID",
				"default": "NotNull"
			}
		}
	},

	"APIResetAccountPassword": {
		"name": "重置账号密码",
		"serviceName": "account.account_web.web_reset_password",
		"paras": {
			"id": {
				"type": PARAM_TYPE_STRING,
				"desc": "Account's UUID",
				"descCN": "账号的UUID",
				"default": "NotNull"
			},
			"password": {
				"type": PARAM_TYPE_STRING,
				"desc": "Account's new password",
				"descCN": "密码（明文，使用Base64编码）",
				"default": "NotNull"
			}
		}
	},

	"APIUpdateAccountPassword": {
		"name": "更新账号密码",
		"serviceName": "account.account_web.web_modify_password",
		"paras": {
			"id": {
				"type": PARAM_TYPE_STRING,
				"desc": "Account's UUID",
				"descCN": "账号的UUID",
				"default": "NotNull"
			},
			"newPassword": {
				"type": PARAM_TYPE_STRING,
				"desc": "Account's new password",
				"descCN": "新密码，base64ed",
				"default": "NotNull"
			},
			"oldPassword": {
				"type": PARAM_TYPE_STRING,
				"desc": "Account's old password",
				"descCN": "原始密码，base64ed",
				"default": "NotNull"
			}
		}
	},

	"APIUpdateAccount": {
		"name": "编辑账号信息",
		"serviceName": "account.account_web.web_update_user",
		"paras": {
			"id": {
				"type": PARAM_TYPE_STRING,
				"desc": "Account's UUID",
				"descCN": "账号的UUID",
				"default": "NotNull"
			},
			"email": {
				"type": PARAM_TYPE_STRING,
				"desc": "email address for account",
				"descCN": "账号名称",
				"default": ""
			},
			"phoneNumber": {
				"type": PARAM_TYPE_STRING,
				"desc": "phone number for account",
				"descCN": "电话号码",
				"default": ""
			},
			"desc": {
				"type": PARAM_TYPE_STRING,
				"desc": "",
				"descCN": "描述",
				"default": ""
			}
		}
	},

	"APILogOut": {
		"name": "退出登录",
		"serviceName": "account.account_web.web_logout",
		"paras": {
			"sessionUuid": {
				"type": PARAM_TYPE_STRING,
				"desc": "UUID of Account to Logou",
				"descCN": "账号UUID",
				"default": "NotNull"
			}
		}
	}
}
