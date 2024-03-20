from django.shortcuts import render
from .models import Service, Team

def index(request):
    service = Service.objects.all()
    context = {
        'service':service,
    }
    return render(request, 'index.html', context)

def about(request):
    team = Team.objects.all()
    context = {
        'team':team,
    }
    return render(request, 'about.html', context)
