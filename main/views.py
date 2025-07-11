from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UniversityRegistrationForm
from django.contrib import messages
from .models import University
from django.contrib.auth import login,logout
import random
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
                num = random.randint(1000000001, 9999999999)
                if num not in used_numbers:
                    used_numbers.add(num)
                    print(num)
                    break
            university = uni_form.save(commit=False)
            university.user = user
            university.uni_id = num
            university.save()
            messages.success(request, 'University registered successfully! Waiting for admin approval.')
            return render(request, 'UniDashboard.html')
        else:
            print("user_form errors:", user_form.errors)
            print("uni_form errors:", uni_form.errors)
            messages.error(request, "Form is not valid. Enter your details accordingly!")
    else:
        user_form = UserRegistrationForm()
        uni_form = UniversityRegistrationForm()
    context = {'user_form': user_form, 'uni_form': uni_form}
    return render(request, 'university.html', context)     

