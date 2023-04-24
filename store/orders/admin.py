from django.contrib import admin

from .models import Order, Token, Warehouse, Store

admin.site.register(Order)
admin.site.register(Token)
admin.site.register(Warehouse)
admin.site.register(Store)
