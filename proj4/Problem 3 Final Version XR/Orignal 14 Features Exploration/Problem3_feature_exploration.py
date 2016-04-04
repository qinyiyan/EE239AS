import csv 
import sys
import json
import time
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pylab import *
from __future__ import division
from __future__ import with_statement


# convert the month tag in the timestamp into number 
def month_convert(time):
    for i in range (len(time)):
        if 'Dec' in time[i]:
            time[i]= time[i].replace('Dec','12')
        elif 'Jan' in time[i]:
            time[i]=time[i].replace('Jan','01')
        elif 'Feb' in time[i]:
            time[i]=time[i].replace('Feb','02')
    return time


# apply time window (1h) for the data to extract features
def apply_time_window(tweet_num, feature):
    feature_each_hour=[]
    for num in tweet_num:
        if len(feature)==0:
            break
        elif num==0:       
            feature_each_hour.append(0)
        else:
            num_each=0
            for i in range(num):
                if len(feature)==0:
                    break
                else:
                    num_each=num_each+feature.pop(0)
            feature_each_hour.append(num_each)
    return feature_each_hour


# plot number of tweets versus feature value and save corresponding figure	
def customed_plot(feature, tweets_num, hashtag, feature_name):
    plt.plot(feature, tweets_num,'bo')
    plt.xlabel(feature_name + ' value in each 1-hour window')
    plt.ylabel('number of tweets in each 1-hour window')
    plt.savefig('tweets_vs_' + feature_name + '_' + hashtag)
    plt.show()
    plt.clf()


