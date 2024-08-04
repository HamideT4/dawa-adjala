from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import  Hospital, HospitalAccount


@receiver(post_save, sender=Hospital)
def create_hospital_account(sender, instance, created, **kwargs):
    if created:
        HospitalAccount.objects.create(owner=instance)
