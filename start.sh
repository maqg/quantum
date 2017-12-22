#!/bin/sh

PROCESS_NUM=`ps aux | grep "QUANTUM" | grep -v grep | awk '{print $2}'`
if [ "$PROCESS_NUM" != "" ]; then
	kill -9 ${PROCESS_NUM}
fi

./PWATCH start "/usr/bin/python3 ./QUANTUM.py 0.0.0.0 9300"
