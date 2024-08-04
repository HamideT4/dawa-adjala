from django import forms
from .models import Hospital

class HospitalRegisterForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'address', 'phone_number', 'description', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5})
        }