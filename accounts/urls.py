from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    #path('user-dashboard/', login_required(views.user_dashbord), name='user_dashboad'),
    
]
