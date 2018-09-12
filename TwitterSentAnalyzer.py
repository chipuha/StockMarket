#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 18:42:39 2018

@author: Razander
"""

import csv
import pandas as pd

#import data
df = pd.DataFrame()
dates = ['Apr_01_2018','Apr_02_2018','Apr_03_2018','Apr_04_2018','Apr_05_2018']
for date in dates:
    fname = 'TwitterData/TwitterSentiment-'+date+'.txt'
    sent = []
    df = df.append(pd.read_csv(fname,sep=' ',header=0))

#import what tickers were being monitored on twitter
tickers = open('TickersToTrack.txt').read().splitlines()

#plot and to some analysis
for tick in tickers:
    s = tick.lower()
    data = df[df.Stock == s]
    plt.plot(data['Date'],data['Sentiment'])
    plt.title(s)
    plt.xlabel('Date')
    plt.ylabel('Sentiment')
    plt.show()