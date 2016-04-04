import csv
import numpy as np
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot,savefig
from pylab import *
from scipy.stats import ttest_ind
from __future__ import print_function
from statsmodels.sandbox.regression.predstd import wls_prediction_std
 
 
def train_model(csv_read,hashtag):
    x1=[]
    x2=[]
    x3=[]
    x4=[]
    x5=[]
    x6=[]
    x7=[]
    x8=[]
    x9=[]
    x10=[]
    x11=[]
    x12=[]
    x13=[]
    x14=[]
    y=[]

    # read each feature values from the csv file
    for line in csv_read:
        x1.append(float(line[0]))
        x2.append(float(line[1]))
        x3.append(float(line[2]))
        x4.append(float(line[3]))
        x5.append(float(line[4]))
        x6.append(float(line[5]))
        x7.append(float(line[6]))
        x8.append(float(line[7]))
        x9.append(float(line[8]))
        x10.append(float(line[9]))
        x11.append(float(line[10]))
        x12.append(float(line[11]))
        x13.append(float(line[12]))
        x14.append(float(line[13]))
        y.append(float(line[14]))
    
    # use our selected feature only 
    X = np.column_stack((x1,x2,x3,x7,x8,x9,x13))

    # fit the linear regression model 
    model = sm.OLS(y, X)
    results = model.fit()
    # write the OLS Regression Results into the file 
    f=open('OLS_Regression_Results'+hashtag+'.txt','w')
    f.write(str(results.summary()))
    f.close

    # calculate the predicted number of tweet based on the linear regression model parameters
    y1=np.dot(X,results.params)

    # plot the predicted number of tweets versus each feature value in last 1 hour
    i=0
    feature_list=[x1,x2,x3,x7,x8,x9,x13]
    feature_name_list=['tweet','retweet','follower','favorite','statuses','ranking','usermetion']
    for feature in feature_list:
        plt.plot(feature,y,'bo')
        xlabel(feature_name_list[i]+' values in last 1 hour')
        ylabel('predicted number of tweets')
        savefig(feature_name_list[i]+'_vs_tweet_'+hashtag)
        plt.show()
        plt.clf()
        i=i+1

    # plot the predicted number of tweets versus actual number of tweets
    # (also plot a line y=x)
    plt.plot(y, y1,'bo',y,y,'r--')
    xlabel('Actuall number of tweets')
    ylabel('Predicted number of tweets')
    savefig('Predicted_vs_Actual'+hashtag)
    plt.show()
    plt.clf()

    
if __name__ == '__main__':
    hashtag_list=["#gohawks", "#gopatriots", "#nfl", "#patriots", "#sb49", "#superbowl"]
    for hashtag in hashtag_list:
        csv_read = csv.reader(file("Processed_Data_"+hashtag+".csv", 'rb'))
        train_model(csv_read, hashtag)