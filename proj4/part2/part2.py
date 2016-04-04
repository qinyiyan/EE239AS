import urllib
import httplib
import json
import numpy as np
from statsmodels.formula.api import ols
import statsmodels.api as sm
from datetime import datetime , timedelta

import pylab as plt
from pandas import *

# -*- coding: utf-8 -*-
# getting max number of retweets



#hashs=['tweets_#superbowl.txt','tweets_#sb49.txt','tweets_#patriots.txt','tweets_#nfl.txt','tweets_#gopatriots.txt','tweets_#gohawks.txt']
hashs=['tweets_#superbowl.txt']

for files in hashs: 
    fseconds=0
    lseconds=0
    tempi=0
    #users=set()
    users_arr = []
    with open(files,'r') as ifile:
        for line in ifile.readlines():
            tweet = json.loads(line)
            #if tweet['tweet']['user']['id'] not in users:
                #users.add(tweet['tweet']['user']['id'])
            users_arr.append(tweet['tweet']['user']['id'])
            if tempi == 0:
                fseconds=tweet['firstpost_date']
                tempi=1
            lseconds=tweet['firstpost_date']
        ifile.close()
    thours=((lseconds-fseconds)/3600)
    totalusers=len(users_arr)
    
    with open(files,'r') as ifile:
        counts = [0]*(thours+1)
        i=-1
        retweets= [0]*(thours+1)
        followers= [0]*(thours+1)
        length=0
        tmax= [0]*(thours+1)
        #users=set()
        users_arr = []  
        for line in ifile.readlines():
             tweet = json.loads(line)
             i=((tweet['firstpost_date']-fseconds)/3600)
             counts[i]=counts[i]+1
             length=length+1
             retweets[i]=retweets[i] + tweet['metrics']['citations']['total']
             
             #if(tweet['tweet']['user']['id'] not in users):
             followers[i]=followers[i] + tweet['author']['followers']
             #users.add(tweet['tweet']['user']['id'])
             users_arr.append(tweet['tweet']['user']['id'])
             tmax[i]=max(tmax[i],tweet['author']['followers'])
             
             
       #length = max(length,tweet['tweet']['retweet_count'])
        time=[0]*(thours+1)
        results=[0]*(thours+1)
        j=0
        while j < thours:
            time[j]=j%24
            results[j]=counts[j+1]
            j=j+1
        results[thours]=counts[0]
        # print counts
        # print retweets
        # print followers
        # print tmax
        # print time
        # print results
        dataset=np.array([counts,retweets,followers,tmax,time])
        dataset=dataset.transpose()
        Y = dataset[1:,0]
        X = dataset[:-1, 0:5]
        X_res = dataset[0,0:5]
        #dta=DataFrame(dataset, columns=['counts', 'retweets','followers','tmax','time','results'])

        #formula = 'results ~ counts + retweets + tmax + time + followers'
        #res = sm.formula.ols(formula, dta).fit()
        model = sm.OLS(Y,X)
        fitting = model.fit()
        result = fitting.predict(X_res)
        print counts
        print result
        #print Y[1]
        Linear_Regression_model1 = open('Linear_Regression_model1.txt', 'a')
        predict_result = open('Linear_Regression_model2.txt', 'a')
        print >>Linear_Regression_model1, files
        print >>Linear_Regression_model1, fitting.summary()
        print >>predict_result, result
        Linear_Regression_model1.close()
        predict_result.close()

        # y=[]
        # for i in range(len(counts)):
        #     y.append(counts[i])
        # Y = np.array(y)
        # Y.rotate(-1)
        # X = np.array([counts,retweets,followers,tmax,time])
        # model = sm.OLS(Y,X)
        # results = model.fit()
        # Linear_Regression_model2 = open('Linear_Regression_model.txt2', 'a')
        # print >>Linear_Regression_model2, files
        # print >>Linear_Regression_model2, results.summary()
        # Linear_Regression_model2.close()


        ifile.close()