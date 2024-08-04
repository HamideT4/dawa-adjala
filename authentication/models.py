from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _ 
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from hospital.models import Hospital
from django.template.loader import render_to_string
import uuid
import base64
from django.urls import reverse

class CustomUserManager(BaseUserManager):

    @staticmethod
    def email_validator(email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email"))
        
    def create_user(self, email, first_name, last_name, gender, birth_date, address, phone_number, avatar, password, **extra_fields):

        if not first_name:
            raise ValueError(_("Users must submit a first name"))
        
        if not last_name:
            raise ValueError(_("Users must submit a last name"))
        
        if not avatar:
            raise ValueError(_("You must provide an avatar"))
        
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Base User: and email address is required"))
        
        
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone_number=phone_number,
            birth_date=birth_date,
            gender=gender,
            **extra_fields
        )

        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user.save()

        return user
    
    def create_superuser(self, first_name, last_name, email, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superusers must have is_superuser=True"))
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superusers must have is_staff=True"))
        
        if not password:
            raise ValueError(_("Superusers must have a password"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Admin User: and email address is required"))
        
        gender = extra_fields.pop("gender", None)
        birth_date = extra_fields.pop("birth_date", None)
        address = extra_fields.pop("address", None)
        phone_number = extra_fields.pop("phone_number", None)
        avatar = extra_fields.pop("avatar", None)
        

        user = self.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        gender=gender,
        birth_date=birth_date,
        address=address,
        phone_number=phone_number,
        avatar=avatar,
        password=password,
        **extra_fields
    )
        user.save()   

        return user



class User(AbstractBaseUser, PermissionsMixin):

    GENDER = (
        ('Masculin', 'Masculin'),
        ('Feminin', 'Feminin'),
     )
    first_name = models.CharField(_("Nom"), max_length=100)
    last_name = models.CharField(_("Prenom"), max_length=100)
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    gender = models.CharField(_('Genre'), choices=GENDER, max_length=10)
    birth_date = models.DateField(_("Date de naissance"), null=True, blank=True)
    address = models.CharField(_('Adresse'), max_length=255)
    phone_number = models.CharField(_('Numero de téléphone'),max_length=20, null=True)
    avatar = models.ImageField(_('Photo'), upload_to='avatars/', default='avatars/avatar.png')
    qr_code = models.FileField(upload_to='qrcodes/', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    date_joined =  models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    
    REQUIRED_FIELDS = ["first_name", "last_name", "gender", "address", "phone_number", "birth_date", "avatar",]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.first_name
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    @property
    def get_full_name(self):
        return f"{self.first_name}".capitalize() + " " + f"{self.last_name}".capitalize()
    
    
    def get_absolute_url(self):
        return "/authentication/%i/" % (self.pk)
    
    
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
    account_unique_identifier = models.CharField(_("Numéro du compte"), max_length=255, unique=True, default=generate_account_uid, editable=False)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='account')
    balance = models.IntegerField(_("Solde"), default=0)

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

        coupon = Coupon.objects.create(recharge=self, amount=self.amount)

        context = {
            'amount': self.amount,
            'source_account': self.source_account,
            'owner': self.source_account.owner,
            'recharge_date': self.date,
        }
        html_content = render_to_string('coupon/index.html', context)
        coupon.html_content = html_content
        coupon.save()

class Rechargebook(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    html_content = models.TextField(blank=True)
    #pdf_file = models.FileField(upload_to='rechargebooks/', null=True, blank=True)

    def get_print_url(self):
        return reverse('print_rechargebook', args=[str(self.id)])
    
class Coupon(models.Model):
    recharge = models.OneToOneField(Recharge, on_delete=models.CASCADE)
    html_content = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_used = models.BooleanField(default=False)
    #owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupons')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Coupon de {self.amount} fcfa"
    

class Payment(models.Model):
    user = models.ForeignKey(User, related_name="source", on_delete=models.CASCADE)
    recipient = models.ForeignKey(Hospital, related_name="destination", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE, related_name='payment', blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} a payé {self.amount} fcfa à {self.recipient}" 

class Transfer(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transfers') 
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE, related_name='transfer')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfert de coupon #{self.coupon.id} de {self.sender} à {self.recipient}" 


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
