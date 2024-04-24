from django.contrib import admin
from .models import Account, Recharge,Notification, Rechargebook

admin.site.register(Account)
admin.site.register(Recharge)
admin.site.register(Notification)
admin.site.register(Rechargebook)
