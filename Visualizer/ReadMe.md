# Visualizer
We need a single application to house, run, compare, and analysis the different models. A web app is a natural choice due to it's flexibility and availability but mostly we're choosing it because you can get sick css styling.

How to run web app. In terminal, change directors until you're in the stockadvisor folder. Run
```python
python manage.py runserver
```
Open a browser and go to either localhost:8000/advisor or http://127.0.0.1:8000/advisor

To open the admin settings and explore the database/edit database manually, run
```python
python manage.py runserver
```
 Then go to http://127.0.0.1:8000/admin. Sign in with username: rasmusson and password: stockadvisor

## Current Project Status
Django projects have a main web app manging level (stockadvisor folder) then plugable "apps". So far this project has the high level manging folder files. Main (and only) app is advisor app. The app uses a template view that is passed in a ticker symbol which is displays on the second header of the page.

* **View**:
Home (index) view mostly complete. Need to finish styling and moving the search bar

* **Model**:
This model setup has stocks as the primary class. For example, if there are 5 stocks and 4 types of models, there will be 5 stock instances and 20 stock model instances. Not sure the best way to save dataframes of data into database...

Class Stock Models: name, the stock's ticker the model is associated with, buy signal, sell signal, hold signal
Class Stock: name, ticker, sell signal, buy signal, hold signal, time series-data
Class TimeSeries: name (label like price, close, etc.), stock it's associated with, data float values

* **Controller**:
Buy, sell, and model health button will take you to their respective sections of the webpage.

## Construction Phases

#### *Phase 1*
Pick a web app library: [Django](https://www.djangoproject.com) looks promising and seems to be well documented. The intro [tutorial](https://docs.djangoproject.com/en/2.1/intro/tutorial01/) is LONG but doable.

#### *Phase 2*
Follow a Model-View-Controller design by deciding what the model will be (stock trading models/data/graphs/text), some basic view styles, and how we want to control the view (think interaction between view and model).
* **View**:
Based on the mockup. I'm thinking we'll need a 'home' view and an individual stock view.
* **Model**:
The model will need stock tickers, stock data, the models to process the data, and maybe more. We may need to talk more about how we want to represent all of that in terms of classes (i.e. what classes do we create for the model). Do we make stock classes and model classes (allowing less data query calls). Or just model classes that can take in a stock (but then everytime a stock is processed by a model, we have to requery for the stock data...).
Possible model setup: Stock class holding ticker, price and other data, and signal (buy,hold,sell). Model class accesses and talks to stock model scripts to determine over all buy hold or sell; also flexible enough to display individual model results. Model Evaluation class evaulates (back tests) models over historical periods and evaulations how combinations of models work together.
* **Controller**:
In the 'home' view we want a search bar and clickable stocks on the left. How often do we want the controller to post sell, hold, buy, and model health values?
In the individual stock view we can use the bohek (or is it bokeh?) plotting to get clickable graphs that are zoomable (but may load in a different browser window... have to look into that).

#### *Phase 3*
Make wicked cool styling scheme.
