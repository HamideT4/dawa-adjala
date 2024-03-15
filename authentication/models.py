from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _ 
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):

    GENDER = (
        ('Masculin', 'Masculin'),
        ('Feminin', 'Feminin'),
     )
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(_("Email Adresse"), max_length=254, unique=True)
    gender = models.CharField(choices=GENDER, max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined =  models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    
    REQUIRED_FIELDS = ["first_name", "last_name", "gender", "address", "phone_number"]

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name
    
    @property
    def get_full_name(self):
        return f"{self.first_name}".capitalize() + " " + f"{self.last_name}".capitalize()
    
def get_absolute_url(self):
    return "/authentication/%i/" % (self.pk)
