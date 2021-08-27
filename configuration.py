
import os
import sys
import platform

useLocalhost = True

PEPPER_IP = "192.168.1.5"
TABLETPEPPER_IP = "192.168.1.10"
PEPPER_PORT = 9559


print ("platform:",platform.node())
if platform.node()=='vangogh':
	if useLocalhost:
		PEPPER_IP = "127.0.0.1"
		TABLETPEPPER_IP = "127.0.0.1"

		PEPPER_PORT = 10759

	YOLO_IP = "127.0.0.1"
	YOLO_PORT = 1234


if platform.node()=='LIGABUE2020':
	if useLocalhost:
		PEPPER_IP = "127.0.0.1"
		TABLETPEPPER_IP = "127.0.0.1"
		PEPPER_PORT = 53348

	YOLO_IP = "127.0.0.1"
	YOLO_PORT = 1234