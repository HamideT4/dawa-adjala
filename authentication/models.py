from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adress = models.CharField(max_length=255)
    gender = models.CharField(choices=GENDER, max_length=1)
    birth_date = models.DateField()
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.adress
