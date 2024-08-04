from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from hospital.models import Hospital
from core import settings
from .models import User, Account, Notification, Coupon, Transfer
from django import forms
from dal import autocomplete

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(localize=True, widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}),)

    class Meta(UserCreationForm):
        model = User
        fields = ['email', 'first_name', 'last_name', 'gender', 'birth_date', 'address', 'phone_number', 'avatar']
        error_class = "error"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Cette adresse e-mail est déjà utilisée.")
        return email

class CustomUserChangeForm(UserChangeForm):
    birth_date = forms.DateField(localize=True, widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}),)

    class Meta(UserChangeForm):
        model = User
        fields = '__all__'
        error_class = "error"

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['owner', 'balance']

class PaymentForm(forms.Form):
    recipient = forms.ModelChoiceField(
        queryset=Hospital.objects.filter(is_approuved=True), 
        to_field_name="name",
        label="Destinataire",
        widget=forms.Select(attrs={
            'class': 'vd hh rg zk _g ch hm dm fm pl/50 xi mi sm xm pm dn/40'
        })
    )
    coupon = forms.ModelChoiceField(
        queryset=Coupon.objects.none(), 
        required=True,
        label="Coupon",
        widget=forms.Select(attrs={
            'class': 'vd hh rg zk _g ch hm dm fm pl/50 xi mi sm xm pm dn/40'
        })
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['coupon'].queryset = Coupon.objects.filter(recharge__source_account__owner=user, is_used=False)

class TransferForm(forms.ModelForm):

    recipient = forms.CharField(
        required=True,
        label="Destinataire",
        widget=forms.TextInput(attrs={
            'class': 'vd hh rg zk _g ch hm dm fm pl/50 xi mi sm xm pm dn/40',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = Transfer
        fields = ('recipient', 'coupon')

    coupon = forms.ModelChoiceField(
        queryset=Coupon.objects.none(),
        required=True,
        label="Sélectionnez un coupon",
        widget=forms.Select(attrs={
            'class': 'vd hh rg zk _g ch hm dm fm pl/50 xi mi sm xm pm dn/40'
        })
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user:
            self.fields['coupon'].queryset = Coupon.objects.filter(recharge__source_account__owner=user, is_used=False)

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['alert_type', 'account', 'status', 'content']
