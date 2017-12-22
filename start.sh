#!/bin/sh

PROCESS_NUM=`ps aux | grep "TUNDRA" | grep -v grep | awk '{print $2}'`
if [ "$PROCESS_NUM" != "" ]; then
	kill -9 ${PROCESS_NUM}
fi

./PWATCH start "/usr/bin/python3 ./TUNDRA.py 0.0.0.0 9090"
