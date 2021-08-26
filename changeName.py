from naoqi import ALProxy
import time

try:
	#tts = ALProxy("ALTextToSpeech", "localhost", 10531)
	alsys = ALProxy("ALSystem", "192.168.137.251", 9559)
	tts = ALProxy("ALTextToSpeech", "192.168.137.251", 9559)

	tab = ALProxy("ALTabletService", "192.168.137.251", 9559)

	alsys.setRobotName("Peppo")

	print(tab.getWifiStatus())
	print(tab.configureWifi("wpa","VANGOGH","vangogh123"))
	tab.connectWifi("VANGOGH")
	time.sleep(3)
	print(tab.getWifiStatus())

	tts.say(alsys.robotName())

	#tab.showInputDialog("text","ciao","ok","cancel" )
	ris = tab.showImageNoCache("https://aimagelab.ing.unimore.it/imagelab/uploadedImages/000233_thumb.jpg")
	print(ris)
	time.sleep(3)
except Exception, e:
	print "Error was: ", e
