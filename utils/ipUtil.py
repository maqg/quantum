from IPy import IP


# eg. ip = 10.10.200.209, netmask = 255.255.0.0, then return IP('10.10.0.0/16').
def make_net(ip, netmask):
	return IP(ip).make_net(netmask)


# paras: 10.10.0.0/16
def BroadcastAddr(net):
	return IP(net).broadcast()


# paras: 10.10.0.0/16
def NetworkAddr(net):
	return IP(net).net()


# start-end/netmask to total
def IPCapacity(start, end, netmask):
	startInt = IP2Int(start)
	endInt = IP2Int(end)

	total = endInt - startInt + 1
	
	network = make_net(ip=startInt, netmask=netmask)
	broadcastAddr = BroadcastAddr(net=network)
	networkAddr = NetworkAddr(net=network)
	
	if (IP2Int(broadcastAddr) in range(startInt, endInt)):
		total = total - 1
		
	if (IP2Int(networkAddr) in range(startInt, endInt)):
		total = total - 1
		
	return total


def IP2Int(ip):
	return IP(ip).int()


def IP2String(ip):
	return IP(ip).strNormal()


def IP2Bin(ip):
	return IP(ip).strBin()


def NetmaskLen(netmask):
	return len(IP2Bin(netmask).replace("0", ""))


def ParseNetwork(ip, netmask):
	return IP("%s/%s" % (ip, netmask), make_net=True).strNormal()


# ip ranges must be in the same network
# True or False
def IPRangeOverLap(start, end, dstStart, dstEnd):
	if IP(end) < IP(dstStart) or IP(dstEnd) < IP(start):
		return False
	else:
		return True


def IPRangeValid(start, end, gateway):
	return not IPRangeOverLap(gateway, gateway, start, end)
	

if __name__ == "__main__":
	ip1 = "192.168.10.1"
	mask1 = "255.255.255.0"
	
	print(NetmaskLen(mask1))
	
	start = "192.168.1.1"
	end = "192.168.1.10"
	
	dstStart = "192.168.1.0"
	dstEnd = "192.168.1.20"
	
	gateway = "192.168.1.1"
	
	print(IPRangeOverLap(start, end, dstStart, dstEnd))
	
	print(IPRangeValid(dstStart, dstEnd, gateway))
	
	print(ParseNetwork("3.3.3.3", "255.255.255.0"))

	net = make_net(ip=IP2Int(start), netmask=mask1)
	broadcastAddr = BroadcastAddr(net=net)
	networkAddr = NetworkAddr(net=net)
	print(broadcastAddr)
	print(networkAddr)