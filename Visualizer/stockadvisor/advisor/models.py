from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=200)
    ticker = models.CharField(max_length=20)
    sell_signal = models.DecimalField(default=0.00,max_digits=5,decimal_places=2)
    buy_signal = models.DecimalField(default=0.00,max_digits=5,decimal_places=2)
    hold_signal = models.DecimalField(default=0.00,max_digits=5,decimal_places=2)
    time_series_prices = models.FloatField(default=0.0)

class StockModel(models.Model):
    name = models.CharField(max_length=200)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    time_series_plot = models.FloatField(default=0.0)