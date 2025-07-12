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

class UniversityLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    uni_id = forms.CharField(label='University ID',help_text="This field is of integer type", max_length=13)
    passkey = forms.CharField(label='University ID', max_length=20)

