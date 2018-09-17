# StockMarket
Many models can be used to make predictions instead of one "golden" or "magic" model. This notebook includes code for multiple models--each with different strengths and weaknesses:

### Simple Moving Average

* What an SMA tells you: trends but does not predict future prices.
* Strength: This confirms past trends.
* Weakness: Does not predict future. Sensitive to the time you average over.
* Inputs: Stock prices over time
* Output: 
* Steps needed: 
* Questions to consider: 
* Possible improvements:

### Insider Trading

* What an IT tells you: We assume insiders buy and sell to make profits, they have within 6 month vision of whether the company's stock will go up or down, and they are ok with breaking insider trading laws
* Strength: Probably more insightful then media news since insiders know more
* Weakness: Strong insider trading is useful; low or weak trading doesn't tell us anything. Insiders may sell or buy to help keep stock price stable
* Possible improvements:

### Linear Fit On Price

* What an LFP tells you: linear trends over long term but does not predict future prices
* Strength: Many larger companies with less volitate stock prices seems to fit to lines quite well. This confirms past trends.
* Weakness:
* Inputs
* Outputs
* Steps needed:
* Questions to consider:
* Possible improvements:

### Volatility Measure

* What an VM tells you: has to stock price been volitate recently. We assume it will continue in the trend though it does not explicity predict that
* Strength: measures volatility. This could be a good measure to weight all other models by. High volatility would mean the price will change soon and thus, look at your other models to see if that change will be up or down.
* Weakness: Does not predict future.
* Inputs
* Outputs
* Steps needed:
* Questions to consider:
* Possible improvements:

### Twitter Sentiment

* What an TS tells you: what twitter is saying about a stock
* Strength: Detects hype and sentiment toward a particular stock. Hype is often a good indicator of large, near-future or immediate price changes
* Weakness: could be missing keywords, or interpreting keywords incorrectly due to some missed context like "*not* good."
* Inputs
* Outputs
* Steps needed:
* Questions to consider:
* Possible improvements: include other social media platforms and news websites

### Bull Vs Bear Market

* What BvB tells you: Periods of gradual rising vs periods of falling prices and volatility
* Strength: Provides a general long-term market trend 
* Weakness: Very general, long-term trend. Not stock specific.
* Inputs
* Outputs
* Steps needed:
* Questions to consider:
* Possible improvements: 

### Machine Learning Model(s):

* What MLM tells you: Predicts price
* Strength: Includes all sort of inputs and nonlinearly predicts future price
* Weakness: Stock market has historically been very difficult to predict
* Inputs: Historical price, employment stats,...
* Outputs: predicted price, model health
* Steps needed: gather and process data, run data through model, output prediction and model health
* Questions to consider:
* Possible improvements:

### The Trunk:

* What the trunk tells you: categorizes stocks into buy, hold, or sell
* Strengths: summarizes and uses all available models to decided if a stock is a hold, buy, or sell, is expandable with new models
* Weakness: categories are simple and don't predict yields
* Inputs: All other models and information gathered
* Outputs: Simple sell, hold, or buy
* Steps needed:
* Questions to consider:
* Possible improvements: Predicting yields

### The Recorder

* What the recorder tells you: How the model is doing, are you making more money than a savings account, etc?
* Strengths: Helps to know if something needs to be reworked, if we're on the right path
* Weaknesses: Based on our bias and if we act on the model's recommendations or not
* Inputs: buy and sell data and model outputs
* Outputs: % yeild
* Steps needed: Easy way to record buy/sell data
* Questions to consider:
* Possible improvements:


# Project Outline
### *Phase 1*
1. Add each model to repo as objects in their own folders/files
2. Add master file that accesses each model for a specific Dow Jones ticker (start with ~30 Dow Jones stocks)

### *Phase 2*
1. Add automation abilities (to be determined)

### *Phase 3*
1. Make money

### *Phase 4*
1. Pay for annual dirt biking tours with stock profits

### *Phase 5*
1. Consider including divedends into analysis (weighted portfolio between trading and holding dividend earning entities (CDs, stocks, etc.)?)
