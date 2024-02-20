from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, login, authenticate
from django.views.generic import CreateView, FormView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import DoctorSignUpForm, PatientSignupForm
from .models import User
from django.contrib.auth.decorators import login_required

User = get_user_model()

def register(request):
    return render (request, 'registration/signup.html')

class DoctorSignupView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'registration/doctor_signup.html'

    def form_valid(self, form):
        user = form.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return redirect('/')

class PatientSignupView(CreateView):
    model = User
    form_class = PatientSignupForm
    template_name = 'registration/patient_signup.html'

    def form_valid(self, form):
        user = form.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        #user.save()
        form.save_m2m()
        login(self.request, user)
        return redirect('/')
    
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None :
                login(request,user)
                if user.is_doctor:
                    return redirect('authentication:doctor_dashboard')
                else:
                    return redirect('authentication:patient_dashboard')
            else:
                messages.error(request,"Email ou mot de passe incorrect")
        else:
            messages.error(request,"Email ou mot de passe incorrect")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form})

@login_required
def doctor_dashboard(request):

    doctor = request.user

    return render(request, 'dashboards/doctors/index.html', {'doctor': doctor})

@login_required
def patient_dashboard(request):

    patient = request.user

    return render(request, 'dashboards/patients/index.html', {'patient': patient})

@login_required
def medical_docs(request):

    doctor = request.user

    return render(request, 'dashboards/doctor/medical_docs.html', {'doctor': doctor})