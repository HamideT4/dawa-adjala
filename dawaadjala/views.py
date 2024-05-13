from django.shortcuts import render
from .models import Service, Team, New
from authentication.models import User
from hospital.models import Hospital

def index(request):
    service = Service.objects.all()
    team = Team.objects.order_by('id')[:3]
    news = New.objects.all()
    total_users = User.objects.count()
    approved_hospitals = Hospital.objects.filter(is_approuved=True).count()

    context = {
        'service':service,
        'team':team,
        'news':news,
        'total_users':total_users,
        'approved_hospitals':approved_hospitals,
    }
    return render(request, 'index.html', context)

def about(request):
    team = Team.objects.all()
    context = {
        'team':team,
    }
    return render(request, 'about.html', context)

def news_detail(request, new_id):
    news = New.objects.get(pk=new_id)
    all = New.objects.all()
    first_image = news.image.all().first()
    last_two_images = news.image.all().order_by('-id')[:2]

    context = {
        'all':all,
        'news':news,
        'first_image': first_image,
        'last_two_images': last_two_images,
    }
    return render(request, 'news.html', context)
