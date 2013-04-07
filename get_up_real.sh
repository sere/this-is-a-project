#!/bin/bash

IP=${1-"192.168.0.0"}
MASK=${2-"24"}

sudo nmap -T0 -sP $IP/$MASK | grep -B 1 "Host is up" | grep "Nmap scan report for" | awk '{print $5}'
