from django.db import models
from authentication.models import User
from hospital.models import generate_uid

class Account(models.Model):
    account_unique_identifier = models.CharField(max_length=255, unique=True, default=generate_uid)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"Compte #{self.account_unique_identifier}"   

class Transaction(models.Model):
    source_account = models.ForeignKey(Account, related_name='source_account', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Transaction #{self.id}"

    # Override the default save method
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_account_balances() # Update balances amount

    def update_account_balances(self):
        source_account = self.source_account
        amount = self.amount

        source_account.balance += amount # add the amount from the source account to the balance
        source_account.save() # Save changes

class Notification(models.Model):
    ALERT_CHOICES = (
        ('Recharge', 'Nouvelle recharge'),
        ('Partenariat', 'Nouveau partenaire')
    )
    alert_type = models.CharField(max_length=255, choices=ALERT_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField(default='None')

    def __str__(self):
        return self.alert_type