def feature_exploration(hashtag):

    title=[]
    post_date=[]
    follower=[]
    citations=[]
    acceleration=[]
    favorite=[]
    influential=[]
    matching=[]
    momentum=[]
    ranking=[]
    statuses=[]
    user_metion=[]
    emotion=[]
 
    # get each original feature data from file 
    with open("tweets_"+hashtag+".txt") as f:
        for line in f:
            result=json.loads(line)
            title.append(result["title"])
            post_date.append(result["tweet"]["created_at"])
            follower.append(result["author"]["followers"])
            citations.append(result["metrics"]["citations"]["total"])
            acceleration.append(result["metrics"]["acceleration"])
            favorite.append(result["tweet"]["favorite_count"])
            influential.append(result["metrics"]["citations"]["influential"])
            matching.append(result["metrics"]["citations"]["matching"])
            momentum.append(result["metrics"]["momentum"])
            ranking.append(result["metrics"]["ranking_score"])
            statuses.append(result["tweet"]["user"]["statuses_count"])

    for metion in title:
        user_metion.append(metion.count("@"))
  
    for content in title:
        if (content.find("!!!")>0 or content.find("???")>0):
            emotion.append(1)
        else:
            emotion.append(0)

    follower_copy=[]
    follower_copy=follower_copy+follower

    time=[]
    for time_stamp in post_date:
        time.append(json.dumps(time_stamp[-4:]+time_stamp[-5]+time_stamp[4:19]))
    time=month_convert(time)

    # create a list which contains the start and end of each time window (1h)
    start_date_all = datetime.datetime(int(time[0][1:5]),int(time[0][6:8]),int(time[0][9:11]), int(time[0][12:14]),00,0)
    end_date_all = datetime.datetime(int(time[-1][1:5]),int(time[-1][6:8]),int(time[-1][9:11]), int(time[-1][12:14])+1,00,0)
    delta = datetime.timedelta(hours=1)
    time_interval=[]
    while start_date_all < end_date_all:
        end_date = start_date_all + delta
        time_interval.append(end_date.strftime("%Y %m %d %H:%M:%S"))
        start_date_all += delta

    time_of_the_day=[]
    for time_stamp in time_interval:
        time_of_the_day.append(time_stamp[11:13])

    number_each_hour=[]   
    for time_limit in time_interval:
        count=0
        for time_stamp in time:
            count+=1
            if time_stamp[1:-1]>time_limit:
                number_each_hour.append(count)
                break


    # get the number of tweets in each 1h time window
    tweet_num=[]
    for i in range (len(number_each_hour)):
        number_each_hour[i]=number_each_hour[i]-1

    tweet_num.append(number_each_hour[0])
    for i in range (len(number_each_hour)-1):
        tweet_num.append(number_each_hour[i+1]-number_each_hour[i])   
    tweet_num.append(count-number_each_hour[-1])


    # create time window (1h) from the data to extract features
    # each window will provide a sample for the following regression model trainning 
    retweet_each_hour=apply_time_window(tweet_num, citations)
    follower_each_hour=apply_time_window(tweet_num, follower)
    acceleration_each_hour=apply_time_window(tweet_num, acceleration)
    favorite_each_hour=apply_time_window(tweet_num, favorite)
    influential_each_hour=apply_time_window(tweet_num, influential)
    matching_each_hour=apply_time_window(tweet_num, matching)  
    momentum_each_hour=apply_time_window(tweet_num, momentum)
    ranking_each_hour=apply_time_window(tweet_num, ranking)	
    statuses_each_hour=apply_time_window(tweet_num, statuses)
    emotion_each_hour=apply_time_window(tweet_num, emotion)
    usermetion_each_hour=apply_time_window(tweet_num, user_metion)
    
    # caculate maximum number of followers in each hour seperately, since the method is a little different
    max_follower_each_hour=[]
    for num in tweet_num:
        if len(follower_copy)==0:
            break
        elif num==0:
            max_follower_each_hour.append(0)
        else:
            num_each=[]
            for i in range(num):
                if len(follower_copy)==0:
                    break
                else:
                    num_each.append(follower_copy.pop(0))
            max_follower_each_hour.append(max(num_each))


    # save the processed data which can be used for trainning model in a csv file for each hashtag       
    csv_file = open("Processed_Data_"+hashtag+".csv", 'wb')
    csv_write = csv.writer(csv_file) 
    csv_write.writerow(tweet_num)
    csv_write.writerow(retweet_each_hour)
    csv_write.writerow(follower_each_hour)
    csv_write.writerow(max_follower_each_hour)
    csv_write.writerow(time_of_the_day)   
    csv_write.writerow(acceleration_each_hour)
    csv_write.writerow(favorite_each_hour)
    csv_write.writerow(influential_each_hour)
    csv_write.writerow(matching_each_hour)
    csv_write.writerow(momentum_each_hour)
    csv_write.writerow(ranking_each_hour)
    csv_write.writerow(statuses_each_hour)
    csv_write.writerow(usermetion_each_hour)
    csv_write.writerow(emotion_each_hour)
    

    # plot number of tweets versus each feature value
    customed_plot(retweet_each_hour,tweet_num,hashtag,'retweet')
    customed_plot(follower_each_hour,tweet_num,hashtag,'follower')
    customed_plot(max_follower_each_hour,tweet_num,hashtag,'max_follower') 
    customed_plot(time_of_the_day,tweet_num,hashtag,'time_of_the_day')
    customed_plot(acceleration_each_hour,tweet_num,hashtag,'acceleration')
    customed_plot(favorite_each_hour,tweet_num,hashtag,'favorite')
    customed_plot(influential_each_hour,tweet_num,hashtag,'influential')
    customed_plot(matching_each_hour,tweet_num,hashtag,'matching')
    customed_plot(momentum_each_hour,tweet_num,hashtag,'momentum')
    customed_plot(ranking_each_hour,tweet_num,hashtag,'ranking')
    customed_plot(statuses_each_hour,tweet_num,hashtag,'statuses')
    customed_plot(usermetion_each_hour,tweet_num,hashtag,'usermetion')
    customed_plot(emotion_each_hour,tweet_num,hashtag,'emotion')


if __name__ == '__main__':
    hashtag_list=["#gohawks", "#gopatriots", "#nfl", "#patriots", "#sb49", "#superbowl"]
    for hashtag in hashtag_list:
        print(hashtag)
        feature_exploration(hashtag)