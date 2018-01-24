#!/bin/sh


./env_check.sh
if [ "$?" != 0 ]; then
	echo "check env failed"
	exit 1
fi

# for server
if [ -f nginx.conf -a -f crt/server.key -a -f crt/server.crt ]; then
	cp nginx.conf /etc/nginx/conf.d/quantum.conf
	cp crt/server.key /etc/nginx/.
	cp crt/server.crt /etc/nginx/.

	if [ -x /etc/init.d/nginx ]; then
		/etc/init.d/nginx restart
	fi
fi


# for agent
if [ -f agent.conf ]; then
	mkdir -p /var/quantum
	cp agent.conf /var/quantum/quantum.conf
fi
