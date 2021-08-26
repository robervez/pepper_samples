from naoqi import ALProxy
#tts = ALProxy("ALTextToSpeech", "localhost", 10531)
tts = ALProxy("ALTextToSpeech", "192.168.137.251", 9559)

tts.say("Ciao Tommy! Come stai?")

