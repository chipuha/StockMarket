# https://stackoverflow.com/questions/44225771/scraping-historical-data-from-yahoo-finance-with-python
# Data is retrieved for tickers given in the filename variable

import re
import urllib.request
from io import StringIO
from datetime import datetime, timedelta, date

import requests
import pandas as pd


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
   
filename="DowJonesTickers.txt"
print('getting tickers from '+filename)
file=open(filename,"r")
total = 0 #track total number of tickers processed
alreadyUpToDate = [] #track how many files were already up to date
updated = [] #track how many files were updated
errored = [] #track which stocks were has errors
for ticker in file:
    ticker=ticker.strip('\n')
    outputfilename=ticker+'.csv'
    total = total+1
    try: #check if file exists
        df = pd.read_csv(ticker+'.csv')
        #update file if it exists
        #check if the df's latest date is today's date, otherwise update
        if df['Date'].tail(1).item()==date.today().__str__():
            #print('already up to date') #do nothing
            alreadyUpToDate.append(ticker)
        else:
            days_back = (date.today()-datetime.strptime(df['Date'].tail(1).item(),"%Y-%m-%d").date()).days
            df2 = YahooFinanceHistory(ticker, days_back=days_back).get_quote()
            df = df.append(df2)
            df.to_csv(path_or_buf=outputfilename)
            updated.append(ticker)
    except: #if file doesn't exist, make it
        try:
            df = YahooFinanceHistory(ticker, days_back=365*10).get_quote()
            df.to_csv(path_or_buf=outputfilename)
            updated.append(ticker)
        except (urllib.error.HTTPError,urllib.error.HTTPSConnectionPool) as err:
            print('HTTP error for '+ticker)
            print('Moving on to next ticker')
            errored.append(ticker)
#print download diagnostics
print(str(len(alreadyUpToDate))+' out of '+str(total)+' were already up-to-date')
print(str(len(updated))+' out of '+str(total)+' were updated')
if len(errored) > 0:
    print(str(errored)+' errored')
    