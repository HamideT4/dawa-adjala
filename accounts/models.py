from django.db import models
from authentication.models import User
import uuid
import base64


def generate_account_uid():
    """
    Génère un code uid unique pour chaque compte.
    Returns:
        Le code uid pour le compte.
    """
    uid = uuid.uuid4()
    uid_bytes = uid.bytes
    uid_base64 = base64.b64encode(uid_bytes).decode('utf-8')
    uid_base64 = uid_base64.replace('/', '').replace('+', '')
    return 'DAD' + uid_base64[:8].upper()

class Account(models.Model):
    account_unique_identifier = models.CharField(max_length=255, unique=True, default=generate_account_uid, editable=False)
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
