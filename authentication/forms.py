from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(input_formats=["%d/%m/%Y"])

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
    birth_date = forms.DateField(input_formats=["%d/%m/%Y"])

    class Meta(UserChangeForm):
        model = User
        fields = '__all__'
        error_class = "error"

# class SignUpForm(UserCreationForm):
#     birth_date = forms.DateField(input_formats=["%d/%m/%Y"])

#     class Meta:
#         model = User
#         fields = ['email', 'first_name', 'last_name', 'gender', 'birth_date', 'address', 'phone_number', 'avatar']


