from django.db import models
from authentication.models import Doctor, Patient

class Hospital(models.Model):
    uid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    photo = models.ImageField(upload_to='hospital_photos/')

    def __str(self):
        return self.name + '-' + self.uid

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='services')

    def __str(self):
        return self.name

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    prescriptions = models.TextField()
    medical_observations = models.TextField()
    tests_result = models.TextField()
    comment = models.TextField(blank=True)
