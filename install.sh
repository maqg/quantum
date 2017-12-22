#!/bin/sh

cp nginx.conf /etc/nginx/conf.d/tundra.conf
cp crt/server.key /etc/nginx/.
cp crt/server.crt /etc/nginx/.

if [ -x /etc/init.d/nginx ]; then
	/etc/init.d/nginx restart
fi
