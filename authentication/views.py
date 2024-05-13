from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from .models import User
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from accounts.models import Account, Recharge, Rechargebook
from django.shortcuts import get_object_or_404
from django.contrib import messages

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login_url = reverse('authentication:login')
            return redirect(login_url)
        else:
            # Le formulaire n'est pas valide, afficher les erreurs
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render (request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse('authentication:user_dashboad')
    
class UserView(DetailView):
    model = User
    template_name = 'registration/profile.html'

@login_required
def user_dashbord(request):
    user = request.user
    user_account = user.account

    account_number = user_account.get_account_unique_identifier()
    balance = user_account.get_balance()

    recent_recharges = Recharge.objects.filter(source_account=user_account).order_by('-date')[:5]

    context = {
        'user':user,
        'account_number': account_number,
        'balance': balance,
        'recent_recharges': recent_recharges,
    }

    return render(request, 'dashbord/index.html', context)

@login_required
def view_rechargebook(request):
    rechargebook = get_object_or_404(Rechargebook, owner=request.user)

    context = {
        'rechargebook': rechargebook,
        'owner': request.user
    }

    return render(request, 'dashbord/rechargebook_view.html', context)
   