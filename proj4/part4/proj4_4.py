import os
import json
import datetime, time
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import random

filename = "tweets_#gopatriots.txt"

tweets = []
f=open(filename)
count = 0
for line in f:
	print (count)
	if count>=0:
		try: 
			tweet=json.loads(line)
			tweets.append([tweet['firstpost_date'],tweet['metrics']['citations']['total'],tweet['author']['followers'],tweet['tweet']['favorite_count'],tweet['tweet']['user']['friends_count'],tweet['metrics']['ranking_score'],tweet['tweet']['user']['statuses_count']])
			count=count+1
		except:
			print ("Failed to read input file.")
	else:
		break
f.close()

time1 = int(time.mktime(datetime.datetime(2015,0o2,0o1, 8,00,0).timetuple()))
time2 = int(time.mktime(datetime.datetime(2015,0o2,0o1, 20,00,0).timetuple()))

tweet_firstpost_date=[tweet[0] for tweet in tweets]
start=min(tweet_firstpost_date)
end=max(tweet_firstpost_date)
interval = (end-start)//3600
# print interval

time_window = [[0 for i in range(10)] for j in range(interval+2)]
interval1=0
interval2=0
for i in range(len(tweets)):
	cur_time = tweets[i][0]

	index = (cur_time-start)//3600

	if cur_time<time1:
		interval1=index
		interval2=interval1
	elif cur_time<time2:
		interval2=index
#choose features
	#number of tweets
	time_window[index][0] = time_window[index][0]+1
	#retweets
	time_window[index][1] = time_window[index][1]+tweets[i][1]
	# time_window[index][2] = max(time_window[index][2],tweets[i][2])
	#followers
	time_window[index][2] = time_window[index][2]+tweets[i][2]
	#favourite
	time_window[index][3] = time_window[index][2]+tweets[i][3]
	#friends
	time_window[index][4] = time_window[index][4]+tweets[i][4]
	#ranking score
	time_window[index][5] = time_window[index][5]+tweets[i][5]
	#statuses
	time_window[index][6] = time_window[index][6]+tweets[i][6]
	# number of tweets_real
	time_window[index-1][7] = time_window[index][0]

time_window_random = random.sample(time_window, len(time_window))

print (len(time_window),interval1,interval2)

y=[]

for i in range(interval+1):
	y.append(time_window_random[i][7])

x=[]

for i in range(interval+1):
	x.append(time_window_random[i][0:7])

X = np.array(x)
Y = np.array(y)

# cross_validation(X,Y,0)
def cross_validation(X,Y,period):
	len10 =  len(X)//10
	cross_err = []
	cross_avg = []
	print ("period: "+str(period))
	for i in range(10):
		#split data
		train = np.delete(X,np.s_[len10*i:len10*(i+1)],0)
		target = np.delete(Y,np.s_[len10*i:len10*(i+1)],0)

		test_input = X[len10*i:len10*(i+1)] 
		test_real = Y[len10*i:len10*(i+1)]
		#train model
		model = sm.OLS(target, train) 
		results = model.fit()

		pred_err1=0

		for i in range(len(target)):
			pred_err1 +=  abs(target[i]-sum(results.params*train[i]))
		print (len(target),pred_err1//len(target))
		# 10% validate
		pred_err=0
		for i in range(len10):
			pred_err +=  abs(test_real[i]-sum(results.params*test_input[i]))
		cross_err.append(round(pred_err//len10,2))
		cross_avg.append(round(np.mean(test_real),2))
	
	avg_err=np.mean(cross_err)
		
	f = open("cross_validation_gopatriots.txt",'a')
	

	print("cross_error of period "+str(period)+" :", file=f)
	print(cross_err, file=f)
	print("cross_avg of period "+str(period)+" :", file=f)
	print(cross_avg, file=f)
	print("cross_error_avg of period "+str(period)+" :", file=f)
	print(avg_err, file=f)
	# print>>f,"model params:"
	# print>>f,results.params
	#print>>f,""
	print("", file=f)
	f.close()
		

X1 = X[0:interval1+1]
Y1 = Y[0:interval1+1]
cross_validation(X1,Y1,0)

X2 = X[interval1+1:interval2+1]
Y2 = Y[interval1+1:interval2+1]

cross_validation(X2,Y2,1)

X3 = X[interval2:]
Y3 = Y[interval2:]
cross_validation(X3,Y3,2)

#def validation():
    #directory=os.getcwd()
    #print (directory)
    #for file in os.listdir(directory+"/proj3"):
     #   if file.endswith('.txt'):
      #      getValidation("proj3/"+file)

#validation()
