#!/bin/bash

VERSION="0.0.1"
TODAY=$(date +"%m%d%Y")

get_package_name()
{
	echo "QUANTUM-$1-BUILD-$VERSION-$TODAY"
}

create_package()
{
	PACKAGE=$1
	if [ "$PACKAGE" = "allinone" ]; then
		echo "Building allinone package..."

		package_name=$(get_package_name $PACKAGE)
		tar -zcf package/$package_name.tgz  *.py *.sh *.conf PWATCH LICENSE bin conf db core crt models modules static templates utils views --exclude=BUILD.sh

		echo ""
		echo -e "\e[32m Well Done \e[0m"
		echo -e "\e[32m Build $PACKAGE package package/$package_name.tgz OK \e[0m"
		echo ""

	elif [ "$PACKAGE" = "server" ]; then
		echo "Building server package..."

		package_name=$(get_package_name $PACKAGE)
		tar -zcf package/$package_name.tgz   __init__.py QUANTUM.py *.sh nginx.conf PWATCH LICENSE bin conf db core crt models modules static templates utils views --exclude=BUILD.sh

		echo ""
		echo -e "\e[32m Well Done \e[0m"
		echo -e "\e[32m Build $PACKAGE package package/$package_name.tgz OK \e[0m"
		echo ""

	elif [ "$PACKAGE" = "agent" ]; then
		echo "Building agent package..."

		package_name=$(get_package_name $PACKAGE)
		tar -zcf package/$package_name.tgz   __init__.py AGENT.py *.sh agent.conf PWATCH LICENSE bin conf core models modules views utils --exclude=BUILD.sh

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
