from django.shortcuts import render
from .models import Service

def index(request):
    service = Service.objects.all()
    context = {
        'service':service,
    }
    return render(request, 'index.html', context)