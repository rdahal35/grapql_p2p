from django.contrib import admin

from .models import User, UserOTP, PropertyAddress, Buyer, Property, EnergySource, Payment, BillingAddress

admin.site.register(User)
admin.site.register(UserOTP)
admin.site.register(PropertyAddress)
admin.site.register(Buyer)
admin.site.register(Property)
admin.site.register(EnergySource)
admin.site.register(Payment)
admin.site.register(BillingAddress)
