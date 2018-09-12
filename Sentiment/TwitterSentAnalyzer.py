#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 18:42:39 2018

@author: Razander
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import datetime

#import data
df = pd.DataFrame()
dates = ['Apr_01_2018','Apr_02_2018','Apr_05_2018'] #'Apr_03_2018','Apr_04_2018'
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
    #plt.plot(data['Date'],data['Sentiment'],'-r')
    #plt.title(s)
    #plt.xlabel('Date')
    #plt.ylabel('Sentiment')
    
    #plot tickers with stock price
    startDate = datetime.datetime(2018, 2, 1)
    endDate = datetime.datetime(2018, 2, 5)     #must be datetime.datetime(yyyy,mm,dd)

    # Import stock data using pandasreader
    try:
        dfstock = pdr.get_data_quandl(tick[1::], start=startDate, end=endDate)
        dfstock = dfstock.reindex(index=dfstock.index[::-1]) #flip index so 0th row is oldest date
    
        plt.plot(dfstock['Close'],data['Sentiment'],'g-')
        plt.title('Close to Sentiment: '+tick[1::])
        plt.xlabel('Close')
        plt.ylabel('Sentiment')
        plt.show()
    except:
        print("Couldn't get data for ticker: "+tick[1::])