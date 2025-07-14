from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import University, Head, Department, EventCoordinator, Student

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
       model = User
       fields = ['username', 'email', 'password1', 'password2']
  

class UniversityRegistrationForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'address', 'contact_email', 'contact_phone', 'uni_document', 'photo']
        widgets = {'address': forms.Textarea(attrs={'rows': 3})}


class UniversityLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    uni_id = forms.CharField(label='University ID',help_text="This field is of integer type", max_length=13)
    passkey = forms.CharField(label='University Passkey', max_length=20)

class HeadLoginForm(forms.Form):
    username = forms.CharField(label='Username :', max_length=150)
    password = forms.CharField(label='Password :', widget=forms.PasswordInput)
    head_id = forms.CharField(label='University Event Head ID :',help_text="This field is of integer type", max_length=13)
    passkey = forms.CharField(label='Unique Passkey :', max_length=20)


class HeadRegistrationForm(forms.ModelForm):
    # university = forms.ModelChoiceField(queryset=University.objects.all(), required=True)
    # head_id = forms.IntegerField(required=True)
    # passkey = forms.CharField(max_length=13, required=True)
    photo = forms.ImageField(required=False)

    class Meta(UserRegistrationForm.Meta):
        model = Head
        fields = ['name','contact_phone','photo','head_document']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'university', 'user', 'department_id', 'passkey', 'photo']

class EventCoordinatorForm(forms.ModelForm):
    class Meta:
        model = EventCoordinator
        fields = ['name', 'department', 'user', 'coord_id', 'passkey', 'photo']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'university', 'full_name', 'email', 'phone', 'is_approved', 'rank', 'document', 'is_verified', 'student_id', 'document2', 'photo']

