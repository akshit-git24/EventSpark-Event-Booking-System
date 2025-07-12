from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UniversityRegistrationForm,UniversityLoginForm
from django.contrib import messages
from .models import University
from django.contrib.auth import login,logout
import random
import string
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate
from .forms import UniversityLoginForm
# Create your views here.
def homepage(request):
    return render(request,'home.html')

def UniversityRegister(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        uni_form = UniversityRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and uni_form.is_valid():
            user = user_form.save()    
            used_numbers = set(University.objects.values_list('uni_id', flat=True))
            while True:
                num = random.randint(1000000000000, 9999999999999)
                if num not in used_numbers:
                    used_numbers.add(num)
                    print(num)
                    break
            chars = string.ascii_letters + string.digits
            password = ''.join(random.choice(chars) for _ in range(15))    
            university = uni_form.save(commit=False)
            university.user = user
            university.uni_id = num
            university.passkey=password
            university.save()
            messages.success(request, 'University registered successfully! Waiting for admin approval.')
            return render(request,'home.html')
        else:
            print("user_form errors:", user_form.errors)
            print("uni_form errors:", uni_form.errors)
            messages.error(request, "Form is not valid. Enter your details accordingly!")
    else:
        user_form = UserRegistrationForm()
        uni_form = UniversityRegistrationForm()
    context = {'user_form': user_form, 'uni_form': uni_form}
    return render(request, 'university.html', context)     

def pending_approval_university(request):
    university = University.objects.filter(user=request.user)
    if not(university.is_approved):
       return render(request,'pending_uni.html')
    elif university.is_approved:
        return render(request,'UniDashboard.html')
    else:
        messages.error(request,"University does not exist!")

def student_registration(request):
    ...
def custom_login(request):
    uni_form=UniversityLoginForm()
    return render(request,'customlog.html',{'uni_form':uni_form})

def university_login(request):
    if request.method == 'POST':
        form = UniversityLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            uni_id = form.cleaned_data['uni_id']
            passkey = form.cleaned_data['passkey']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                    try:
                        university = University.objects.get(user=user, uni_id=uni_id, passkey=passkey)
                        if university.is_approved:
                            login(request, user)
                            return redirect('UniDashboard')
                        else:
                            messages.error(request, 'University is not approved yet.')
                    except University.DoesNotExist:
                        messages.error(request, 'Invalid University ID or credentials.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UniversityLoginForm()
    return render(request, 'customlog.html', {'form': form})
def Head_login(request):
    ...
def Department_login(request):
    ...
def coordinator_login(request):
    ...
def loginstudent(request):
    return render(request,'login.html')

# def loginUniversity(request):

