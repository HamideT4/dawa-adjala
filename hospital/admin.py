from django.contrib import admin
from .models import Hospital, Service, Consultation

admin.site.register(Hospital)
admin.site.register(Service)
admin.site.register(Consultation)
