from django.contrib import admin
from .models import Profile, Doctor, Patient

admin.site.register(Profile)
admin.site.register(Doctor)
admin.site.register(Patient)