import json
from datetime import datetime , timedelta
import pylab as plt

hashs=['tweets_#gopatriots.txt','tweets_#gohawks.txt','tweets_#patriots.txt','tweets_#sb49.txt', 'tweets_#nfl.txt','tweets_#superbowl.txt']
hashs2=['tweets_#nfl.txt']
#hashs2=['tweets_#superbowl.txt']

for files in hashs:  
    fseconds=0
    lseconds=0
    tempi=0
    followers=0
    users=set()
    #user_arr=[]
    with open(files,'r') as ifile:
        for line in ifile.readlines():
            tweet = json.loads(line)
            if tweet['tweet']['user']['id'] not in users:
                users.add(tweet['tweet']['user']['id'])
            #user_arr.append(tweet['tweet']['user']['id'])
                followers=followers + tweet['author']['followers']
            if tempi == 0:
                fseconds=tweet['firstpost_date']
                tempi=1
            lseconds=tweet['firstpost_date']
        ifile.close()
    thours=((lseconds-fseconds)/3600)+0.00
    totalusers=len(users)
    with open(files,'r') as ifile:
        counts = [0]*(int(thours)+1)
        i=-1
        retweets=0
        
        length=0
        hcount=0
        for line in ifile.readlines():
             tweet = json.loads(line)
             i=((tweet['firstpost_date']-fseconds)/3600)
             counts[i]=counts[i]+1
             length=length+1
             retweets=retweets + tweet['metrics']['citations']['total']
             
                 
   #length = max(length,tweet['tweet']['retweet_count'])
        xaxis = [0]*(int(thours)+1)
        j=0
        k=0
        tsum=0
        while j <=int(thours):
            xaxis[j]=j
            if counts[j] >0:
                k=k+1
                tsum=tsum+counts[j]
            j=j+1
        #if (files == 'tweets_#superbowl.txt' or files == 'tweets_#nfl.txt'):
        #bar1 = plt.bar( xaxis,counts)
        #plt.show()

        print files    
        print "total tweets: "+str(tsum)
        print "total time: "+str(thours+1)
        #print "total users: "+ str(totalusers)
        print ":Average number of tweets per hour:"+str((tsum+0.0)/(thours+1.0))
        print ":total retweets:"+str((retweets+0.0))
        print ":Average number of retweets per tweet:"+str((retweets+0.0)/(length+0.0))
        print ":total_followers:"+str(followers+0.0)
        print ":Average number of followers per user:"+str((followers+0.0)/(totalusers+0.0))
        ifile.close()

# for files in hashs2:  
#     fseconds=0
#     lseconds=0
#     tempi=0
#     followers=0
#     users=set()
#     with open(files,'r') as ifile:
#         for line in ifile.readlines():
#             tweet = json.loads(line)
#             if tweet['tweet']['user']['id'] not in users:
#                 users.add(tweet['tweet']['user']['id'])
#                 followers=followers + tweet['author']['followers']
#             if tempi == 0:
#                 fseconds=tweet['firstpost_date']
#                 tempi=1
#             lseconds=tweet['firstpost_date']
#         ifile.close()
#     thours=((lseconds-fseconds)/3600)
#     totalusers=len(users)
#     with open(files,'r') as ifile:
#         counts = [0]*(thours+1)
#         i=-1
#         retweets=0
        
#         length=0
#         hcount=0
#         for line in ifile.readlines():
#              tweet = json.loads(line)
#              i=((tweet['firstpost_date']-fseconds)/3600)
#              counts[i]=counts[i]+1
#              length=length+1
#              retweets=retweets + tweet['metrics']['citations']['total']
             
                 
#    #length = max(length,tweet['tweet']['retweet_count'])
#         xaxis = [0]*(thours+1)
#         #x_time = [0]*(thours+1)
#         j=0
#         k=0
#         tsum=0
#         while j <=thours:
#             xaxis[j]=j
#            # x_time[j]=datetime.fromtimestamp(float(fseconds+j)).strftime('%H:%M:%S')
#             if counts[j] >0:
#                 k=k+1
#                 tsum=tsum+counts[j]
#             j=j+1
#         #if (files == 'tweets_#superbowl.txt' or files == 'tweets_#nfl.txt'):
#         bar1 = plt.bar( xaxis,counts)
#         plt.ylabel('count')
#         plt.xlabel('time')
#         plt.title('number of tweets in hour'+ files)
#         plt.show()

#         print files    
#         print "total tweets: "+str(tsum)
#         #print "total users: "+ str(totalusers)
#         print ":Average number of tweets per hour:"+str((tsum+0.0)/(thours+0.0))
#         print ":Average number of retweets per tweet:"+str((retweets+0.0)/(length+0.0))
#         print ":Average number of followers per user:"+str((followers+0.0)/(totalusers+0.0))
#         ifile.close()


    