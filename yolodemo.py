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

memory = None
YoloModule = None

class ImageGetter():
	def __init__(self):
		self.video_service = ALProxy("ALVideoDevice")
		resolution = 5#3  # VGA
		colorSpace = 11  # RGB
		self.video_service.setActiveCamera(0)

		for idx in self.video_service.getSubscribers():
			if idx.startswith('python_client_yolo'):
				self.video_service.unsubscribe(idx)



		self.videoClient = self.video_service.subscribe("python_client_yolo", resolution, colorSpace, 10)
		print ('videoclientID: ',self.videoClient)

	def __del__(self):
		print('unsubscribing ',self.videoClient)
		self.video_service.unsubscribe(self.videoClient)

	def getImage(self):


		t0 = time.time()

		# Get a camera image.
		# image[6] contains the image data passed as an array of ASCII chars.
		naoImage = self.video_service.getImageRemote(self.videoClient)

		t1 = time.time()

		# Time the image transfer.
		print "acquisition delay ", t1 - t0
		self.video_service.releaseImage(self.videoClient)


		return naoImage


def PepperSay(message, tts):
	global memory

	try:

		if memory is not None:
			memory.unsubscribeToEvent("Dialog/LastInput","YoloModule")

		if tts is not None:
			tts.say(message)

		if memory is not None:
			memory.subscribeToEvent("Dialog/LastInput","YoloModule", "onInput")
	except:
		pass


# create python module
class myModule(ALModule):
	"""python class myModule test auto documentation: comment needed to create a new python module"""

	def __init__(self, name):
		ALModule.__init__(self, name)
		self.tts = ALProxy("ALTextToSpeech")

		self.mycamera= ImageGetter()
		self.show_flag = False

	def close(self):
		self.mycamera.close()

	def onInput(self, key, value, message):

		awp = ALProxy("ALBasicAwareness")
		awp.pauseAwareness()

		global memory
		print memory.getData("Dialog/LastInput")
		if memory.getData("Dialog/LastInput")=='':
			return
		#print memory.getDataListName()

		print ("yeah:",key, value, message)

		#self.tts.say("yeah!")
		#PepperSay("mmm...",self.tts)
		image = self.mycamera.getImage()
		awp.resumeAwareness()
		#print ("image:", image)

		if image is None:

			return

		print "width of the image:		", image[0]
		print "height of the image:		", image[1]
		print "image.getNbLayers:		", image[2]
		print 'colorspace of the image:	', image[3]
		print 'time stamp (second):		', image[4]
		print 'time stamp (microsecond):', image[5]
		print 'data of the image (ignore to print). - image[6]', len(image[6])
		print 'camera ID:				', image[7]
		print 'camera FOV left angle:	', image[8]
		print 'camera FOV top angle:	', image[9]
		print 'camera FOV right angle:	', image[10]
		print 'camera FOV bottom angle:	', image[11]

		# use Python Image Library (PIL)
		# Create a PIL Image from our pixel array.
		image_colorspace = 'RGB'
		image_width, image_height = image[0], image[1]
		image_data=image[6]
		risimage = Image.frombytes(image_colorspace, (image_width, image_height), image_data)

		self.saveImage(risimage, 'PNG', 'camImage.png')
		risposta = self.analyseImage(risimage,'camImage.png')
		print (risposta)


		PepperSay(risposta,self.tts)




	def saveImage(self, image, image_format='PNG', image_filename='camImage.png'):
		# use Python Image Library (PIL)
		# Create a PIL Image from our pixel array.
		# Save the image.
		print '<VideoImage> - save image to', image_filename
		image.save(image_filename, image_format)
		if self.show_flag == True:
			image.show()


	def analyseImage(self,image,filename):
		#TODO
		#filename = 'D:\\foto\\IMG_9324.jpg'
		r = requests.post("http://"+configuration.YOLO_IP+":" + str(configuration.YOLO_PORT)+"/detect",
						  files = {'image': open(filename,'rb')},
						  data={'model': 'yolo4'})
		print(r.status_code, r.reason)
		ris = r.content
		print (ris)
		obj = json.loads(ris)

		listbb = obj.get('bounding-boxes',[])
		classes=[]
		for bb in listbb:
			classes.append(bb.get('ObjectClassName',''))
		risstr = "ecco quello che vedo: " + ', '.join(classes)
		return risstr.encode('ascii', 'replace')

def createDialog(dlg, tts):
	if configuration.Language == 'ENG':
		dlg.setLanguage("English")

		print "English loaded topics:", dlg.getLoadedTopics("English")

		for topic in dlg.getLoadedTopics("English"):
			if topic=='topic_yolo':
				dlg.unloadTopic(topic)


		f = open("topic_eng.top", "r")
		topicContent = f.read()
		f.close()

		topicName = dlg.loadTopicContent (topicContent)
		print topicName
		dlg.activateTopic(topicName)


	if configuration.Language == 'ITA':
		dlg.setLanguage("Italian")

		print "Italian loaded topics:", dlg.getLoadedTopics("Italian")

		for topic in dlg.getLoadedTopics("Italian"):
			if topic=='topic_yolo':
				dlg.unloadTopic(topic)


		f = open("topic_yolo.top", "r")
		topicContent = f.read()
		f.close()


		topicName = dlg.loadTopicContent (topicContent)
		print topicName
		dlg.activateTopic(topicName)


	# tts.say("Ciao! Dimmi e ti dirò cosa vedo!")
	PepperSay("Ciao!",tts)

	global memory
	memory = ALProxy("ALMemory")

	global YoloModule
	YoloModule = myModule("YoloModule")


	memory.subscribeToEvent("Dialog/LastInput","YoloModule", "onInput")


def main(pip, pport):

	myBroker = ALBroker("myBroker",
						"0.0.0.0",  # listen to anyone
						0,  # find a free port and use it
						pip,  # parent broker IP
						pport)  # parent broker port

	# setto linguaggio per sicurezza
	tts = ALProxy("ALTextToSpeech")
	dlg = ALProxy("ALDialog")


	print(tts)
	dlg.setASRConfidenceThreshold(0.35)
	print (dlg.getASRConfidenceThreshold())

	createDialog(dlg,tts)

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print "Interrupted by user, shutting down"
		PepperSay("ciao, a presto!",tts)
		global YoloModule
		YoloModule.close()
		myBroker.shutdown()
		sys.exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", type=str, default=configuration.PEPPER_IP,
	                    help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
	parser.add_argument("--port", type=int, default=configuration.PEPPER_PORT,
	                    help="Naoqi port number")

	args = parser.parse_args()

	main(args.ip, args.port)


