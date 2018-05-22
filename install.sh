#!/bin/sh
cd /home/pi/cumulocity-python-client
/usr/bin/git pull
sudo /usr/bin/python setup.py install
/sbin/reboot
