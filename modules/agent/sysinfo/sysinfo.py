#!/usr/bin/python3

import os
import sys
import platform
sys.path.append("../../../")

from core.log import ERROR
from utils.commonUtil import OCT_SYSTEM, transToStr
from utils.timeUtil import get_current_time, getStrTime


def get_cmdline():
	CMDLINE_FILE = "/proc/cmdline"

	fd = open(CMDLINE_FILE, "r")
	if not fd: 
		return "UNKNOWN"

	cmdline = fd.readline().split("\n")[0]

	fd.close()

	return cmdline


def get_debian_version():
	DEBIAN_VERSION_FILE = "/etc/debian_version"
	if not os.path.exists(DEBIAN_VERSION_FILE):
		return "UNKNOWN"

	ret, data = OCT_SYSTEM("cat %s" % DEBIAN_VERSION_FILE)
	if ret != 0:
		return "UNKNOWN"

	return data.split("\n")[-1]


def get_max_open_files():
	ret, data = OCT_SYSTEM("ulimit -n")
	if ret != 0:
		return "ulimited"
	return data.split("\n")[0]


def get_max_processes():
	ret, data = OCT_SYSTEM("ulimit -p")
	if ret != 0:
		print(ret)
		print(data)
		return "ulimited"
	return data.split("\n")[0]


def get_kernel_info():
	ret, data = OCT_SYSTEM("uname -r -v -m")
	if ret != 0:
		return "UNKNOWN"
	return data.split("\n")[0]


def get_cpu_cores():
	ret, data = OCT_SYSTEM("cat /proc/cpuinfo | grep -w processor | wc -l")
	if ret != 0:
		ERROR("get processor number error")
		return 1

	return int(data.replace("\n", ""))


def get_uptime():

	uptime = {}

	UPTIME_FILE = "/proc/uptime"
	fd = open(UPTIME_FILE, "r")
	if not fd:
		return None

	data = fd.readline().split()

	seconds = int(float(data[0]))
	freeSeconds = int(float(data[1]))

	MINUTE, HOUR, DAY = 60, 3600, 86400
	uptime['day'] = int(seconds / DAY )
	uptime['hour'] = int((seconds % DAY) / HOUR)
	uptime['minute'] = int((seconds % HOUR) / MINUTE)
	uptime['second'] = int(seconds % MINUTE)
	uptime['seconds'] = int(seconds)

	ncores = get_cpu_cores()

	uptime['freeRate'] = round(freeSeconds / (seconds * ncores) * 100.0, 2)

	return uptime  


"""
{
	"os": "Debianxxxx",
	"kernel": "",
	"cmdline": "",
	"hostname": "fff",
	"sysTime": "fffff",
	"upTime": "",
	"lastRebootTime": "",
	"maxOpenFiles": 10000,
	"maxUserProcesses": 10000,
}
"""
def get_sys_info():
	sysinfo = {
		"os": platform.system() + " Debian " + get_debian_version(),
		"kernel": get_kernel_info(),
		"cmdline": get_cmdline(),
		"maxOpenFiles": get_max_open_files(),
		"maxUserProcesses": get_max_processes(),
		"hostname": platform.node()
	}

	uptime = get_uptime()
	if not uptime:
		ERROR("got uptime error")
		return sysinfo

	sysinfo["upTime"] = "%d 天 %d 时 %d 分 %d 秒" % (uptime["day"],
			uptime["hour"], uptime["minute"], uptime["second"])
	sysinfo["freeRate"] = uptime["freeRate"]

	rebootTime = get_current_time() - uptime["seconds"] * 1000
	sysinfo["lastRebootTime"] = getStrTime(rebootTime)

	return sysinfo

if __name__ == "__main__":
	info = get_sys_info()
	print(transToStr(info))
