#!/bin/sh

echo "hello" >> /tmp/1111.log

cd /home/maintainer/monitor/
/usr/bin/python monitor_restart.py

