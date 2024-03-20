from django.shortcuts import render
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from .models import User
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
    else:
        form = CustomUserCreationForm()
    return render (request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        return 'authentication:user_dashboad'
    
class UserView(DetailView):
    model = User
    template_name = 'registration/profile.html'

@login_required
def user_dashbord(request):
    user = request.user

    context = {
        'user':user,
    }

    return render(request, 'dashbord/index.html', context)
   