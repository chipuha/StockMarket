from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=200)
    ticker = models.CharField(max_length=20)
    sell_signal = models.DecimalField(default=0.00,max_digits=5,decimal_places=2) #overall signal
    buy_signal = models.DecimalField(default=0.00,max_digits=5,decimal_places=2) #overall signal
    hold_signal = models.DecimalField(default=0.00,max_digits=5,decimal_places=2) #overall signal
    #time_series_prices = models.FloatField(default=0.0)

class StockModel(models.Model):
    name = models.CharField(max_length=200)
    health = models.CharField(max_length=200,default="red")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE) #what stock is this model associated with
    sell_signal = models.DecimalField(default=0.00,max_digits=5,decimal_places=2) #signal form one model
    buy_signal = models.DecimalField(default=0.00,max_digits=5,decimal_places=2) #signal form one model
    hold_signal = models.DecimalField(default=0.00,max_digits=5,decimal_places=2) #signal form one model

class TimeSeries(models.Model):
    name = models.CharField(max_length=200)
    #stockmodel = models.ForeignKey(StockModel, blank=True, on_delete=models.CASCADE) #what stock is the data associated with
    #stock = models.ForeignKey(Stock, blank=True, on_delete=models.CASCADE) #what stock is the data associated with
    #time_series_data = models.FloatField(default=0.0) #CHANGE THIS TO A LIST OF FLOATS, NOT JUST ONE FLOAT