#!/usr/bin/python3

import sys
sys.path.append("../../../")

from core.log import ERROR
from utils.commonUtil import OCT_SYSTEM, transToStr

def parse_disk_info():
	diskinfo = {}

	ret, data = OCT_SYSTEM("df")
	if ret != 0:
		ERROR("exec cmdline df error")
		return diskinfo

	data = data.split("\n")[1:]
	for i in data:

		filesystem = i.split()[0]
		disk = {
			"total": int(i.split()[1]),
			"used": int(i.split()[2]),
			"available": int(i.split()[3]),
			"pused": i.split()[4],
			"mount": i.split()[5]
		}
		diskinfo[filesystem] = disk

	return diskinfo

def get_disk_info():

	diskinfo = parse_disk_info()
	if not diskinfo:
		ERROR("parse disk info from df command error")
		return info

	return diskinfo


if __name__ == "__main__":
	diskinfo = get_disk_info()
	print(transToStr(diskinfo))
