#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 08:53:50 2018

@author: Razander
"""

#Twitter Data collector

#initialize api
import tweepy
from tweepy import OAuthHandler
 
# ---------- INSERT API STUFF ----------
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

#stream tweets
import sys
from tweepy import Stream
from tweepy.streaming import StreamListener

#get tickers to track from TickersToTrack.txt
#what_to_track = open(sys.argv[1]).read().splitlines()
what_to_track = open('TickersToTrack.txt').read().splitlines()

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('twitterData.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print('error: ',status)
        return True

class CollectData():
    print('streaming in data...\n')
    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=what_to_track)

if __name__ == '__main__':
    collect = CollectData()
    collect.run()
