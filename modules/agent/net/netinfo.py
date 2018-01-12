#!/usr/bin/python3

import time
import sys
sys.path.append("../../../")

from core.log import ERROR
from utils.commonUtil import OCT_SYSTEM, transToStr


NETINFO_FILE = "/proc/net/dev"

def get_net_stat():

	netstat = {}

	fd = open(NETINFO_FILE, "r")
	if not fd:
		ERROR("open file %s error\n" % NETINFO_FILE)
		return netstat


	line = fd.readline()
	while line:

		if ": " in line:
			segs = line.replace("\t", "").replace("\n", "").split(": ")

			interface = segs[0].replace(" ", "")

			data = segs[1].split()
			inbytes = data[0]
			outbytes = data[8]

			netstat[interface] = {"inbytes": inbytes, "outbytes": outbytes}

		line = fd.readline()

	fd.close()
	return netstat

#unit bps, bits per second
def get_net_info():

	netinfo = []

	netstat_before = get_net_stat()

	time.sleep(5)

	netstat_after = get_net_stat()

	for k in netstat_before:
		inspeed = (int(netstat_after[k]["inbytes"]) - int(netstat_before[k]["inbytes"])) / 5 * 8

		outspeed = (int(netstat_after[k]["outbytes"]) - int(netstat_before[k]["outbytes"])) / 5 * 8

		tmp = {
			"interface": k,
			"incoming": int(inspeed), 
			"outgoing": int(outspeed)
		}
		
		netinfo.append(tmp)

	return netinfo


if __name__ == "__main__":

	netinfo = get_net_info()
	print(transToStr(netinfo))
