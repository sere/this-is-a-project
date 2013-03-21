#!/bin/bash

IF=${1-"eth0"}

line="$(ifconfig | sed -n "/$IF/,/\n/p" | grep "inet")"
inet="$(echo $line | awk '{print $2}')"
netmask="$(echo $line | awk '{print $4}')"

if [[ $inet == "" ]]; then
	exit 0
fi

#inet_cut=${inet%.*}.0

count=0
for i in ${netmask//./ }; do
	partialcount=$((`echo "obase=2;$i" | bc | sed 's/[^1]//g'|wc -m`-1))
	count=`expr $count + $partialcount`
done

echo $inet $count

