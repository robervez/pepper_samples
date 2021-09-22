#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Modify Face Tracking policy on the robot."""

import configuration
import qi
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from PIL import Image
import requests
import json

import argparse
import sys
import time


def main(pip, pport):

	myBroker = ALBroker("myBroker",
	                    "0.0.0.0",  # listen to anyone
	                    0,  # find a free port and use it
	                    pip,  # parent broker IP
	                    pport)  # parent broker port


	syspr = ALProxy("ALSystem")
	syspr.reboot()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default=configuration.PEPPER_IP,
	                    help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
	parser.add_argument("--port", type=int, default=configuration.PEPPER_PORT,
	                    help="Naoqi port number")

	args = parser.parse_args()

	main(args.ip, args.port)


