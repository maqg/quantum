#!/usr/bin/python3

import sys
sys.path.append("../../../")

from core.log import ERROR
from utils.commonUtil import OCT_SYSTEM, transToStr


MEMINFO_CMD = "/usr/bin/vmstat -s | grep -w K"


def get_mem_info():
	mem_flags = {
		"totalmemory": "total",
		"usedmemory": "used",
		"available": "available",
		"inactivememory": "cache",
		"freememory": "free",
		"buffermemory": "buffer",
		"swapcache": "swapCache",
		"totalswap": "totalSwap",
		"usedswap": "usedSwap",
		"freeswap": "freeSwap"
	}

	info = {}

	ret, data = OCT_SYSTEM(MEMINFO_CMD)
	if ret != 0:
		ERROR("get meminfo error with cmd %s, %d\n" % (MEMINFO_CMD, ret))
		return info

	lines = data.split("\n")
	for line in lines:
		segs = line.replace(" ", "").split("K")
		flag = mem_flags.get(segs[1])
		if not flag:
			continue
		info[flag] = int(segs[0]) * 1024

	info["shared"] = 0 # TBD
	info["available"] = info["free"] + info["buffer"]

	if not info["totalSwap"]:
		info["pfreeSwap"] = 0
		info["pusedSwap"] = 0
	else:
		info["pfreeSwap"] = round(info["freeSwap"] / info["totalSwap"] * 100.0, 2)
		info["pusedSwap"] = round(info["usedSwap"] / info["totalSwap"] * 100.0, 2)

	if not info["total"]:
		info["pused"] = 0
		info["pavailable"] = 0
	else:
		info["pused"] = round((info["total"] - info["free"]) / info["total"] * 100.0, 2)
		info["pavailable"] = round(info["available"] / info["total"] * 100.0, 2)

	return info


if __name__ == "__main__":
	info = get_mem_info()
	print(transToStr(info))
