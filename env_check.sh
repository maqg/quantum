#!/bin/bash

if [ ! -x /usr/bin/python3 ]; then
	echo -e "\e[1;31mpython3 not installed\e[0m"
	exit 1
fi

if [ ! -x /usr/bin/dstat ]; then
	echo -e "\e[1;31mdstat not installed, with \"apt-get install dstat\" to install\e[0m"
	exit 1
fi

if [ ! -x /usr/bin/ifstat ]; then
	echo -e "\e[1;31mifstat not installed, with \"apt-get install ifstat\" to install\e[0m"
	exit 1
fi

if [ ! -x /usr/bin/iostat ]; then
	echo -e "\e[1;31miostat not installed, with \"apt-get install sysstat\" to install\e[0m"
	exit 1
fi

echo -e "\e[1;32mENV CHECKED OK\e[0m"
