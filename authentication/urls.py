from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views
from .views import UserView, CustomLoginView

app_name = 'authentication'

urlpatterns = [
<<<<<<<<< Temporary merge branch 1
    path('', include('allauth.urls')),
=========
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/<int:pk>/', login_required(UserView.as_view()), name='profile'),
    path('signup/', views.signup, name='signup'),
    path('user-dashboard/', login_required(views.user_dashbord), name='user_dashboad'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
