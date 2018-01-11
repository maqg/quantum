#!/usr/bin/python3

import sys
sys.path.append("../../../")

from core.log import ERROR
from utils.commonUtil import OCT_SYSTEM, transToStr


HW_CPUINFO_FILE = "/proc/cpuinfo"


def parse_hd_cpuinfo():

	cpus = []

	fd = open(HW_CPUINFO_FILE, "r")
	if not fd:
		ERROR("open file %s error\n", HW_CPUINFO_FILE)
		return cpus

	cpu = {}
	line = fd.readline()
	while line:

		segs = line.replace("\t","").replace("\n", "").split(": ")
		if len(segs) != 2:
			line = fd.readline()
			continue

		if segs[0] == "processor":
			cpu["processor"] = int(segs[1])
		elif segs[0] == "vendor_id":
			cpu["vendorId"] = segs[1]
		elif segs[0] == "model name":
			cpu["modelName"] = segs[1]
		elif segs[0] == "cpu MHz":
			cpu["cpuHz"] = int(float(segs[1]) * 1000)
		elif segs[0] == "cache size":
			cpu["cacheSize"] = int(segs[1].split(" ")[0]) # kB
		elif segs[0] == "cpu cores":
			cpu["cores"] = int(segs[1])
		elif segs[0] == "flags": # end of cpuinfo
			cpus.append(cpu)
			cpu["flags"] = segs[1]
			cpu = {}

		line = fd.readline()

	fd.close()

	return cpus


def get_cpu_info():
	info = {}

	cpuinfo = parse_hd_cpuinfo()
	if not cpuinfo:
		ERROR("parse cpu info from cpuinfo file error")
		return info

	info["ncpu"] = len(cpuinfo)
	info["modelName"] = cpuinfo[0]["modelName"]
	info["cpuHz"] = cpuinfo[0]["cpuHz"]
	info["coresPerCpu"] = cpuinfo[0]["cores"]
	info["cpus"] = cpuinfo
	
	return info


if __name__ == "__main__":
	info = get_cpu_info()
	print(transToStr(info))
