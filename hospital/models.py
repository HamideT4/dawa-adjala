from django.db import models
import uuid
import base64

def generate_hospital_uid():
        """
        Génère un code matricule unique.
        Returns:
            Le code uid pour l'hôpital.
        """
        uid = uuid.uuid4()
        uid_bytes = uid.bytes
        uid_base64 = base64.b64encode(uid_bytes).decode('utf-8')
        uid_base64 = uid_base64.replace('/', '').replace('+', '')
        return 'DADH' + uid_base64[:8].upper()

class Hospital(models.Model):
    uid = models.CharField(max_length=255, unique=True, default=generate_hospital_uid, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    photo = models.ImageField(upload_to='hospital_photos/')
    is_approuved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
