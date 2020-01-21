from django.contrib import admin

from .models import Seller, SellerAddress, PaymentMethod, EnergyDetail

admin.site.register(Seller)
admin.site.register(SellerAddress)
admin.site.register(PaymentMethod)
admin.site.register(EnergyDetail)
