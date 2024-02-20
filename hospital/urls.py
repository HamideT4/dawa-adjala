from django.urls import path
from .views import hospital_register

app_name = 'hospital'

urlpatterns = [
    path('register/', hospital_register, name='hospital_register'),
]
