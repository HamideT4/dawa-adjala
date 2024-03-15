import os
from dotenv import load_dotenv

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

load_dotenv()

urlpatterns = [
    path(str (os.getenv ('ADMIN_URL')), admin.site.urls),
    path('', include('dawaadjala.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('auth/', include('authentication.urls')), 
    path('hospital/', include('hospital.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
