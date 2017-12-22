
all::
	./build_dbcache.pl dbquantum > mysql.xml
	python3 ../bin/initial.py

init::
	./build_dbcache.pl dbquantum > mysql.xml
#python3 initData.py > mysql.default.auto
	python3 ../bin/initial.py
	./init_db.sh
	./dump.sh

initdb::
#python3 initData.py > mysql.default.auto
	./init_db.sh
