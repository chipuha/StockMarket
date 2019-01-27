import io
import csv
import requests
import pandas as pd
import datetime

#get data for stock models using github project files
class gitHubData:
    def __init__ (self):
        #get tickers of interest from github repository
        self.ticker_url = "https://raw.githubusercontent.com/chipuha/StockMarket/master/Data/DowJonesTickers.txt"
        self.tickers = pd.read_csv(self.ticker_url)
        self.dataBaseUrl = "https://raw.githubusercontent.com/chipuha/StockMarket/master/Data/data/"
    
    #Returns data frame of values for specified ticker within specified range (INCLUSIVE)
    #ticker needs to be a string and in github list
    #startDate and endDate need to be datetime.datetime() objects
    def getData(self,ticker,startDate,endDate):
        self.ticker = ticker
        self.start = startDate
        self.end = endDate
        if self.start >= self.end:
            raise ValueError("\n----- Error -----\nStart date cannot be the same as or later than end date.")
        if not(self.ticker in self.tickers.values):
            raise ValueError("\n----- Error -----\n"+self.ticker+" is not in database.\nAdd ticker to database.")
        else:
            self.df = pd.read_csv(self.dataBaseUrl+self.ticker+".csv")
            try:
                #convert datatime.datetimes to strings to compare with dataframe dates which are strings
                self.start = self.start.strftime("%Y-%m-%d")
                self.end = self.end.strftime("%Y-%m-%d")

                #check github database contains desired ranges
                if self.df[self.df['Date'] <= self.start].empty:
                    raise ValueError("\n----- Error -----\nStart date is too early. Consider updating database.")
                if self.df[self.df['Date'] >= self.end].empty:
                    raise ValueError("\n----- Error -----\nEnd date is too recent. Database has not yet updated.")
                
                #new dataframe will INCLUDE the start and end dates
                self.df = self.df[self.df['Date'] >= self.start]
                self.df = self.df[self.df['Date'] <= self.end]
                return self.df
            except ValueError as e:
                raise

    
    def getTickerList(self):
        return self.tickers
    
    def getAvailableDateRange(self,ticker):
        self.ticker = ticker
        
        if not(self.ticker in self.tickers.values):
            raise ValueError("\n----- Error -----\n"+self.ticker+" is not in database.\nAdd ticker to database.")
        else:
            self.df = pd.read_csv(self.dataBaseUrl+self.ticker+".csv")
            first = self.df['Date'].values[0]
            last = self.df['Date'].values[-1]
            return [first, last] #first and last should be strings