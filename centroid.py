import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
from sklearn.cluster import DBSCAN
from sklearn import metrics
from geopy.distance import great_circle
from shapely.geometry import MultiPoint


'''georads = []
coords = []
with open("log.log", 'r') as infile:
	for line in infile:
		line = list(map(float, line.strip()[1:-1].split(',')))
		#converts = []
		coords.append(line)
		#converts.append(np.radians(line[0]))
		#converts.append(np.radians(line[1]))
		#georads.append(converts)

#print len(georads)'''

def get_centermost_point(cluster):
	centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
	centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
	#print centermost_point
	return tuple(centermost_point)


def form_cluster(coords):
	coords = np.array(coords)
	kms_per_radian = 6371.0088

	# Assuming that mesh nodes are 25 feet apart from each other and converting it to kilometers.
	epsilon = 48.547 / kms_per_radian

	start_time = time.time()
	db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
	cluster_labels = db.labels_

	# get the number of clusters
	num_clusters = len(set(cluster_labels))

	message = 'Clustered {:,} points down to {:,} clusters, for {:.1f}% compression in {:,.2f} seconds'
	#print(message.format(len(df), num_clusters, 100*(1 - float(num_clusters) / len(df)), time.time()-start_time))

	# turn the clusters in to a pandas series, where each element is a cluster of points
	clusters = pd.Series([coords[cluster_labels==n] for n in range(num_clusters)])

	centermost_points = clusters.map(get_centermost_point)

	# unzip the list of centermost points (lat, lon) tuples into separate lat and lon lists
	loc = []
	lats, lons = zip(*centermost_points)
	for lat,lon in zip(lats,lons):
		loc.append([lat,lon])
	return loc

	
