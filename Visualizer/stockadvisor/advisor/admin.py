from django.contrib import admin

from .models import Stock, StockModel

admin.site.register(Stock)
admin.site.register(StockModel)