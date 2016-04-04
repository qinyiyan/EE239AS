import folium, pandas, ast
import json
import re
# -*- coding: utf-8 -*-


def processTweet(tweet):
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))',' ',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+',' ',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s+])', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    
    return tweet

locations_p = []
locations_h = []
geos_p = []
files = 'tweets_#superbowl.txt'   
match_patriot=re.compile('patriot')
match_hawks = re.compile('hawks')
with open(files,'r') as ifile:
        for line in ifile.readlines():
            tweet = json.loads(line)
            tweet_text = tweet['tweet']['text']
            tweet_text = processTweet(tweet_text)
            if tweet['tweet']['geo'] is not None:
                if match_patriot.search(tweet_text) is not None:  
            	   locations_p.append(tweet['tweet']['geo']['coordinates'])
                if match_hawks.search(tweet_text) is not None:
                    locations_h.append(tweet['tweet']['geo']['coordinates'])
ifile.close()



# initialize and create map
tweet_map= folium.Map(location=[52.8, -2], tiles='Mapbox Bright', zoom_start=7)

# add markers
for geo in locations_h:
	tweet_map.circle_marker(location=geo, radius=250, line_color='#E91616')

for geo in locations_p:
	tweet_map.circle_marker(location=geo, radius=250, line_color='#3186cc')

tweet_map.create_map(path='superbowl_map.html')

