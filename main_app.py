from handle_db import *
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_twisted import PubNubTwisted as PubNub
#from pubnub.pubnub import PubNub
from pubnub.enums import PNStatusCategory
from pubnub.callbacks import SubscribeCallback
import sys
import time
from twisted.internet import reactor
from centroid import *
from math import radians, cos, sin, asin, sqrt

# Connect to the PubNub server
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-e2aa1c80-b6f9-11e7-b8f2-c6027b8a2e05"
pnconfig.publish_key = "pub-c-b3b3434d-7fbb-4ce6-bcc2-6762382de1d4"
pubnub = PubNub(pnconfig)


def send_drone(location):
	print "sending to {}".format(location)

def position_calculation(c_list, a_list):
	for c in c_list:
		mini = 1 # 1 km
		for a in a_list:
			temp = havesine(c[0], c[1], a[0], a[1])
			if mini > temp:
				mini = temp
				nearest_active = list(a[0], a[1])
		send_drone([c, nearest_active])

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

class MySubscribeCallback(SubscribeCallback):
	def presence(self, pubnub, presence):
	        pass  # handle incoming presence data
 
	def status(self, pubnub, status):
		pass

	def message(self, pubnub, message):
		ip_list = message.message
		geo_loc  = []
		update_db(ip_list)
		for ip in ip_list:
			geo_loc.append(get_location_from_ip(ip))
			#print ip
		centroids = form_cluster(geo_loc)	
		active_nodes = get_active_nodes()
		position_calculation(centroids, active_nodes)

def main():
	#pubnub.add_listener(MySubscribeCallback())
	#pubnub.subscribe().channels("failed_nodes").execute() 
	#reactor.callLater(10, pubnub.stop)  # stop reactor loop after 30 seconds
    	#pubnub.start()
	print haversine(37.411823, -121.995850, 37.411823, -121.995850)
	geo_loc = [[37.411823, -121.995850],
		[37.412331, -121.995888],
		[37.41182, -121.9959],
		[37.41182, -121.99589],
		[37.411821667, -121.9959],
		[37.41182, -121.9959],
		[37.41182, -121.99589],
		[37.411818333, -121.99589],
		[37.411818333, -121.99589],
		[37.41182, -121.99589],
		[38.41182, -121.99589],
		[37.411818333, -121.99589],
		[37.41182, -121.99589],
		[37.41185, -121.9959],
		[37.41192, -121.99589899],
		[40.411931667, -121.9959],
		[37.411953333, -121.99589],
		[37.41205, -121.9959],
		[37.412084, -121.9959],
		[37.41216, -121.9959]]

#	print len(geo_loc)
#	position_calculation(geo_loc)
	'''###Make this script as a server
	####Receive the failed nodes (F1)
	####Update the database with the failed nodes
	#####call the position_calculation function with input as failed nodes (F1)
	####Get the active nodes (A1) from database.
	For each centroid, find out the nearest node from A1.
	Call the send_drone function with the pair(centroid,nearest active node)
	This function will return the precide positions to the drone. '''

if __name__ == "__main__":
	main()
