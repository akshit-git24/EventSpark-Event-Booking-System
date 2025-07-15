from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import University, Head, Department, EventCoordinator, Student, Event

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
       model = User
       fields = ['username', 'email', 'password1', 'password2']
  

class UniversityRegistrationForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'address', 'contact_email', 'contact_phone', 'uni_document', 'photo','admin_photo']
        widgets = {'address': forms.Textarea(attrs={'rows': 3})}


class UniversityLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    uni_id = forms.CharField(label='University ID',help_text="This field is of integer type", max_length=13)
    passkey = forms.CharField(label='University Passkey', max_length=20)

class HeadRegistrationForm(forms.ModelForm):
    photo = forms.ImageField(required=True)

    class Meta(UserRegistrationForm.Meta):
        model = Head
        fields = ['name','contact_phone','photo','head_document']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    

class HeadLoginForm(forms.Form):
    username = forms.CharField(label='Username :', max_length=150)
    password = forms.CharField(label='Password :', widget=forms.PasswordInput)
    head_id = forms.CharField(label='University Event Head ID :',help_text="This field is of integer type", max_length=13)
    passkey = forms.CharField(label='Unique Passkey :', max_length=20)

class DepartmentLoginForm(forms.Form):
    username = forms.CharField(label='Username :', max_length=150)
    password = forms.CharField(label='Password :', widget=forms.PasswordInput)
    department_id = forms.CharField(label='University Department ID :',help_text="This field is of integer type", max_length=13)
    passkey = forms.CharField(label='Unique Passkey :', max_length=20)

class CoordinatorLoginForm(forms.Form):
    username = forms.CharField(label='Username :', max_length=150)
    password = forms.CharField(label='Password :', widget=forms.PasswordInput)
    coord_id = forms.CharField(label='Coordinator ID :',help_text="This field is of integer type", max_length=13)
    passkey = forms.CharField(label='Unique Passkey :', max_length=20)

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'photo','Department_admin']
                                                        
class EventCoordinatorForm(forms.ModelForm):
    class Meta:
        model = EventCoordinator
        fields = ['name','contact', 'photo','document']
        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['university','photo','full_name','phone','student_id']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','about','details','start_date', 'start_time', 'end_date', 'end_time', 'banner', 'fee','venue']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(format='%H:%M:%S', attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}),
            'end_time': forms.TimeInput(format='%H:%M:%S', attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}),
            'address': forms.Textarea(attrs={'rows': 3})
        }
    



