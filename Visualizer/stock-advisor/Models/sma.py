# coding: utf-8

# # Simple Moving Average
# 
# Object implimentation is at the beginning, examples follow.


#Import lots of stuff
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as pdr

#trying new plotting library
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook


# ## The simple moving average object
# Simple moving average analysis of stocks. Best for trending markets (not sidways/violate markets)
# 
# This is a Simple Moving Crossover Trading Strategy (Momentum class of strategies)
# The code comes from part of the tutorial form this website:
# https://www.datacamp.com/community/tutorials/finance-python-trading#tradingstrategy
# 

class sma:
    
    def __init__(self, ticker, df): #executed when an sma object in created
        self.ticker = ticker   #must be all caps string (e.g. "MSFT")
        self.df = df
        self.signals = pd.DataFrame(index=self.df.index)
        
    def viewDFhead(self, length=10):
        return self.df.head(length)
        
    def viewDFtail(self):
        return self.df.tail(length)
    
    #Plots the Closing price vs. Datetime in matplotlib and bokeh
    def plotDF(self):
        #iteractive bokeh plot
        #output_notebook() #puts plot inside notebook instead of making it in a new browser tab
        p = figure(title=self.ticker,x_axis_type='datetime',y_axis_label='Price $')
        p.line(self.df.index.values,self.df['Close'])
        show(p)
        
        #matplotlib version (not interactive)
        self.df['Close'].plot(grid=True,figsize=(12,8))
        plt.title(ticker)
        plt.ylabel('Price $')
        plt.show()
        
    #Creates moving average over small and long window.
    #Creates buy and sell signals based on whether small and long windows cross
    def createSMA(self, short_window, long_window): #Calculate SMA for given window_sizes
        self.short_window = short_window
        self.long_window = long_window
        
        # Initialize the signals DataFrame
        self.signals['signal'] = 0.0

        # Create short simple moving average over the short window
        self.signals['short_mavg'] = self.df['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
        self.signals['long_mavg'] = self.df['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
        
        # Create signals
        self.signals['signal'][short_window:] = np.where(self.signals['short_mavg'][short_window:] > self.signals['long_mavg'][short_window:], 1.0, 0.0)   

        # Generate trading orders
        self.signals['positions'] = self.signals['signal'].diff()

    #Plots the Closing price vs. Datetime of the stock, short moving average, and long moving average
    #Plots are done in matplotlib and bokeh
    def plotSMA(self): #plot price with SMA short and long windows. For now, buy sell signals are not included
        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='Price in $')
        self.df['Close'].plot(ax=ax1, color='r', lw=2.)
        self.signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

        ##(needs work: double showing sell and buy signals)
        # Plot the buy signals
        ax1.plot(self.signals.loc[self.signals.positions == 1.0].index.values,
                 self.signals.loc[self.signals.positions == 1.0]['short_mavg'],
                 "^", markersize=10, color="c")
         
        # Plot the sell signals
        ax1.plot(self.signals.loc[self.signals.positions == -1.0].index.values,
                 self.signals.loc[self.signals.positions == -1.0]['short_mavg'],
                 "v", markersize=10, color="k")
        plt.show()
        
        # Bohek plot (interactive)
        #output_notebook() #puts plot inside notebook instead of making it in a new browser tab
        p = figure(title=self.ticker,x_axis_type='datetime',y_axis_label='Price $')
        p.line(self.df.index.values,self.df['Close'],color = 'red',legend='Close')
        p.line(self.df.index.values,self.signals['short_mavg'], color='green',legend=str(self.short_window))
        p.line(self.df.index.values,self.signals['long_mavg'], color='blue',legend=str(self.long_window))
        p.legend.click_policy="hide"

        ##(need to figure out how to add the buy and sell signals)
        #p.circle(signals.loc[signals.positions == 1.0].index,
        #         signals.loc[signals.positions == 1.0],size=30, color="green", alpha=0.5)
        #p.circle(signals.loc[signals.positions == -1.0].index,
        #         signals.loc[signals.positions == -1.0],size=30, color="red", alpha=0.5)
        show(p)
    
    #Tracks capital change if you were to follow this strategy
    #Initial_capital is how much money you start with.
    #Interally, 10 stocks will be sold or bought at a time. This can be changed
    def createBackTest(self, initial_capital):
        # Set the initial capital
        initial_capital= float(initial_capital)

        # Create a DataFrame `positions`
        positions = pd.DataFrame(index=self.signals.index).fillna(0.0)

        # Buy a 10 shares at a time
        positions[ticker] = 10*self.signals['signal']   
  
        # Initialize the portfolio with value owned   
        self.portfolio = positions.multiply(self.df['AdjClose'], axis=0)

        # Store the difference in shares owned 
        pos_diff = positions.diff()

        # Add `holdings` to portfolio
        self.portfolio['holdings'] = (positions.multiply(self.df['Close'], axis=0)).sum(axis=1)
        # Add `cash` to portfolio
        self.portfolio['cash'] = initial_capital - (pos_diff.multiply(self.df['Close'], axis=0)).sum(axis=1).cumsum()   
        # Add `total` to portfolio
        self.portfolio['total'] = self.portfolio['cash'] + self.portfolio['holdings']
        # Add `returns` to portfolio
        self.portfolio['returns'] = self.portfolio['total'].pct_change()

        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')
        self.portfolio['total'].plot(ax=ax1, lw=2.)
        # Plot the "buy" trades against the equity curve
        #ax1.plot(self.portfolio.loc[signals.(self.positions) == 1.0].index, 
        #         self.portfolio.total[signals.(self.positions) == 1.0],
        #        '^', markersize=10, color='m')
        # Plot the "sell" trades against the equity curve
        #ax1.plot(self.portfolio.loc[signals.(self.positions) == -1.0].index, 
        #         self.portfolio.total[signals.(self.positions) == -1.0],
        #         'v', markersize=10, color='k')
        plt.show()
        
        # Bohek plot (interactive)
        #output_notebook() #puts plot inside notebook instead of making it in a new browser tab
        p = figure(title=self.ticker, x_axis_type='datetime', y_axis_label='Price $')
        p.line(self.df.index.values, self.portfolio['total'], color='red', legend='Total Profit $')
        p.legend.click_policy="hide"
        ##(need to figure out how to add the buy and sell signals)
        #p.circle(signals.loc[signals.positions == 1.0].index,
        #         signals.loc[signals.positions == 1.0],size=30, color="green", alpha=0.5)
        #p.circle(signals.loc[signals.positions == -1.0].index,
        #         signals.loc[signals.positions == -1.0],size=30, color="red", alpha=0.5)
        show(p)
    
    #Calculates and prints Sharpe Ratio
    #Calculates and plots maximum and daily drawdown in matplotlib and bokeh
    def evaluation(self):
        returns = self.portfolio['returns']

        # annualized Sharpe ratio
        sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())

        # Print the Sharpe ratio
        print("Sharpe ratio:", sharpe_ratio)

        # Define a trailing 252 trading day window
        window = 252

        # Calculate the max drawdown in the past window days for each day
        rolling_max = self.df['Close'].rolling(window, min_periods=1).max()
        daily_drawdown = self.df['Close']/rolling_max - 1.0

        # Calculate the minimum (negative) daily drawdown
        max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()

        # Plot the results
        daily_drawdown.plot()
        max_daily_drawdown.plot()
        plt.show()
        
        #output_notebook() #puts plot inside notebook instead of making it in a new browser tab
        p = figure(title=self.ticker, x_axis_type='datetime', y_axis_label='Price $')
        p.line(self.df.index.values, daily_drawdown, color='red', legend='daily drawdown')
        p.line(self.df.index.values, max_daily_drawdown, color='blue', legend='max daily drawdown')
        p.legend.click_policy="hide"
        show(p)

        #Compound Annual Growth Rate
        days = (self.df.index[-1] - self.df.index[0]).days
        cagr = ((((self.df['Close'][-1]) / self.df['Close'][1])) ** (365.0/days)) - 1
        print("Compound Annual Growth Rate:",cagr)
'''
ticker = 'MSFT'
start = datetime.datetime(2017, 6, 19)
end = datetime.datetime(2018, 6, 1)
sma1 = sma(ticker, start, end)
sma1.viewDFhead()
#sma1.plotDF() #redirects to new page
short_window = 52
long_window = 104
sma1.createSMA(short_window,long_window)
sma1.plotSMA()

sma1.createBackTest(1000) #start with $1000

# ### Evaluating strategy
# 1. Sharpe Ratio:
# 1 is ok, 2 is very good and 3 is excellent. (according to tutorial)
# 2. Maximum Drawdown:
# measure of the largest single drop from peak to bottom
# 3. Compound Annual Growth Rate (CAGR): What you actual made over the time period as if a constant rate

sma1.evaluation()'''