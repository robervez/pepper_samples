#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Modify Face Tracking policy on the robot."""

import qi
import argparse
import sys
import configuration

def createDialog(dlg, tts):
	dlg.setLanguage("Italian")
	f = open("topic_yolo.top", "r")
	topicContent = f.read()
	f.close()


	topicName = dlg.loadTopicContent (topicContent)
	print topicName
	dlg.activateTopic(topicName)


	tts.say("Ciao! Dimmi 'Pepper' e ti dirò cosa vedo!")

def main(session):
	# setto linguaggio per sicurezza
	tts = session.service("ALTextToSpeech")
	dlg = session.service("ALDialog")

	print(tts)

	createDialog(dlg,tts)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default=configuration.PEPPER_IP,
	                    help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
	parser.add_argument("--port", type=int, default=configuration.PEPPER_PORT,
	                    help="Naoqi port number")

	args = parser.parse_args()
	session = qi.Session()
	try:
		session.connect("tcp://" + args.ip + ":" + str(args.port))
	except RuntimeError:
		print ("Can't connect at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
		                                                                            "Please check your script arguments. Run with -h option for help.")
		sys.exit(1)
	main(session)
