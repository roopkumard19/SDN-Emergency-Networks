from db_fetch import *
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_twisted import PubNubTwisted as PubNub
#from pubnub.pubnub import PubNub
from pubnub.enums import PNStatusCategory
from pubnub.callbacks import SubscribeCallback
import sys
import time
from twisted.internet import reactor

# Connect to the PubNub server
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-e2aa1c80-b6f9-11e7-b8f2-c6027b8a2e05"
pnconfig.publish_key = "pub-c-b3b3434d-7fbb-4ce6-bcc2-6762382de1d4"
pubnub = PubNub(pnconfig)


def send_drone(location):
	print "sending to {}".format(location)

def position_calculation(geo_loc):
	if len(geo_loc) == 1:
		send_drone(geo_loc[0])
	elif

class MySubscribeCallback(SubscribeCallback):
	def presence(self, pubnub, presence):
	        pass  # handle incoming presence data
 
	def status(self, pubnub, status):
		pass

	def message(self, pubnub, message):
		ip_list = message.message
		geo_loc  = []
		for ip in ip_list:
			geo_loc.append(get_location_from_ip(ip))
		position_calculation(geo_loc)
		

def main():
	pubnub.add_listener(MySubscribeCallback())
	pubnub.subscribe().channels("failed_nodes").execute() 
	reactor.callLater(10, pubnub.stop)  # stop reactor loop after 30 seconds
    	pubnub.start()

if __name__ == "__main__":
	main()
