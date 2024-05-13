from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('news_detail/<int:new_id>/', views.news_detail, name='news_detail')
]
