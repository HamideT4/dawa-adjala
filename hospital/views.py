from django.shortcuts import render, redirect
from .forms import HospitalRegisterForm
from .models import Hospital

def hospital_register(request):
    if request.method == 'POST':
        form = HospitalRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.is_approuved = False
            hospital.save()
            return redirect('/')
    else:
        form = HospitalRegisterForm()
    return render(request, 'hospital/register.html', {'form': form})

def hospital_detail(request):

    hospital = Hospital.objects.all()

    context = {
        'hospital': hospital,
    }

    return render(request, 'hospital/detail.html', context )
