#!/bin/sh

PROCESS_NUM=`ps aux | grep "QUANTUM" | grep -v grep | grep -v PWATCH | awk '{print $2}'`
if [ "$PROCESS_NUM" != "" ]; then
	kill -9 ${PROCESS_NUM}
fi
