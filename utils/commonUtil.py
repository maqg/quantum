#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import json
import os
import socket
import struct
import time
import platform
import uuid
from binascii import crc32
from random import Random

from core.err_code import err_desc_en, err_desc_ch
from utils.timeUtil import get_current_time

DEBIAN_VERSION_FILE = "/etc/debian_version"
CENTOS_VERSION_FILE = "/etc/centos-release"
REDHAT_VERSION_FILE = "/etc/redhat-release"

PLATFORM_DEBIAN7 = "debian7"
PLATFORM_DEBIAN9 = "debian9"
PLATFORM_REDCENT6 = "redcent6"
PLATFORM_REDCENT7 = "redcent7"


SYSTEM_TYPE_WINDOWS = "Windows"
SYSTEM_TYPE_MAC = "Darwin"
SYSTEM_TYPE_LINUX = "Linux"


# generate random str which len is randomlength.
def random_str(randomlength=8):
	str = ''
	chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str += chars[random.randint(0, length)]
	
	return str


def CRC32(crcStr):
	return crc32(crcStr.encode()) & 0xFFFFFFFF


def listFiles(fileDir, keyword=None):
	fileList = []
	
	for file in os.listdir(fileDir):
		if (not os.path.isdir(file) and (not keyword or file.find(keyword) != -1)):
			fileList.append(file)
	
	return fileList


def getPlatform():
	if (os.path.exists(DEBIAN_VERSION_FILE)):
		fd = open(DEBIAN_VERSION_FILE, "r")
		line = fd.readline()
		version = line.split(".")[0]
		fd.close()
		return "debian" + version
	elif (os.path.exists(CENTOS_VERSION_FILE)):
		filePath = CENTOS_VERSION_FILE
	else:
		filePath = REDHAT_VERSION_FILE
	
	fd = open(filePath, "r")
	line = fd.readline()
	version = line.split(".")[0].split(" ")[-1]
	fd.close()
	
	return "readcent" + version


def isPlatformDebian7():
	return getPlatform() == PLATFORM_DEBIAN7


def isPlatformDebian9():
	return getPlatform() == PLATFORM_DEBIAN9


def ip2long(ip):
	packedIP = socket.inet_aton(ip)
	return struct.unpack("!L", packedIP)[0]


def long2ip(ip_long):
	return socket.inet_ntoa(struct.pack("!L", ip_long))


def removeFile(filepath):
	if (filepath == None or os.path.exists(filepath) == False):
		return
	
	os.remove(filepath)


def buildRetMsg(errorCode, data=None, errorLog=None):
	if (not errorLog):
		return (errorCode, data)
	else:
		return (errorCode, data, errorLog)


def buildRetObj(errorCode, data=None, errorLog=""):
	return {
		"RetCode": errorCode,
		"RetObj": data,
		"ErrorLog": errorLog
	}


def toString(src, encoding="utf-8"):
	if (type(src) == str):
		try:
			return src.encode(encoding)
		except:
			return octUnicode(src).encode(encoding)
	else:
		return src


def transToObj(string):
	if (string == None):
		return None
	
	if (type(string) != type("a") and type(string) != type('a')):
		string = string.encode()
	
	if (len(string) < 2):
		return None
	
	try:
		obj = json.loads(string, encoding="utf-8")
	except:
		obj = {}
	
	return obj


def getStrTime(milisecs=None):
	if not milisecs:
		milisecs = get_current_time()
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(milisecs) / 1000))


def isSystemWindows():
	if (platform.system() == "Windows"):
		return True
	else:
		return False


def getSystemType():
	return platform.system()


def transToStr(obj, indent=False):
	if (indent != False):
		return json.dumps(obj, ensure_ascii=False, indent=indent)
	else:
		return json.dumps(obj, ensure_ascii=False)


def OCT_SYSTEM(formatStr, arg=None):
	TEMPFILE_NAME = "/tmp/OCTTEMP_FILE_%ld%s" % (get_current_time(), getUuid())
	
	if (arg):
		CMD = formatStr % arg
	else:
		CMD = formatStr
	
	CMD += " > %s" % (TEMPFILE_NAME)
	ret = os.system(CMD)
	
	fp = open(TEMPFILE_NAME, 'r')
	if (fp == None):
		return (ret >> 8 & 0XFF, None)
	
	data = fp.read()
	fp.close()
	os.remove(TEMPFILE_NAME)
	
	if (len(data) == 0):
		return (ret >> 8 & 0XFF, None)
	
	if (data[-1] == '\n'):
		data = data[:-1]  # to remove last "\n"
	
	if (len(data) == 0):
		data = None
	
	return (ret >> 8 & 0XFF, data)


def OCT_PIPERUN(cmd):
	import subprocess
	
	if (cmd == None):
		return (0, None)
	
	args = cmd.split()
	p = subprocess.Popen(args, close_fds=True, stdout=subprocess.PIPE,
	                     stderr=subprocess.PIPE, shell=False)
	p.wait()
	
	ret = p.returncode
	msg = p.stdout.read()
	
	return (ret, msg)


def getUuid(spilt=None):
	if (spilt):
		return str(uuid.uuid4())
	else:
		x = uuid.uuid4().hex
		return x


def octUnicode(src):
	if (type(src) == str):
		return src
	else:
		try:
			return str(src, "utf-8")
		except:
			return src


def fileToObj(filePath):
	if (not os.path.exists(filePath)):
		print(("file %s not exist" % (filePath)))
		return None
	
	fd = open(filePath, "r", encoding="utf-8")
	if (not fd):
		print(("open file %s error" % (filePath)))
		return None
	
	obj = transToObj(fd.read())
	
	fd.close()
	
	return obj


def getErrorMsgCN(error):
	return err_desc_ch.get(error) or ""


def getErrorMsg(error):
	return err_desc_en.get(error) or ""


def b64_decode(src):
	if not src:
		return ""
	try:
		return base64.b64decode(src.encode()).decode()
	except:
		return ""


def b64_encode(src):
	if not src:
		return ""
	return base64.b64encode(src.encode()).decode()


def FORMAT(total, free):
	if not total:
		return format(0, ".2%")
	return format(free / total, ".2%")
