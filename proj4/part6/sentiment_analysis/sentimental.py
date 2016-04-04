import nltk
from nltk.classify.naivebayes import NaiveBayesClassifier
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


files = 'tweets_#gopatriots.txt'
files2 = 'tweets_#gohawks.txt'
# gopatriotsText = open('gopatriots_text.txt', 'a')
# with open(files,'r') as ifile:
#     for line in ifile.readlines():
#         tweet = json.loads(line)
#         tweet_text = tweet['tweet']['text'].encode("utf-8")
#         tweet_text = processTweet(tweet_text)
#         print >>  gopatriotsText, tweet_text
#         print >> gopatriotsText, classify_tweet(tweet['tweet']['text'])
# gopatriotsText.close()
# ifile.close()

gohawksText = open('gohawks_text.txt','a')
with open(files2,'r') as ifile:
    for line in ifile.readlines():
        tweet = json.loads(line)
        tweet_text = tweet['tweet']['text'].encode("utf-8")
        tweet_text = processTweet(tweet_text)
        print >>  gohawksText, tweet_text
        print >> gohawksText, classify_tweet(tweet['tweet']['text'])
gohawksText.close()
ifile.close()



# read in the test tweets and check accuracy
# to add your own test tweets, add them in the respective files
# test_tweets = read_tweets('happy_test.txt', 'positive')
# print test_tweets
# test_tweets.extend(read_tweets('sad_test.txt', 'negative'))
# total = accuracy = float(len(test_tweets))

# for tweet in test_tweets:
#     if classify_tweet(tweet[0]) != tweet[1]:
#         print classify_tweet(tweet[0])
#         accuracy -= 1

# print('Total accuracy: %f%% (%d/20).' % (accuracy / total * 100, accuracy))