#!/usr/bin/python3

import os
import sys
sys.path.append("../../../")

from core.log import ERROR
from utils.commonUtil import OCT_SYSTEM, transToStr


HW_CPUINFO_FILE = "/proc/cpuinfo"

def get_cpu_time():
	timeinfo = {
		"user": 0,
		"system": 0,
		"nice": 0,
		"idle": 100.00,
		"steal": 0,
		"iowait": 0,
	}
	IOSTAT_TOOL = "/usr/bin/iostat"
	if not os.path.exists(IOSTAT_TOOL):
		ERROR("iostat tool not installed")
		return timeinfo

	ret, data = OCT_SYSTEM("%s -c 1 5" % IOSTAT_TOOL)
	if ret != 0:
		ERROR("get iostat info error %d" % ret)
		return timeinfo

	user = 0
	nice = 0
	system = 0
	iowait = 0
	steal = 0
	idle = 0
	lines = data.split("\n")
	for line in lines:
		segs = line.split()
		if len(segs) != 6 or not segs[0] or segs[0] == "Linux":
			continue

		user = user + float(segs[0])
		nice = nice + float(segs[1])
		system = system + float(segs[2])
		iowait = iowait + float(segs[3])
		steal = steal + float(segs[4])
		idle = idle + float(segs[5])

	timeinfo["user"] = round(user / 5, 2)
	timeinfo["nice"] = round(nice / 5, 2)
	timeinfo["system"] = round(system / 5, 2)
	timeinfo["iowait"] = round(iowait / 5, 2)
	timeinfo["steal"] = round(steal / 5, 2)
	timeinfo["idle"] = round(idle / 5, 2)

	return timeinfo


def get_irq_info():
	irq = {
		"irq": 0,
		"softIrq": 0,
	}
	DSTAT_TOOL = "/usr/bin/dstat"
	if not os.path.exists(DSTAT_TOOL):
		ERROR("dstat tool not installed")
		return irq

	ret, data = OCT_SYSTEM("%s -c --nocolor --noheaders 1 5" % DSTAT_TOOL)
	if ret != 0:
		ERROR("get dstat info error %d" % ret)
		return irq

	hi = 0
	si = 0
	lines = data.split("\n")
	for line in lines:
		segs = line.split()
		if len(segs) != 6 or segs[0] == "usr":
			continue
		hi = hi + int(segs[4])
		si = si + int(segs[5])

	irq["irq"] = round(hi / 5, 2)
	irq["softIrq"] = round(si / 5, 2)

	return irq


def get_loadavg():  
	loadavg = {}

	fd = open("/proc/loadavg", "r")
	data = fd.read().split()
	fd.close()

	loadavg['loadAvg1'] = round(float(data[0]) * 100.0, 2)
	loadavg['loadAvg5'] = round(float(data[1]) * 100.0, 2)
	loadavg['loadAvg15'] = round(float(data[2]) * 100.0, 2)

	return loadavg

"""
{
	"user": 1.1,
	"nice": 1,
	"iowait": 1,
	"system": 1,
	"steal": 1,
	"idle": 0,
	"irq": 0,
	"softIrq": 1,
	"loadAvg1": 1, # load avarage per 1 minute
	"loadAvg5": 1, # load avarage per 5 minute
	"loadAvg15": 1, # load avarage per 15 minute
	"contextps": 1, # Context switches per second
	"interruptps": 1 # Interrupts switches per second
}
"""
def get_cpu_stats():
	stats = {}

	loadavg = get_loadavg()
	if not loadavg:
		ERROR("parse cpu info from cpuinfo file error")
		return stats

	for (k, v) in loadavg.items():
		stats[k] = v

	irq = get_irq_info()
	for (k, v) in irq.items():
		stats[k] = v

	cputime = get_cpu_time()
	for (k, v) in cputime.items():
		stats[k] = v

	return stats


if __name__ == "__main__":
	info = get_cpu_stats()
	print(transToStr(info))
