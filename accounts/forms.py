from django import forms
from .models import Account, Transaction, Notification

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_unique_identifier', 'owner', 'balance']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['source_account', 'amount', 'date', 'description']

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['alert_type', 'account', 'date', 'status', 'content']
