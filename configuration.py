
import os
import sys

useLocalhost = True

PEPPER_IP = "192.168.1.5"
TABLETPEPPER_IP = "192.168.1.10"
PEPPER_PORT = 9559

if useLocalhost:
	PEPPER_IP = "127.0.0.1"
	TABLETPEPPER_IP = "127.0.0.1"
	PEPPER_PORT = 53348


