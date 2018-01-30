#!/bin/bash

VERSION="0.0.1"
TODAY=$(date +"%m%d%Y")
CUR_PATH=`pwd`
PACKAGE_DIR=$CUR_PATH/package

get_package_name()
{
	echo "QUANTUM-$1-BUILD-$VERSION-$TODAY"
}

create_package()
{
	PACKAGE=$1
	if [ "$PACKAGE" = "allinone" ]; then
		echo "Building allinone package..."
		cd $CUR_PATH

		mkdir -p $PACKAGE_DIR/quantum
		cp -rf *.py *.sh *.conf PWATCH LICENSE bin conf db core crt models modules static templates utils views  $PACKAGE_DIR/quantum
		rm -f $PACKAGE_DIR/quantum/BUILD.sh
	
		cd $PACKAGE_DIR
		package_name=$(get_package_name $PACKAGE)
		tar -zcf $package_name.tgz quantum
		rm -rf quantum

		echo ""
		echo -e "\e[32m Well Done \e[0m"
		echo -e "\e[32m Build $PACKAGE package package/$package_name.tgz OK \e[0m"
		echo ""

	elif [ "$PACKAGE" = "server" ]; then
		echo "Building server package..."
		cd $CUR_PATH

		mkdir -p $PACKAGE_DIR/quantum
		cp -rf  __init__.py QUANTUM.py *.sh nginx.conf PWATCH LICENSE bin conf db core crt models modules static templates utils views  $PACKAGE_DIR/quantum
		rm -f $PACKAGE_DIR/quantum/BUILD.sh

		cd $PACKAGE_DIR
		package_name=$(get_package_name $PACKAGE)
		tar -zcf $package_name.tgz quantum 
		rm -rf quantum

		echo ""
		echo -e "\e[32m Well Done \e[0m"
		echo -e "\e[32m Build $PACKAGE package package/$package_name.tgz OK \e[0m"
		echo ""

	elif [ "$PACKAGE" = "agent" ]; then
		echo "Building agent package..."
		cd $CUR_PATH

		mkdir -p $PACKAGE_DIR/quantum
		cp -rf __init__.py AGENT.py *.sh agent.conf PWATCH LICENSE bin conf core models modules views utils  $PACKAGE_DIR/quantum
		rm -f $PACKAGE_DIR/quantum/BUILD.sh

		cd $PACKAGE_DIR
		package_name=$(get_package_name $PACKAGE)
		tar -zcf $package_name.tgz quantum
		rm -rf quantum

		echo ""
		echo -e "\e[32m Well Done \e[0m"
		echo -e "\e[32m Build $PACKAGE package package/$package_name.tgz OK \e[0m"
		echo ""

	else

		echo "unsupport build type [$PACKAGE]"
		exit 1
	fi
}

echo "Start build package..."

BUILDTYPE=$1
rm -rf package
mkdir -p package

if [ $BUILDTYPE = "build" ]; then 
	PACKAGES="server agent allinone"
else
	PACKAGES="$BUILDTYPE"
fi

for PACKAGE in $PACKAGES; do

	create_package $PACKAGE
done

exit 0
