from django.db import models
from authentication.models import User
from hospital.models import Hospital

import uuid
import base64
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.conf import settings
from weasyprint import HTML
import imgkit

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
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='account')
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"Compte de {self.owner.get_full_name}"

    def get_account_unique_identifier(self):
        return self.account_unique_identifier

    def get_balance(self):
        return self.balance

class Recharge(models.Model):
    source_account = models.ForeignKey(Account, related_name='source_account', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Recharge #{self.id}"

    # Override the default save method
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_account_balances() # Update balances amount
        self.generate_coupon()

    def update_account_balances(self):
        source_account = self.source_account
        amount = self.amount

        source_account.balance += amount # add the amount from the source account to the balance
        source_account.save() # Save changes

    def generate_coupon(self):
        # Customize pdf generaion logic

        coupon = Coupon.objects.create(recharge=self)

        context = {
            'amount': self.amount,
            'source_account': self.source_account,
            'owner': self.source_account.owner,
        }
        html_content = render_to_string('coupon/index.html', context)
       
        image_content = imgkit.from_string(html_content, False, {'format': 'png', 'enable-local-file-access': None })
        image_file = ContentFile(image_content)
        image_file.name = f'{self.source_account.owner.first_name}coupon.png'

        coupon.coupon.save(image_file.name, image_file, save=True) 

        #pdf_content = HTML(string=html_content).write_pdf()

        #coupon.coupon.save(f'{self.source_account.owner.first_name}_coupon.pdf', ContentFile(pdf_content), save=True)

# class Payment(models.Model):
#     source_account = models.ForeignKey(Account, related_name="source_account", on_delete=models.CASCADE)
#     destination_account = models.ForeignKey(Hospital, related_name="destination_account", on_delete=models.CASCADE)
#     amount = models.IntegerField()
#     date = models.DateField(auto_now_add=True)
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return f"Paiement #{self.id}"
    
#     # Override the default save method
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.update_account_balance() # Update balances amount

#     def update_account_balance(self):
#         source_account = self.source_account
#         destination_account = self.destination_account
#         amount = self.amount

#         source_account.balance -= amount 

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

class Rechargebook(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    html_content = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='rechargebooks/', null=True, blank=True)

class Coupon(models.Model):
    recharge = models.OneToOneField(Recharge, on_delete=models.CASCADE)
    coupon = models.FileField(upload_to='coupons/')
    is_used = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


    