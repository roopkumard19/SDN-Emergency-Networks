from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
import pubnub#pubnub==4.0.2
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import json

# Connect to the PubNub server
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-e2aa1c80-b6f9-11e7-b8f2-c6027b8a2e05"
pnconfig.publish_key = "pub-c-b3b3434d-7fbb-4ce6-bcc2-6762382de1d4"
pubnub = PubNub(pnconfig)

# Connect to the local MySQL db
cnx = mysql.connector.connect(user='root', password='toor@1234',database='Mesh')
cursor = cnx.cursor()

# Query the DB for Name, Latitude & Longitude values
query = "SELECT Name,LAT,LNG FROM Nodes"
cursor.execute(query)

#Parse & JSONify the values from the query result
for (Name,LAT,LNG) in cursor:
	#print("{}, {}, {}".format(Name, LAT, LNG))
	result = []
	result.append(Name)
	result.append(LAT)
	result.append(LNG)
	final = json.dumps(result) 
	pubnub.publish().channel("logging").message(final)
	print(final)
cursor.close()
cnx.close()


