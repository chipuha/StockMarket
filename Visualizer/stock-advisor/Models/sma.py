import datetime
import pandas as pd
import numpy as np

# Simple moving average analysis of stocks.
# Best for trending markets (not sidways/violate markets)
# The code comes from part of the tutorial form this website:
# https://www.datacamp.com/community/tutorials/finance-python-trading#tradingstrategy


class sma:

    def __init__(self, df):  # executed when an sma object in created
        self.df = df
        self.signals = pd.DataFrame(index=self.df.index)

    def viewDFhead(self, length=10):
        return self.df.head(length)

    def viewDFtail(self):
        return self.df.tail(length)

    # Creates moving average over small and long window.
    # Creates buy and sell signals based on small and long window crossings
    def createSMA(self, short_window, long_window):
        self.short_window = short_window
        self.long_window = long_window

        # Initialize the signals DataFrame
        self.signals['signal'] = 0.0

        # Create short simple moving average over the short window
        self.signals['short_mavg'] = self.df['Close'].rolling(
                window=short_window, min_periods=1, center=False).mean()
        self.signals['long_mavg'] = self.df['Close'].rolling(
                window=long_window, min_periods=1, center=False).mean()

        # Create signals
        self.signals['signal'][short_window:] = np.where(
                self.signals['short_mavg'][short_window:] > self.signals['long_mavg'][short_window:],
                1.0, 0.0)

        # Generate trading orders
        self.signals['positions'] = self.signals['signal'].diff()

    # Determine whether it's a buy or sell signal
    # If short_mavg goes above long_mavg, it's a buy
    # If short_mavg goes below long_mavg, it's a sell
    # The longer it's been since a signal compared to the time different the
    # window choice will decay the signal strength
    def getCurrentSignal(self):

        # extract last value -1 is sell, 1 is buy
        try:
            sig = self.signals['positions'].nonzero()[0]
            sig = self.signals['positions'].iloc[sig]
            last_signal = sig.tail(1).item()
            if last_signal == -1:
                return 'sell'
            elif last_signal == 1:
                return 'buy'
        except:
            return 'none'
