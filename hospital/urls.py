from django.urls import path
from .views import hospital_register, hospital_detail

app_name = 'hospital'

urlpatterns = [
    path('register/', hospital_register, name='hospital_register'),
    path('hospital-partners/', hospital_detail, name='hospital_detail')
]
