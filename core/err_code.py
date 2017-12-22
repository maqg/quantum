# -*- coding: utf-8 -*-

OCT_SUCCESS = 0
NOT_ENOUGH_PARAS = 1
TOO_MANY_PARAS = 2
INVALID_PARAS = 3
XML_ERR = 4
EXEC_CMD_ERR = 5
COMMON_ERR = 6
SEGMENT_NOT_EXIST = 7
SEGMENT_ALREADY_EXIST = 8
FILE_NOT_EXIST = 9
TIME_OUT_ERR = 10
CHECK_ENV_ERR = 11
SEND_MSG_FAILED = 12
INCOMPATIBLE_CONFIG = 13
PERMISSION_NOT_ENOUGH = 14
CONNECT_SERVER_ERR = 15
DB_ERR = 16
CONFIG_NOT_EXIST = 256
LAZY_PROGRAMMER = 257
NO_SUCH_CMD = 258
OPE_FORBID = 259
INVALID_CONFIG_FILE = 260
CONFIG_ALREADY_EXIST = 261
SYSCALL_ERR = 262
SYSTEM_ERR = 263
NO_AUTH_SKEY = 264
WRONG_AUTH_SKEY = 265
WRONG_AUTH_TIMESTAMP = 266
USER_NOT_EXIST = 512
USER_ALREADY_EXIST = 513
USER_PASSWD_ERR = 514

err_desc_ch = {
	OCT_SUCCESS: "执行成功",
	NOT_ENOUGH_PARAS: "参数不够",
	TOO_MANY_PARAS: "参数太多",
	INVALID_PARAS: "参数错误",
	XML_ERR: "XML解析错误",
	EXEC_CMD_ERR: "命令执行错误",
	COMMON_ERR: "通用错误",
	SEGMENT_NOT_EXIST: "字段不存在",
	SEGMENT_ALREADY_EXIST: "字段已经存在",
	FILE_NOT_EXIST: "文件不存在",
	TIME_OUT_ERR: "等待超时",
	CHECK_ENV_ERR: "环境检测失败",
	SEND_MSG_FAILED: "发送消息失败",
	INCOMPATIBLE_CONFIG: "不兼容的配置",
	PERMISSION_NOT_ENOUGH: "权限不足",
	CONNECT_SERVER_ERR: "连接服务器错误",
	DB_ERR: "数据库错误",
	CONFIG_NOT_EXIST: "配置文件不存在",
	LAZY_PROGRAMMER: "此功能未实现",
	NO_SUCH_CMD: "没有此命令",
	OPE_FORBID: "禁止此操作",
	INVALID_CONFIG_FILE: "配置文件不合法",
	CONFIG_ALREADY_EXIST: "配置文件已经存在",
	SYSCALL_ERR: "系统调用错误",
	SYSTEM_ERR: "系统错误",
	NO_AUTH_SKEY: "没有URL认证密码",
	WRONG_AUTH_SKEY: "错误的URL认证密码",
	WRONG_AUTH_TIMESTAMP: "错误的URL认证时间戳，请同步你的客户机时间",
	USER_NOT_EXIST: "用户不存在",
	USER_ALREADY_EXIST: "用户已经存在",
	USER_PASSWD_ERR: "用户名或密码错误",
}

err_desc_en = {
	OCT_SUCCESS: "Command success",
	NOT_ENOUGH_PARAS: "Not enough parameters",
	TOO_MANY_PARAS: "Too many parameters",
	INVALID_PARAS: "Invalid parameters",
	XML_ERR: "XML Error",
	EXEC_CMD_ERR: "Execute Command Error",
	COMMON_ERR: "Common error",
	SEGMENT_NOT_EXIST: "Segment not exist",
	SEGMENT_ALREADY_EXIST: "Segment already exist",
	FILE_NOT_EXIST: "File not exist",
	TIME_OUT_ERR: "Time out error",
	CHECK_ENV_ERR: "check env err",
	SEND_MSG_FAILED: "send msg failed",
	INCOMPATIBLE_CONFIG: "incompatible config",
	PERMISSION_NOT_ENOUGH: "Permissions Not Enough",
	CONNECT_SERVER_ERR: "Connect to Server Error",
	DB_ERR: "Database Error",
	CONFIG_NOT_EXIST: "Config file not exist",
	LAZY_PROGRAMMER: "Not Complete This Function",
	NO_SUCH_CMD: "No This Commond",
	OPE_FORBID: "Forbid this peration",
	INVALID_CONFIG_FILE: "Invalid config file",
	CONFIG_ALREADY_EXIST: "Config file already exists",
	SYSCALL_ERR: "System call error",
	SYSTEM_ERR: "System error",
	NO_AUTH_SKEY: "No skey specified",
	WRONG_AUTH_SKEY: "Wrong auth skey",
	WRONG_AUTH_TIMESTAMP: "Wrong auth timestamp,please sync your system time",
	USER_NOT_EXIST: "User not exist",
	USER_ALREADY_EXIST: "User already exist",
	USER_PASSWD_ERR: "Password and username dont match",
}

def print_retmsg(buff):
	print('\n%% %s\n' % buff)