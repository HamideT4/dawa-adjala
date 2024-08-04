from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from core import settings
from .forms import CustomUserCreationForm, PaymentForm, TransferForm
from .models import User, Payment, Account, Recharge, Rechargebook, Transfer
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .tokens import account_activation_token
from django.views.decorators.http import require_GET
from dal import autocomplete
from django.db.models import Q


from django.db.models import Sum
from django.db.models.functions import TruncMonth
from collections import OrderedDict
import datetime

from weasyprint import HTML

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            #login_url = reverse('authentication:login')
            #return redirect(login_url)

            # Send confirmation email
            current_site = get_current_site(request)
            subject = 'Activer votre compte'
            message = render_to_string(
                'registration/account_activation_email.html', {
                'user': user,
                'domain': 'localhost:8000' if settings.DEBUG else current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.info(request, "Un lien d\'activation a été envoyé à votre adresse mail. Veuillez vérifier votre boîte de réception et cliquer sur le lien d\'activation pour activer votre compte.")
            return redirect('/')
        else:
            # Le formulaire n'est pas valide, afficher les erreurs
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render (request, 'registration/signup.html', {'form': form})


#-------------------------------------------------------------------

def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


#-------------------------------------------------------------------

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login_url = reverse('authentication:login')
        return redirect(login_url)
        #return redirect('/')
    else:
        return HttpResponseBadRequest("Le lien d'activation est invalide")

#-----------------------------------------------------------------------
    
def account_activation_complete(request):
    return render(request, 'registration/account_activation_complete.html')
    

# ----------------------------------------------------------------------

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Email ou mot de passe incorrect.")
        return self.render_to_response(self.get_context_data(form=form))


    def get_success_url(self):
        messages.success(self.request, "Connexion réussie.")
        return reverse('authentication:user_dashboad')
    

#-------------------------------------------------------------------------
    
class UserView(DetailView):
    model = User
    template_name = 'registration/profile.html'

#-------------------------------------------------------------------------

@login_required
def user_dashbord(request):
    user = request.user
    user_account = user.account

    account_number = user_account.get_account_unique_identifier()
    balance = user_account.get_balance()

    recent_recharges = Recharge.objects.filter(source_account=user_account).order_by('-date')[:5]
    recent_payments = Payment.objects.filter(user=user).order_by('-date')[:5]


    context = {
        'user':user,
        'account_number': account_number,
        'balance': balance,
        'recent_recharges': recent_recharges,
        'recent_payments': recent_payments,
        'parent': 'dashbord',
        'segment': 'index',
    }

    return render(request, 'dashbord/index.html', context)

#-----------------------------------------------------------------------------------


@login_required
def view_rechargebook(request):
    rechargebook = get_object_or_404(Rechargebook, owner=request.user)

    context = {
        'rechargebook': rechargebook,
        'owner': request.user,
        'parent': 'dashbord',
        'segment': 'book',
    }

    return render(request, 'dashbord/rechargebook_view.html', context)

#-----------------------------------------------------------------------------------

@login_required
def view_recharge(request):
    user = request.user
    recharges = Recharge.objects.filter(source_account__owner=user, coupon__is_used=False)
    
    context = {
        'recharges': recharges,
        'parent': 'dashbord',
        'segment': 'coupon',
    }

    return render(request, 'dashbord/recharges.html', context)

#--------------------------------------------------------------------------

@login_required
def view_payment(request):
    user = request.user
    payments = Recharge.objects.filter(source_account__owner=user, coupon__is_used=True)
    
    context = {
        'payments': payments,
        'parent': 'dashbord',
        'segment': 'payment',
    }

    return render(request, 'dashbord/payments.html', context)

#------------------------------------------------------------------------------

@login_required
def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, user=request.user)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            coupon = form.cleaned_data['coupon']
            amount = coupon.amount
            user_account = request.user.account

            if user_account.balance < amount:
                messages.error(request, "Votre solde est insuffisant pour effectuer ce paiement.")
            else:
                # Effectuer le paiement
                hospital_account = recipient.account
                user_account.balance -= amount
                hospital_account.balance += amount
                user_account.save()
                hospital_account.save()

                # Marquer le coupon comme utilisé
                coupon.is_used = True
                coupon.save()

                # Enrégistrer le paiement
                Payment.objects.create(user=request.user, recipient=recipient, amount=amount, coupon=coupon)


                messages.success(request, "Le paiement a été effectué avec succès.")

                return redirect('authentication:user_dashboad')
    else:
        form = PaymentForm(user=request.user)

    return render(request, 'make_payment.html', {'form':form})

#---------------------------------------------------------------------------
@login_required
def user_autocomplete(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        users = User.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).distinct()
        
        results = []
        for user in users:
            user_json = {
                'id': user.id,
                'text': f'{user.first_name} {user.last_name}',
                'image_url': user.avatar.url  # Assurez-vous que le champ avatar a une URL valide
            }
            results.append(user_json)
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})
#----------------------------------------------------------------------------

