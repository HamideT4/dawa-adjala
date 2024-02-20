from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Doctor, User, Patient
from hospital.models import Hospital

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        error_class = "error"

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class DoctorSignUpForm(CustomUserCreationForm):
    GENRE_CHOICES = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme')
    ]
    address = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=GENRE_CHOICES, widget=forms.RadioSelect)
    phone_number = forms.CharField(required=True)
    birth_date = forms.DateField(required=True)
    avatar = forms.ImageField(required=False)
    speciality = forms.CharField(required=True)
    hospital = forms.ModelChoiceField(
        queryset=Hospital.objects.all(),
        widget=forms.Select,
        required=True
    )
    service = forms.CharField(required=True)
    matricule = forms.CharField(required=True)

    class Meta(CustomUserCreationForm.Meta):
        model = User
        fields = CustomUserCreationForm.Meta.fields + ['address', 'gender', 'phone_number', 'birth_date', 'avatar', 'speciality', 'service', 'matricule', 'hospital']
        error_class = "error"

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        user.address = self.cleaned_data.get('address')
        user.gender = self.cleaned_data.get('gender')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.birth_date = self.cleaned_data.get('birth_date')
        user.avatar = self.cleaned_data.get('avatar')
        if commit:    
            user.save()
        hospital = self.cleaned_data['hospital']   
        doctor = Doctor.objects.create(
            user=user, hospital=hospital,
            speciality = self.cleaned_data.get('speciality'),
            service = self.cleaned_data.get('service'),
            matricule = self.cleaned_data.get('matricule')
        )
        if commit:
            doctor.save()
        return user
    
class PatientSignupForm(CustomUserCreationForm):
    GENRE_CHOICES = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme')
    ]
    address = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=GENRE_CHOICES, widget=forms.RadioSelect)
    phone_number = forms.CharField(required=True)
    birth_date = forms.DateField(required=True)
    avatar = forms.ImageField(required=False)
    antecedent = forms.CharField(required=True)
    medical_record = forms.CharField(required=True)
    allergies = forms.CharField(required=True)
    emergency_contact = forms.CharField(required=True)
    emergency_number = forms.CharField(required=True)
    weight = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step': '0.01'}))
    height = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step': '0.01'}))

    class Meta(CustomUserCreationForm.Meta):
        model = User
        fields = CustomUserCreationForm.Meta.fields + ['address', 'gender', 'phone_number', 'birth_date', 'avatar', 'antecedent', 'medical_record', 'allergies', 'emergency_contact', 'emergency_number', 'weight', 'height']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        user.address = self.cleaned_data.get('address')
        user.gender = self.cleaned_data.get('gender')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.birth_date = self.cleaned_data.get('birth_date')
        user.avatar = self.cleaned_data.get('avatar')
        if commit:
            user.save()

        patient = Patient.objects.create(user=user)
        patient.antecedent = self.cleaned_data.get('antecedent')
        patient.medical_record = self.cleaned_data.get('medical_record')
        patient.allergies = self.cleaned_data.get('allergies')
        patient.emergency_contact = self.cleaned_data.get('emergency_contact')
        patient.emergency_number = self.cleaned_data.get('emergency_number')
        patient.weight = self.cleaned_data.get('weight')
        patient.height = self.cleaned_data.get('height')
        if commit:
            patient.save()
        return user