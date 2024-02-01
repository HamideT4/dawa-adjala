from django.contrib import admin
from .models import Account, Transaction, Operation, Notification

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Operation)
admin.site.register(Notification)
