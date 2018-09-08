### StockMarket
Many models can be used to make predictions instead of one "golden" or "magic" model. This notebook includes code for multiple models--each with different strengths and weaknesses:

# Simple Moving Average

* What an SMA tells you: trends but does not predict future prices.
* Strength: This confirms past trends.
* Weakness: Does not predict future. Sensitive to the time you average over.
* Possible improvements:

# Insider Trading

* What an IT tells you: We assume insiders buy and sell to make profits, they have within 6 month vision of whether the company's stock will go up or down, and they are ok with breaking insider trading laws
* Strength: Probably more insightful then media news since insiders know more
* Weakness: Strong insider trading is useful; low or weak trading doesn't tell us anything. Insiders may sell or buy to help keep stock price stable
* Possible improvements:

# Linear Fit On Price

* What an LFP tells you: linear trends over long term but does not predict future prices
* Strength: Many larger companies with less volitate stock prices seems to fit to lines quite well. This confirms past trends.
* Weakness:
* Possible improvements:

# Volatility Measure

* What an VM tells you: has to stock price been volitate recently. We assume it will continue in the trend though it does not explicity predict that
* Strength: measures volatility. This could be a good measure to weight all other models by. High volatility would mean the price will change soon and thus, look at your other models to see if that change will be up or down.
* Weakness: Does not predict future.
* Possible improvements:

# Twitter Sentiment

* What an TS tells you: what does the news say about the stock
* Strength:
* Weakness: could be missing keywords, or interpreting keywords incorrectly due to some context like "not good."
* Possible improvements: include other social media platforms

# Bull Vs Bear Market

* What BvB tells you: Periods of gradual rising vs periods of falling prices and volatility
* Strength: Provides a general long-term market trend 
* Weakness: Very general, long-term trend. Not stock specific.
* Possible improvements: 
