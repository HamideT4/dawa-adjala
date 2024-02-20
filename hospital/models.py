from django.db import models
import uuid
import base64

def generate_uid():
        """
        Génère un code matricule unique.
        Returns:
            Le code uid.
        """
        uid = uuid.uuid4()
        uid_bytes = uid.bytes
        uid_base64 = base64.b64encode(uid_bytes).decode('utf-8')
        uid_base64 = uid_base64.replace('/', '').replace('+', '')
        return uid_base64[:8].upper()

class Hospital(models.Model):
    uid = models.CharField(max_length=255, unique=True, default=generate_uid)
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    photo = models.ImageField(upload_to='hospital_photos/')
    is_approuved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.name

