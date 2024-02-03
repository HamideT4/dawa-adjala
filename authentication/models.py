from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _ 
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):

    GENDER = (
        ('Female', 'Female'),
        ('Male', 'Male'),
     )
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(_("Email Adresse"), max_length=254, unique=True)
    adress = models.CharField(max_length=255)
    gender = models.CharField(choices=GENDER, max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined =  models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "adress"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    antecedent = models.CharField()
    medical_record = models.CharField(max_length=150)
    allergies = models.CharField(max_length=150)
    emergency_contact = models.CharField(max_length=150)
    emergency_number = models.CharField(max_length=150)

class Doctor(models.Model):

#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     adress = models.CharField(max_length=255)
#     gender = models.CharField(choices=GENDER, max_length=1)
#     birth_date = models.DateField()
#     avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    uid = models.CharField(max_length=150)
    specialty = models.CharField(unique=True)
    hospital_id = models.CharField(max_length=150)

    

# class Profile(models.Model):
#     GENDER = (
#         ('F', 'Female'),
#         ('M', 'Male'),
#     def __str__(self):
#         return self.adress