@login_required
def make_transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            coupon = form.cleaned_data['coupon']
            amount = coupon.amount
            sender = request.user 
            #recipient = form.cleaned_data['recipient']
            
            recipient_id = request.POST.get('recipient_id')
            try:
                recipient = User.objects.get(id=recipient_id)
            except User.DoesNotExist:
                form.add_error('recipient', 'Le destinataire sélectionné est invalide.')
                return render(request, 'make_transfer.html', {'form': form})

            # Mettre à jour les soldes des utilisateurs
            recipient.account.balance += amount
            sender.account.balance -= amount
            recipient.account.save()
            sender.account.save()

            # Enregistrer le transfert dans la base de données
            Transfer.objects.create(coupon=coupon, sender=sender, amount=amount, recipient=recipient)

            # Marquer le coupon comme utilisé pour l'utilisateur actuel
            coupon.is_used = True
            coupon.save()

            messages.success(request, f"Le coupon a été transféré avec succès à {recipient.get_full_name}.")
            return redirect('authentication:user_dashboad')
        else:
            messages.error(request, "There was an error with your form")
       
    else:
        form = TransferForm(user=request.user)

    return render(request, 'make_transfer.html', {'form': form})



#---------------------------------------------------------------------------
@login_required
def get_monthly_savings(request):
    user = request.user

    # Obtenir les épargnes de l'utilisateur, groupées par mois
    savings = Recharge.objects.filter(source_account__owner=user).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')

    # Créer un dictionnaire pour contenir les données des 12 mois avec une valeur par défaut de 0
    current_year = datetime.datetime.now().year
    monthly_savings = OrderedDict((datetime.date(current_year, month, 1).strftime('%Y-%m'), 0) for month in range(1, 13))

    # Remplir le dictionnaire avec les valeurs d'épargne
    for s in savings:
        monthly_savings[s['month'].strftime('%Y-%m')] = s['total']

    data = {
        'labels': list(monthly_savings.keys()),
        'data': list(monthly_savings.values())
    }
    return JsonResponse(data)

#--------------------------------------------------------------------------------------------------------------------------------
@login_required
def get_expense_distribution(request):
    user = request.user
    user_account = user.account
    total_recharges = user_account.balance
    #total_recharges = Recharge.objects.filter(source_account=user.account).aggregate(total=Sum('amount'))['total'] or 0
    total_payments = Payment.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0

    data = {
        'labels': ['Épargne actuelle', 'Paiements vers les Hôpitaux'],
        'data': [total_recharges, total_payments],
    }
    return JsonResponse(data)

#----------------------------------------------------------------------------------------------------------------
def print_rechargebook(request, pk):
    rechargebook = get_object_or_404(Rechargebook, pk=pk)
    context = {
        'rechargebook': rechargebook,
        'owner': rechargebook.owner,
    }
    return render(request, 'print_rechargebook.html', context)