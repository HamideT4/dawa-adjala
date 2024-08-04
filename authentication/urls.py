from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views
from .views import UserView, CustomLoginView,user_autocomplete, print_rechargebook

app_name = 'authentication'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/<int:pk>/', login_required(UserView.as_view()), name='profile'),
    path('signup/', views.signup, name='signup'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('account_activation_complete/', views.account_activation_complete, name='account_activation_complete'),
    path('user-dashboard/', login_required(views.user_dashbord), name='user_dashboad'),
    path('view-rechargebook/', login_required(views.view_rechargebook), name='view_rechargebook'),
    path('view_recharge/', login_required(views.view_recharge), name='view_recharge'),
    path('view_payment/', login_required(views.view_payment), name='view_payment'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('user-autocomplete/', user_autocomplete, name='user-autocomplete'),
    path('make_transfer/', views.make_transfer, name='make_transfer'),
    path('chart-data/', views.get_monthly_savings, name='get_monthly_savings'),
    path('chart-expense-distribution/', views.get_expense_distribution, name='get_expense_distribution'),
    path('root/rechargebook/<int:pk>/print/', print_rechargebook, name='print_rechargebook'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
