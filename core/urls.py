import os
from dotenv import load_dotenv

from django.contrib import admin
from django.urls import path, include

load_dotenv()

urlpatterns = [
    path(str (os.getenv ('ADMIN_URL')), admin.site.urls),
    path('auth/', include('authentication.urls')), # Authentication app URL
]
