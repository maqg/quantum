#!/bin/bash

echo ""
echo "STEP 1, Create server key, then remove password"
echo ""
openssl genrsa -des3 -out server.key 1024
if [ "$?" != "0" ]; then
	echo -e "create server private key [\e[1;31m FAILED \e[0m]"
	exit 1
fi
openssl rsa -in server.key -out server.key

echo ""
echo "STEP 2, Create server Certificate Signing Request (CSR)"
echo ""
if [ ! -f ./openssl.cnf ]; then
	cp /etc/ssl/openssl.cnf .
fi
openssl req -new -key server.key -out server.csr -config openssl.cnf
if [ "$?" != "0" ]; then
	echo -e "create server CSR [\e[1;31m FAILED \e[0m]"
	exit 1
fi

echo ""
echo "STEP 3, Create CA"
echo ""
openssl req -new -x509 -keyout ca.key -out ca.crt -days 3650 -config openssl.cnf
if [ "$?" != "0" ]; then
	echo -e "create CA [\e[1;31m FAILED \e[0m]"
	exit 1
fi

echo ""
echo "STEP 4, Sign server cert"
echo ""
if [ ! -d ./demoCA ]; then
	mkdir -p demoCA/newcerts
	touch demoCA/index.txt
	echo "01" > demoCA/serial
fi
openssl ca -in server.csr -out server.crt -cert ca.crt -keyfile ca.key -days 3650 -config openssl.cnf
if [ "$?" != "0" ]; then
	echo -e "Sign server cert with self-CA [\e[1;31m FAILED \e[0m]"
	exit 1
fi

echo ""
echo -e "\e[1;32mServer Certs Created! \e[0m"
echo ""
