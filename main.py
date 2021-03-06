import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

import configuration
from optparse import OptionParser


# set di funzioni per testare pepper

def ciao():

    tts = ALProxy("ALTextToSpeech", configuration.PEPPER_IP,configuration.PEPPER_PORT)
    tts.say("Ciao Tommy! Come stai?")


def main():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
                      help="Parent broker port. The IP address or your robot",
                      dest="pip")
    parser.add_option("--pport",
                      help="Parent broker port. The port NAOqi is listening to",
                      dest="pport",
                      type="int")
    parser.set_defaults(
        pip=configuration.PEPPER_IP,
        pport=configuration.PEPPER_PORT)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    ciao()

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
                        "0.0.0.0",   # listen to anyone
                        0,           # find a free port and use it
                        pip,         # parent broker IP
                        pport)       # parent broker port




    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)



if __name__ == "__main__":
    main()