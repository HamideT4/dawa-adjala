from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import User
from accounts.models import Account, Rechargebook
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
import weasyprint, imgkit
from django.core.files.storage import default_storage

# The @receiver decorator connects the create_account function to the post_save
# signal of the User model

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created: # if the user is newly created (created == True)
        # Create a new account:
        account = Account.objects.create(owner=instance)

        # Récupérer le numéro de compte de l'utilisateur nouvellement créé
        account_number = account.account_unique_identifier

        # Solde initial du compte nouvellement créé (par défaut 0)
        balance = account.balance

        # Generate QRCode data
        qr_data = f"Nom: {instance.get_full_name}\n"
        qr_data += f"Genre: {instance.gender}\n"
        qr_data += f"Email: {instance.email}\n"
        qr_data += f"Numéro de compte: {account.account_unique_identifier}\n"

        # Generate QRCode
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_code.add_data(qr_data)
        qr_code.make(fit=True)
        qr_code_img = qr_code.make_image(fill_color="black", back_color="white")

        # Convert the QRCode image to bytes
        qr_code_bytes = BytesIO()
        qr_code_img.save(qr_code_bytes, format='PNG')
        qr_code_bytes.seek(0)

        # Save the QRCode image to the user's qr_code field
        instance.qr_code.save(f'{instance.first_name}_qrcode.png', ContentFile(qr_code_bytes.read()), save=True)

        # # Create a new rechargebook for the user
        rechargebook = Rechargebook.objects.create(owner=instance)

        # # Generate rechargebook's html content using templates
        context = {
            'owner': instance,
            'account_number': account_number,
            'balance': balance,
        }
        html_content = render_to_string('rechargebook/index.html', context)

        # Save the html content in rechargebook model
        rechargebook.html_content = html_content
        rechargebook.save()

        # # Convert html content to pdf
        # pdf_content = weasyprint.HTML(string=html_content).write_pdf(stylesheets=[weasyprint.CSS(string='@page { size: landscape; }')])

        # # Save the pdf in rechargebook model
        # rechargebook.pdf_file.save(f'{instance.first_name}_livret_de_paiement.pdf', ContentFile(pdf_content), save=True)

        # Envoi de notification par e-mail
        subject = 'Bienvenue sur Dawa Adjala !'
        message = render_to_string('registration/welcome_email_template.html', {'user': instance})
        recipient_list = [instance.email]
        send_mail(subject, message, settings.EMAIL_HOST, recipient_list)