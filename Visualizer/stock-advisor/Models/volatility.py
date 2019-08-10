import numpy as np
import pandas as pd
from scipy import stats
from datetime import datetime


# Helper function to make sure df is formated as expected
# replaces spaces in column names with '_'
# turns dates into datetime objects
# sets Date to index
def format_df(df):
    df.columns = [col.replace(' ', '_') for col in df.columns]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index(df['Date'], drop=True)
    return df


class volatility:

    def __init__(self, df, min_window):
        self.df = format_df(df)
        self.min_periods = min_window

        # Import DOW data
        self.df_dow = pd.read_csv('Data/Data/^DJI.csv', index_col=[0])
        self.df_dow = format_df(self.df_dow)

    # Calculates difference in percent change of price--compared to DOW
    def calcVol(self):
        daily_close_px_dow = self.df_dow[['Adj_Close']]
        daily_close_px = self.df[['Adj_Close']]

        # Calculate the daily percentage change for `daily_close_px`
        daily_pct_change_dow = daily_close_px_dow.pct_change()
        daily_pct_change = daily_close_px.pct_change()

        # Calculate the volatility
        sqrt = np.sqrt(self.min_periods)
        vol_dow = daily_pct_change_dow.rolling(self.min_periods).std() * sqrt
        vol_ticker = daily_pct_change.rolling(self.min_periods).std() * sqrt

        # Calculates difference between DJI volatility and ticker
        # join dow and ticker only inlcuding ticker dates
        vol_diff = vol_ticker.join(vol_dow,
                                   how='inner', lsuffix='_tick', rsuffix='_dow')
        vol_diff.head()
        vol_diff['Dif'] = vol_diff['Adj_Close_tick'] - vol_diff['Adj_Close_dow']
        vol_diff['Ratio'] = vol_diff['Adj_Close_tick'] / vol_diff['Adj_Close_dow']
        self.vol_diff = vol_diff.dropna()

        # vol_diff['Dif'].hist()
        # vol_diff['Dif'].describe()

    def fitToF(self):
        # Fit a normal distribution to the data:
        mu, std = stats.norm.fit(data)

        # Plot the histogram.
        plt.hist(data, bins=30, density=True, alpha=0.6, color='g')

        # Plot the PDF.
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mu = %.4f,  std = %.4f" % (mu, std)
        plt.title(title)

        plt.show()

        # Bohek plot (interactie)
        output_notebook()
        p = figure(title=ticker + ' volatility comparison',
                   x_axis_type='datetime', y_axis_label='Volatility $')
        p.line(vol_diff.index.values, vol_diff['Ratio'],
               color='blue', legend='Volatility Ratio')

        p.legend.click_policy = "hide"
        show(p)

        vol_diff['Ratio'].hist()

        vol_diff['Ratio'].describe()

        # Fit histogram to f-distribution?
        data = vol_diff['Ratio'].dropna()

        # Fit a normal distribution to the data:
        df1, df2, loc, scale = stats.f.fit(data, 2, 1, loc=0, scale=1)

        # Plot the histogram.
        plt.hist(data, bins=20, density=True, alpha=0.6, color='g')

        # Plot the PDF.
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.f.pdf(x, df1, df2, loc, scale)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: loc = %.4f,  scale = %.4f" % (loc, scale)
        plt.title(title)

        plt.show()
