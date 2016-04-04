import folium, pandas, ast
import json
# -*- coding: utf-8 -*-
locations_p = []
geos_p = []
files = 'tweets_#gopatriots.txt'
# get geo data only from rows with non-empty values
with open(files,'r') as ifile:
        for line in ifile.readlines():
            tweet = json.loads(line)
            if tweet['tweet']['geo'] is not None:
            	locations_p.append(tweet['tweet']['geo']['coordinates'])

ifile.close()

locations_h = []
files = 'tweets_#gohawks.txt'
with open(files,'r') as ifile:
        for line in ifile.readlines():
            tweet = json.loads(line)
            if tweet['tweet']['geo'] is not None:
            	locations_h.append(tweet['tweet']['geo']['coordinates'])

ifile.close()
# for location in locations:
#   # add to geos array an evaluated python literal syntax of the data
#  	geos.append(ast.literal_eval(location))

# initialize and create map
tweet_map= folium.Map(location=[52.8, -2], tiles='Mapbox Bright', zoom_start=7)

# add markers
for geo in locations_p:
	tweet_map.circle_marker(location=geo, radius=250, line_color='#E91616')

for geo in locations_h:
	tweet_map.circle_marker(location=geo, radius=250, line_color='#3186cc')


tweet_map.create_map(path='map.html')

