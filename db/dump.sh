#!/bin/sh

. ./global.sh

mysqldump -u$DB_USER -p$DB_PASSWD $DB_NAME -n -q -R > dumped4windows.sql
