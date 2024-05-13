# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import Account, Recharge

# @login_required
# def account_details(request):
#     # 1. Obtenez l'utilisateur connecté
#     user = request.user
    
#     # 2. Obtenez le compte associé à l'utilisateur connecté
#     user_account = user.account
    
#     # 3. Obtenez le numéro de compte et le solde du compte associé
#     account_number = user_account.get_account_unique_identifier()
#     balance = user_account.get_balance()
    
#     # 4. Obtenez les 5 dernières recharges associées à ce compte
#     recent_recharges = Recharge.objects.filter(source_account=user_account).order_by('-date')[:5]
    
#     context = {
#         'account_number': account_number,
#         'balance': balance,
#         'recent_recharges': recent_recharges,
#     }

#     return render(request, 'dashbord/index.html', context)
