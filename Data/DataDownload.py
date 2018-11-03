import pandas as pd
from time import sleep
from alpha_vantage.timeseries import TimeSeries


ts = TimeSeries(key='3ZYW8IZMDJJOJMLR',retries=10,output_format='pandas', indexing_type='integer')
testDF = pd.DataFrame()
trainDF = pd.DataFrame()

symbols = open('DowJonesTickers.txt','r')
for x in symbols:
    ticket = x.rstrip()
    #print(ticket)
    data, meta_data = ts.get_daily_adjusted(symbol=ticket,outputsize="full")
    print(data[0])

print(xData[[0]])

