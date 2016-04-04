import folium, pandas, ast
import json
import re
import nltk
from nltk.classify.naivebayes import NaiveBayesClassifier

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

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


def read_tweets(fname, t_type):
    tweets = []
    f = open(fname, 'r')
    line = f.readline()
    while line != '':
        tweets.append([line, t_type])
        line = f.readline()
    f.close()
    return tweets


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
      features['contains(%s)' % word] = (word in document_words)
    return features


def classify_tweet(tweet):
    return \
        classifier.classify(extract_features(nltk.word_tokenize(tweet)))


# read in postive and negative training tweets
pos_tweets = read_tweets('happy.txt', 'positive')
neg_tweets = read_tweets('sad.txt', 'negative')

# filter away words that are less than 3 letters to form the training data
tweets = []
for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))


# extract the word features out from the training data
word_features = get_word_features(\
                    get_words_in_tweets(tweets))


# get the training set and train the Naive Bayes Classifier
training_set = nltk.classify.util.apply_features(extract_features, tweets)
classifier = NaiveBayesClassifier.train(training_set)



locations_negative = []
locations_positive = []
geos_p = []
files = 'tweets_#gohawks.txt'   
match_patriot=re.compile('patriot')
match_hawks = re.compile('hawks')
with open(files,'r') as ifile:
        for line in ifile.readlines():
            tweet = json.loads(line)
            tweet_text = tweet['tweet']['text']
            tweet_text = processTweet(tweet_text)
            if tweet['tweet']['geo'] is not None:
                if classify_tweet(tweet_text) == "negative":  
            	   locations_negative.append(tweet['tweet']['geo']['coordinates'])
                else:
                    locations_positive.append(tweet['tweet']['geo']['coordinates'])
ifile.close()



# initialize and create map
tweet_map= folium.Map(location=[52.8, -2], tiles='Mapbox Bright', zoom_start=7)

# add markers
for geo in locations_negative:
	tweet_map.circle_marker(location=geo, radius=250, line_color='#3186cc')

for geo in locations_positive:
	tweet_map.circle_marker(location=geo, radius=250, line_color='#E91616')

tweet_map.create_map(path='posVSneg_hawks_map.html')

