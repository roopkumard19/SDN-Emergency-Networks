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

def show(msg, stat):
    if msg and stat: print( msg.timetoken, stat.status_code )
    else           : print( "Error", stat and stat.status_code )




def execute_query(query):
	try:
		# Connect to the local MySQL db
		cnx = mysql.connector.connect(user='root', password='toor@1234',database='Mesh')
		cursor = cnx.cursor()
		result = ""
		cursor.execute(query)
		if "update" not in query:
			result = cursor.fetchall()
                
	except mysql.connector.Error as err:
		print("Failed executing query: {}".format(err))
		exit(1)

	cnx.commit()
	cursor.close()
	cnx.close()
	return result

def send_to_map():
	# Query the DB for Name, Latitude & Longitude values
	query = "SELECT ID,Name,LAT,LNG FROM Nodes"
	cursor = execute_query(query)
	final = {}

	#Parse & JSONify the values from the query result
	for (ID,Name,LAT,LNG) in cursor:
		#print("{}, {}, {}".format(Name, LAT, LNG))
		result = {}
		result['name'] = Name
		result['lat'] = LAT
		result['lng'] = LNG
		final[ID] = result 

	print(final)

	pubnub.publish().channel("mesh_nodes").message(final).async(show)


def get_location_from_ip(ip):
	query = "SELECT LAT,LNG FROM Nodes WHERE IP=\""+ip+"\" AND Name NOT LIKE \"gw%\""
	cursor = execute_query(query)
	return list(cursor[0])

def get_XY_from_ip(ip):
	query = "SELECT X,Y FROM Nodes WHERE IP=\""+ip+"\" AND Name NOT LIKE \"gw%\""
        cursor = execute_query(query)
        return list(cursor[0])

def update_db(ip_list):
	for ip in ip_list:
		query = "update Nodes set Status = \"Inactive\" where IP = \""+ip+"\""	
		print(query)
		execute_query(query)

def get_active_nodes():
	query = "SELECT LAT,LNG FROM Nodes WHERE Status=\"active\""
	cursor = execute_query(query)
	return [list(elem) for elem in cursor]

def get_XY_active_nodes():
        query = "SELECT X,Y FROM Nodes WHERE Status=\"active\""
        cursor = execute_query(query)
        return [list(elem) for elem in cursor]

