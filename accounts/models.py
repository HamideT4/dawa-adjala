from django.db import models
from authentication.models import Patient, Profile

class Account(models.Model):
    account_unique_identifier = models.CharField(max_length=255, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    balance = models.IntegerField()
    min_balance = models.IntegerField()

    def __str__(self):
        return self.patient.user.firt_name    

class Transaction(models.Model):
    source_account = models.ForeignKey(Account, related_name='source_account', on_delete=models.CASCADE)
    destination_account = models.ForeignKey(Account, related_name='destination_account', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return 'Transaction #' + str(self.id)

class Operation(models.Model):
    initiator = models.CharField(max_length=255)
    amount = models.IntegerField()
    sender_phone = models.CharField(max_length=8)
    receiver_phone = models.CharField(max_length=8)
    description = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='operations')

    def __str__(self):
        return 'Operation #' + str(self.id)
    

class Notification(models.Model):
    alert_type = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
