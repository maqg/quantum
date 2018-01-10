#!/usr/bin/python3

from core.log import ERROR
from utils.commonUtil import OCT_SYSTEM


def get_cpu_number():
	ret, data = OCT_SYSTEM("cat /proc/cpuinfo | grep processor | wc -l")
	if ret != 0:
		ERROR("get cpu number error")
		return 1
	
	return int(data)


def get_cpu_info():
	info = {}
	info["ncpu"] = get_cpu_number()
	
	return info


if __name__ == "__main__":
	info = get_cpu_info()
	print(info)
