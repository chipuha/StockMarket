# Long Short-Term Memory
This is a type of recurrent neural network (RNN) designed to keep a memory of sequential data, making it a good choice for time series machine learning. See [wikipedia](https://en.wikipedia.org/wiki/Long_short-term_memory).
The code came form this [tutorial](https://www.datacamp.com/community/tutorials/lstm-python-stock-market) posted to [Github](https://github.com/thushv89/datacamp_tutorials/tree/master/Reviewed).

* What an LSTM tells you: predicts future prices based on sequential data. For now, we choose the sequential data to be previous old prices.
* Strength: LSTM’s are made to take in sequential data and make predictions, though we will need to play with it to determine how to get the most range out of the model.
* Weakness: May have problems predicting more than 30 days into the future.
* Inputs: Stock prices over time
* Output: Future stock prices
* Steps needed:
* Questions to consider:
* Possible improvements: