from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import University

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
       model = User
       fields = ['username', 'email', 'password1', 'password2']
  
class UniversityRegistrationForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'address', 'contact_email', 'contact_phone', 'uni_document']
        widgets = {'address': forms.Textarea(attrs={'rows': 3})}

