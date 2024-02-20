from django.shortcuts import render, redirect
from .forms import HospitalRegisterForm

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

