from django.shortcuts import render, redirect
from .forms import HospitalRegisterForm
from django.contrib import messages
from .models import Hospital

def hospital_register(request):
    if request.method == 'POST':
        form = HospitalRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.is_approuved = False
            hospital.save()
            messages.success(request, "Votre hopital est inscrit avec succès, notre équipe vous contactera très prochainement pour son approbation.")
            return redirect('/')
        else:
            # Le formulaire n'est pas valide, afficher les erreurs
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = HospitalRegisterForm()
    return render(request, 'hospital/register.html', {'form': form})

def hospital_detail(request):

    hospital = Hospital.objects.all()
    approved_hospitals = Hospital.objects.filter(is_approuved=True)

    context = {
        'hospital': hospital,
        'approved_hospitals': approved_hospitals,
    }

    return render(request, 'hospital/detail.html', context )
