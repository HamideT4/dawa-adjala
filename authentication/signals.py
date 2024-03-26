from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import User
from accounts.models import Account, generate_account_uid

# The @receiver decorator connects the create_account function to the post_save
# signal of the User model

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created: # if the user is newly created (created == True)
        # Create a new account:
        account = Account.objects.create(owner=instance)

        # Envoi de notification par e-mail
        subject = 'Bienvenue sur Dawa Adjala !'
        message = render_to_string('registration/welcome_email_template.html', {'user': instance})
        recipient_list = [instance.email]
        send_mail(subject, message, settings.EMAIL_HOST, recipient_list)