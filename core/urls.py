import os
from dotenv import load_dotenv

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index

load_dotenv()

urlpatterns = [
    path(str (os.getenv ('ADMIN_URL')), admin.site.urls),
    path('', index, name='index'),
    path('auth/', include('authentication.urls')), # Authentication app URL
    path('hospital/', include('hospital.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
