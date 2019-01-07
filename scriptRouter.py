#!/usr/bin/env python2

"""picofix.py: reboot the a router when it fails to contact a distant node."""

__author__ = "Alex 'Chozabu' P-B"


import pyping
from time import sleep
from datetime import datetime
import telnetlib

def reboot_router():
    tn=telnetlib.Telnet("192.168.1.1")         
    tn.read_until("username:")
    tn.write("1234\n")
    tn.read_until("password:")
    tn.write("1234\n")
    sleep(2)
    tn.write("reboot\n")
    print tn.read_all()

def main_loop():
	reboots = [None]
	fail_count = 0
	ok_count = 0
	while True:
		if pyping.ping('192.168.10.1').ret_code:
			ok_count = 0
			fail_count += 1
			print("FAIL", fail_count)
			if fail_count > 0:
				reboots.append(datetime.now().strftime("%Y-%m-%m %H:%M"))
				print("rebooting router!")
				reboot_router()
				print("rebooted router, waiting 60 seconds")
				print('reboots:', reboots)
				sleep(120)
				print("OK, back to normal")
				fail_count = 0
		else:
			fail_count = 0
			ok_count += 1
			print("seems OK, ok_count:", ok_count, 'last_reboot:', reboots[-1], 'of', len(reboots)-1)
		sleep(2)

if __name__ == "__main__":
	main_loop()
