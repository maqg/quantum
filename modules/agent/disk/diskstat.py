#!/usr/bin/python3

import sys
sys.path.append("../../../")
import os

from core.log import ERROR
from utils.commonUtil import OCT_SYSTEM, transToStr

IOSTAT_TOOL = "/usr/bin/iostat"

def parse_disk_stat():
	info = []

	if not os.path.exists(IOSTAT_TOOL):
		ERROR("iostat tool not installed")
		return stat

	ret, data = OCT_SYSTEM("iostat -d -k 1 5")
	if ret != 0:
		ERROR("exec iostat command error")
		return stat
		
	paras = data.split("Device:")[1:]

	dev_num = len([tmp for tmp in paras[0].split("\n")[1:] if tmp])

	devices = []
	for i in range(dev_num):
		device = []
		for para in paras:
			lines = [tmp for tmp in para.split("\n")[1:] if tmp]
			device.append(lines[i])

		devices.append(device)

	for device in devices:

		tps_total = 0
		read_total = 0
		write_total = 0
		for i in device:
			tps_total += float(i.split()[1])
			read_total += float(i.split()[2])
			write_total += float(i.split()[3])
			
		dev = {
			"device": i.split()[0],
			"tps": round(tps_total/5, 2),
			"readSpeed": round(read_total/5, 2),  # unit KB/s
			"writeSpeed": round(write_total/5, 2) # unit KB/s
		}

		info.append(dev)

	return info

def get_disk_stat():
	disk_stat = {}

	stat = parse_disk_stat()
	if not stat:
		ERROR("parse disk stat info use iostat command error")
		return disk_stat

	disk_stat["ndev"] = len(stat)
	disk_stat["devs"] = stat

	return disk_stat

if __name__ == "__main__":
	diskstat = get_disk_stat()
	print(transToStr(diskstat))
