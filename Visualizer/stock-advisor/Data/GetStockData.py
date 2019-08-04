# https://stackoverflow.com/questions/44225771/scraping-historical-data-from-yahoo-finance-with-python
# Data is retrieved for tickers given in the filename variable

import re
import urllib.request
from io import StringIO
from datetime import datetime, timedelta, date

import requests
import pandas as pd

#gets data for short (a few months back) time periods
'''class PandasDataReaderHistory:
    
    # Import stock data using pandasreader
    def getData(self, startDate, endDate):
        df = pdr.get_data_quandl(self.ticker, start=startDate, end=endDate)
        df = df.reindex(index=df.index[::-1]) #flip index so 0th row is oldest date
        return df
    
    def __init__(self, ticker): #executed when an sma object in created
        self.ticker = str(ticker)   #must be all caps string (e.g. "MSFT")
        outputfilename='Data/Data/'+self.ticker+'.csv'
        
        total = 0 #track total number of tickers processed
        alreadyUpToDate = [] #track how many files were already up to date
        updated = [] #track how many files were updated
        errored = [] #track which stocks were has errors
        #try:
        print('Data/Data/'+str(self.ticker)+'.csv')
        df = pd.read_csv('Data/Data/'+str(self.ticker)+'.csv')
        print('in')
        #update file if it exists
        #check if the df's latest date is today's date, otherwise update
        if df['Date'].tail(1).item()==date.today().__str__():
            print('here3')
            #print('already up to date') #do nothing
            alreadyUpToDate.append(self.ticker)
        else:
            print('here2')
            print(str(df['Date'].tail(1).item()))
            days_back = (date.today()-datetime.strptime(df['Date'].tail(1).item(),"%Y-%m-%d").date()).days
            #check if you have Friday's data and it's Saturday/Sunday 
            if days_back < 3 and date.today().weekday() > 4:
                alreadyUpToDate.append(self.ticker)
            else:
                df2 = pdr.get_data_quandl(self.ticker, start=df['Date'].tail(1).item(), end=date.today())
                print('head\n',df2.head())
                df2 = df2.reindex(index=df.index[::-1])
                df = pd.concat([df, df2])
                #df.to_csv(path_or_buf=outputfilename)
                updated.append(self.ticker)
        #except as e: #if file doesn't exist, make it
        #print(e) 
        try:
            print('here1')
            #get last year of data
            df = getData(self.ticker,date.today() - timedelta(365),date.today())
            df.to_csv(path_or_buf=outputfilename)
            updated.append(self.ticker)
        except: 
            print('here')
            errored.append(ticker)
                
        #print download diagnostics
        print(str(len(alreadyUpToDate))+' out of '+str(total)+' were already up-to-date')
        print(str(len(updated))+' out of '+str(total)+' were updated')
        if len(errored) > 0:
            print(str(errored)+' errored')
            
'''
#gets data for long time periods
class YahooFinanceHistory:
    timeout = 2
    crumb_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
    crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
    quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{quote}?period1={dfrom}&period2={dto}&interval=1d&events=history&crumb={crumb}'

    def __init__(self, symbol, days_back=7):
        self.symbol = symbol
        self.session = requests.Session()
        self.dt = timedelta(days=days_back)

    def get_crumb(self):
        response = self.session.get(self.crumb_link.format(self.symbol), timeout=self.timeout)
        response.raise_for_status()
        match = re.search(self.crumble_regex, response.text)
        if not match:
            raise ValueError('Could not get crumb from Yahoo Finance')
        else:
            self.crumb = match.group(1)

    def get_quote(self):
        if not hasattr(self, 'crumb') or len(self.session.cookies) == 0:
            self.get_crumb()
        now = datetime.utcnow()
        dateto = int(now.timestamp())
        datefrom = int((now - self.dt).timestamp())
        url = self.quote_link.format(quote=self.symbol, dfrom=datefrom, dto=dateto, crumb=self.crumb)
        response = self.session.get(url)
        response.raise_for_status()
        # --- original line below ---
        #return pd.read_csv(StringIO(response.text), parse_dates=['Date'])
        # --- new line below ---
        #Modified to force numerical values to be float types and avoid object type. added by AJ
        return pd.read_csv(StringIO(response.text), parse_dates=['Date'],na_values='.')
   
    #def updateData(self):
        # --- UPDATE TICKER DATA ---
filename="Data/TickersToTrack.txt"
print('Fetching data for tickers in '+filename)
file=open(filename,"r")
total = 0 #total number of tickers processed (attempted)
alreadyUpToDate = [] #track which tickers were already up to date
updated = [] #track which tickers were updated
errored = [] #track which tickers encounted errors

for ticker in file:
    ticker=ticker.strip('\n')
    outputfilename='Data/Data/'+ticker+'.csv'
    total = total+1
    try: #check if file exists
        df = pd.read_csv('Data/Data/'+ticker+'.csv')
        days_back = (date.today()-datetime.strptime(df['Date'].tail(1).item(),"%Y-%m-%d").date()).days
        #if updating during a weekend, days_back needs to be reduced (sat -1; sun -2)
        if date.today().weekday() > 4:
            days_back = days_back-(date.today().weekday()-4)
        yesterday = datetime.strftime(datetime.now()-timedelta(1), "%Y-%m-%d")
        today = datetime.strftime(datetime.now()-timedelta(1), "%Y-%m-%d")
        #check if the df's latest date is yesterday's date, otherwise update
        if df['Date'].tail(1).item()==yesterday:
            print(ticker,'is already up to date') #do nothing
            alreadyUpToDate.append(ticker)
        elif days_back <= 2 and date.today().weekday() > 4: #check that's it's not a weekend
            print(ticker,'is update to date enough. Try again Monday')
            alreadyUpToDate.append(ticker)
        else:
            try:
                print(ticker,'is updating')
                df2 = YahooFinanceHistory(ticker, days_back=days_back).get_quote()
                df2['Date'] = df2['Date'].dt.strftime("%Y-%m-%d")
                df = pd.concat([df,df2], join='inner', ignore_index=True) #force format of dataframe
                df = df.reset_index(drop=True)
                df.to_csv(path_or_buf=outputfilename)
                updated.append(ticker)
            except (urllib.error.HTTPError, requests.exceptions.HTTPError) as err:
                print('HTTP error for '+ticker)
                errored.append(ticker)
                continue
    except (FileNotFoundError) as err: #if file doesn't exist, make it
        try:
            print(ticker+' is getting a new file and updating')
            days_back = 365*10
            df = YahooFinanceHistory(ticker, days_back=days_back).get_quote()
            df.to_csv(path_or_buf=outputfilename)
            updated.append(ticker)
        except (urllib.error.HTTPError, requests.exceptions.HTTPError) as err:
            print('HTTP error for '+ticker)
            errored.append(ticker)
            continue
file.close()

#print download diagnostics
print('\n'+str(len(alreadyUpToDate))+' out of '+str(total)+' were already up-to-date')
print(str(len(updated))+' out of '+str(total)+' were updated')
if len(errored) > 0:
    print(str(errored)+' errored')
    