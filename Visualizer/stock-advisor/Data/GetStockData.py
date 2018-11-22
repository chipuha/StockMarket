# https://stackoverflow.com/questions/44225771/scraping-historical-data-from-yahoo-finance-with-python
# Data is retrieved for tickers given in the filename variable

import re
import urllib.request
from io import StringIO
from datetime import datetime, timedelta, date

import requests
import pandas as pd

#gets data for short (a few months back) time periods
class PandasDataReaderHistory:
    
    def __init__(self, ticker): #executed when an sma object in created
        self.ticker = str(ticker)   #must be all caps string (e.g. "MSFT")
        outputfilename='CSVs/'+self.ticker+'.csv'
        
        total = 0 #track total number of tickers processed
        alreadyUpToDate = [] #track how many files were already up to date
        updated = [] #track how many files were updated
        errored = [] #track which stocks were has errors
        try:
            print('CSVs/'+str(self.ticker)+'.csv')
            df = pd.read_csv('CSVs/'+str(self.ticker)+'.csv')
            print('in')
            #update file if it exists
            #check if the df's latest date is today's date, otherwise update
            if df['Date'].tail(1).item()==date.today().__str__():
                print('here3')
                #print('already up to date') #do nothing
                alreadyUpToDate.append(self.ticker)
            else:
                print('here2')
                days_back = (date.today()-datetime.strptime(df['Date'].tail(1).item(),"%Y-%m-%d").date()).days
                #check if you have Friday's data and it's Saturday/Sunday 
                if days_back < 3 and date.today().weekday() > 4:
                    alreadyUpToDate.append(self.ticker)
                else:
                    df2 = getData(self.ticker,df['Date'].tail(1).item(),date.today())
                    df = df.append(df2)
                    df.to_csv(path_or_buf=outputfilename)
                    updated.append(self.ticker)
        except: #if file doesn't exist, make it
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
        
    # Import stock data using pandasreader
    def getData(self, startDate, endDate):
        df = pdr.get_data_quandl(self.ticker, start=startDate, end=endDate)
        df = df.reindex(index=df.index[::-1]) #flip index so 0th row is oldest date
        return df
            
    
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
   
    def updateData(self):
        filename="DowJonesTickers.txt"
        print('getting tickers from '+filename)
        file=open(filename,"r")
        total = 0 #track total number of tickers processed
        alreadyUpToDate = [] #track how many files were already up to date
        updated = [] #track how many files were updated
        errored = [] #track which stocks were has errors
        for ticker in file:
            ticker=ticker.strip('\n')
            print('working on ticker '+ticker)
            outputfilename='CSVs/'+ticker+'.csv'
            total = total+1
            try: #check if file exists
                df = pd.read_csv('CSVs/'+ticker+'.csv')
                #update file if it exists
                #check if the df's latest date is today's date, otherwise update
                if df['Date'].tail(1).item()==date.today().__str__():
                    #print('already up to date') #do nothing
                    alreadyUpToDate.append(ticker)
                else:
                    days_back = (date.today()-datetime.strptime(df['Date'].tail(1).item(),"%Y-%m-%d").date()).days
                    #check if you have Friday's data and it's Saturday/Sunday 
                    if days_back < 3 and date.today().weekday() > 4:
                        alreadyUpToDate.append(ticker)
                    else:
                        df2 = YahooFinanceHistory(ticker, days_back=days_back).get_quote()
                        df = df.append(df2)
                        df.to_csv(path_or_buf=outputfilename)
                        updated.append(ticker)
            except: #if file doesn't exist, make it
                try:
                    df = YahooFinanceHistory(ticker, days_back=365*10).get_quote()
                    df.to_csv(path_or_buf=outputfilename)
                    updated.append(ticker)
                except(requests.exceptions.HTTPError,requests.exceptions.ReadTimeout) as err:
                    print('HTTP error for '+ticker)
                    print('Moving on to next ticker')
                    errored.append(ticker)
        #print download diagnostics
        print(str(len(alreadyUpToDate))+' out of '+str(total)+' were already up-to-date')
        print(str(len(updated))+' out of '+str(total)+' were updated')
        if len(errored) > 0:
            print(str(errored)+' errored')
    