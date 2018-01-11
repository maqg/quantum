#!/usr/bin/python3

import os
import sys
import platform
sys.path.append("../../../")

from core.log import ERROR
from utils.commonUtil import OCT_SYSTEM, transToStr


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


"""
主机名、时间，系统信息，运行时间，重启时间，最大打开文件数，最大进程数
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

	return sysinfo

"""
	def load_stat():  
		loadavg = {}  
	f = open("/proc/loadavg")  
	con = f.read().split()  
f.close()  
	loadavg['lavg_1']=con[0]  
	loadavg['lavg_5']=con[1]  
	loadavg['lavg_15']=con[2]  
	loadavg['nr']=con[3]  
	loadavg['last_pid']=con[4]  
	return loadavg

	def uptime_stat():  
		uptime = {}  
	f = open("/proc/uptime")  
	con = f.read().split()  
	f.close()  
all_sec = float(con[0])  
	MINUTE,HOUR,DAY = 60,3600,86400  
	uptime['day'] = int(all_sec / DAY )  
	uptime['hour'] = int((all_sec % DAY) / HOUR)  
	uptime['minute'] = int((all_sec % HOUR) / MINUTE)  
	uptime['second'] = int(all_sec % MINUTE)  
	uptime['Free rate'] = float(con[1]) / float(con[0])  
	return uptime  
"""

if __name__ == "__main__":
	info = get_sys_info()
	print(transToStr(info))
