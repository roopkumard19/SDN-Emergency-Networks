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
from math import radians, degrees, cos, sin, asin, sqrt, atan2
from pygeodesy.sphericalNvector import LatLon
from pygeodesy import R_NM, F_D, F_DM, F_DMS, F_RAD, \
                      degrees, isclockwise, isconvex, isenclosedby, \
                      m2NM

import re


# Connect to the PubNub server
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-e2aa1c80-b6f9-11e7-b8f2-c6027b8a2e05"
pnconfig.publish_key = "pub-c-b3b3434d-7fbb-4ce6-bcc2-6762382de1d4"
pubnub = PubNub(pnconfig)

distance_threshold = 0.00762 # 25 feet in km
distance_XY_threshold = 275

def uav_placement(centroid_active_pair):
	print "In send drone centroid_active_pair: {}".format(centroid_active_pair)
	final = {}
	lat1 = centroid_active_pair[0][0]
	lon1 = centroid_active_pair[0][1]
	lat2 = centroid_active_pair[1][0]
	lon2 = centroid_active_pair[1][1]
	dist = haversine(lat1, lon1, lat2, lon2)
	print "init: dist:{}".format(dist)
	
	if dist <= distance_threshold:
		print "Sending drone to:{}".format([lat2, lon2])

        q = LatLon(lat2, lon2)
	while dist > distance_threshold:
		p = LatLon(lat1, lon1)
        	i = p.intermediateTo(q, (distance_threshold/dist))
		print "dms:{}".format(i)
	        lat1,lon1 = map(degrees, list(i.to2ab()))
		dist = haversine(lat1, lon1, lat2, lon2)
		print "cur_dist:{}".format(dist)
		print "Sending drone to:{}".format([lat1, lon1])
		

def uav_XY_placement(centroid_active_pair):
        print "In send drone centroid_active_pair: {}".format(centroid_active_pair)
        final = {}
        x1 = centroid_active_pair[0][0]
        y1 = centroid_active_pair[0][1]
        x2 = centroid_active_pair[1][0]
        y2 = centroid_active_pair[1][1]
        dist = sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
	print "init: dist:{} {} {} {} {}".format(dist, x1, y1, x2, y2)

        if dist <= distance_XY_threshold:
                print "Sending drone to:{}".format([x2, x2])
        
	while dist > distance_XY_threshold:
                frac = distance_XY_threshold/dist
		ix = (1-frac)*x1 + frac*x2
		iy = (1-frac)*y1 + frac*y2
                dist = sqrt( (x2 - ix)**2 + (y2 - iy)**2 )
		print "cur_dist:{}".format(dist)
                print "Sending drone to:{}".format([ix, iy])


def find_nearest_active(c_list, a_list):
	final = []
	for c in c_list:
		mini = 1 # 1 km
		for a in a_list:
			temp = haversine(c[0], c[1], a[0], a[1])
			if mini > temp:
				mini = temp
				nearest_active = [a[0], a[1]]
		final.append([nearest_active, c])
	return final		

def find_XY_nearest_active(c_list, a_list):
        final = []
        for c in c_list:
                mini = 1000 # 1000 units
                for a in a_list:
                        temp = sqrt( (a[0] - c[0])**2 + (a[1] - c[1])**2 )
			if mini > temp:
                                mini = temp
                                nearest_active = [a[0], a[1]]
                final.append([nearest_active, c])
        return final



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
		failed_ip_list = message.message
		failed_node_geo_loc  = []
		update_db(failed_ip_list)
		for ip in failed_ip_list:
			failed_node_geo_loc.append(get_XY_from_ip(ip))
			#print ip
		#centroids = form_cluster(failed_node_geo_loc, 'euclidean', 48.547/6371.0088)
		centroids = form_cluster(failed_node_geo_loc, 'euclidean', 275/2)
		print "centroids: {}".format(centroids)	
		active_nodes = get_XY_active_nodes()
		centroid_active_pairs = find_XY_nearest_active(centroids, active_nodes)
		for pair in centroid_active_pairs:
			uav_XY_placement(pair)

def main():
	pubnub.add_listener(MySubscribeCallback())
	pubnub.subscribe().channels("failed_nodes").execute() 
	reactor.callLater(10, pubnub.stop)  # stop reactor loop after 30 seconds
    	pubnub.start()

#	print len(geo_loc)
#	position_calculation(geo_loc)
	'''###Make this script as a server
	####Receive the failed nodes (F1)
	####Update the database with the failed nodes
	#####call the position_calculation function with input as failed nodes (F1)
	####Get the active nodes (A1) from database.
	###3For each centroid, find out the nearest node from A1.
	####Call the send_drone function with the pair(centroid,nearest active node)
	###This function will return the precise positions to the drone. '''

if __name__ == "__main__":
	main()
