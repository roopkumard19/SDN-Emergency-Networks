import time
import pubnub#pubnub==4.0.2
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-e2aa1c80-b6f9-11e7-b8f2-c6027b8a2e05"
pnconfig.publish_key = "pub-c-b3b3434d-7fbb-4ce6-bcc2-6762382de1d4"

pubnub = PubNub(pnconfig)

def show(msg, stat):
	if msg and stat: 
		print( msg.timetoken, stat.status_code )
		print(msg)
	else: print( "Error", stat and stat.status_code )

#time.sleep(2)
def failed_nodes_dummy_call():
	with open("failedIPs.txt", 'r') as infile:
		final = []
		for line in infile:
			final.append(line.rstrip())
			print line

		pubnub.publish().channel("failed_nodes").message(final).async(show)

def mesh_nodes_dummy_call():
	with open("sample_gps.txt", 'r') as infile:
                final = {}
		i = 0
                for line in infile:
			tmp_dict = {}
			tmp_list = line.rstrip().split(',')
                        tmp_dict['name'] = "M"+str(i)
			tmp_dict['lat'] = float(tmp_list[0])
			tmp_dict['lng'] = float(tmp_list[1])
			final[i] = tmp_dict
			i = i + 1
		print final
                pubnub.publish().channel("mesh_nodes").message(final).async(show)


def main():
	mesh_nodes_dummy_call()
#	failed_nodes_dummy_call()

if __name__ == '__main__':
	main()


