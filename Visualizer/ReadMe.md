# Visualizer
We need a single application to house, run, compare, and analysis the different models. A web app is a natural choice due to it's flexibility and availability but mostly we're choosing it because you can get sick css styling.

How to run web app. In terminal, change directors until you're in the stockadvisor folder. Run
```python
python manage.py runserver
```
Open a browser and go to either [localhost:8000/advisor](localhost:8000/advisor) or http://127.0.0.1:8000/advisor

## Current Project Structure
Django projects have a main web app manging level (stockadvisor folder) then plugable "apps". So far this project has the high level manging folder files. Apps to come!

## Construction Phases

#### *Phase 1*
Pick a web app library: [Django](https://www.djangoproject.com) looks promising and seems to be well documented. The intro [tutorial](https://docs.djangoproject.com/en/2.1/intro/tutorial01/) is LONG but doable.

#### *Phase 2*
Follow a Model-View-Controller design by deciding what the model will be (stock trading models/data/graphs/text), some basic view styles, and how we want to control the view (think interaction between view and model).
* **View**:
Based on the mockup. I'm thinking we'll need a 'home' screen view and an individual stock view.
* **Model**:
The model will need stock tickers, stock data, the models to process the data, and maybe more. We may need to talk more about how we want to represent all of that in terms of classes (i.e. what classes do we create for the model). Do we make stock classes and model classes (allowing less data query calls). Or just model classes that can take in a stock (but then everytime a stock is processed by a model, we have to requery for the stock data...)
* **Controller**:
In the 'home' view we want a search bar and clickable stocks on the left. How often do we want the controller to post sell, hold, buy, and model health values?
In the individual stock view we can use the bohek (or is it bokeh?) plotting to get clickable graphs that are zoomable (but may load in a different browser window... have to look into that).

#### *Phase 3*
Make wicked cool styling scheme.
