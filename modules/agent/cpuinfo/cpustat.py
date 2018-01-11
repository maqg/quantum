#!/usr/bin/python3

import sys
sys.path.append("../../../")

from core.log import ERROR
from utils.commonUtil import OCT_SYSTEM, transToStr


HW_CPUINFO_FILE = "/proc/cpuinfo"


def parse_cpu_stats():

	stats = []

	return stats


def get_cpu_stats():
	info = {}

	cpuinfo = parse_cpu_stats()
	if not cpuinfo:
		ERROR("parse cpu info from cpuinfo file error")
		return info

	return info


if __name__ == "__main__":
	info = get_cpu_stats()
	print(transToStr(info))
