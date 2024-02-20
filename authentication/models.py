from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _ 
from .managers import CustomUserManager
from hospital.models import Hospital


class User(AbstractBaseUser, PermissionsMixin):

    GENDER = (
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
     )
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(_("Email Adresse"), max_length=254, unique=True)
    address = models.CharField(max_length=255)
    gender = models.CharField(choices=GENDER, max_length=10)
    phone_number = models.CharField(max_length=20, null=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined =  models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    
    REQUIRED_FIELDS = ["first_name", "last_name", "address"]

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name
    
    @property
    def get_full_name(self):
        return f"{self.first_name}".capitalize() + " " + f"{self.last_name}".capitalize()
    

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    antecedent = models.CharField()
    medical_record = models.CharField(max_length=150)
    allergies = models.CharField(max_length=150)
    emergency_contact = models.CharField(max_length=150)
    emergency_number = models.CharField(max_length=20)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.user.first_name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    matricule = models.CharField(max_length=150)
    speciality = models.CharField(max_length=150)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctors')
    service = models.CharField(max_length=254)
    is_root = models.BooleanField(default=False)
    is_approuved = models.BooleanField(default=False)

    def __str__(self):
        return 'Docteur' + ' ' + self.user.first_name
    

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    prescriptions = models.TextField()
    medical_observations = models.TextField()
    tests_result = models.TextField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return 'Consultation #' + str(self.id)
    
def get_absolute_url(self):
    return "/authentication/%i/" % (self.pk)
