from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserRegistrationForm,UniversityRegistrationForm,UniversityLoginForm,HeadRegistrationForm,HeadLoginForm
from django.contrib import messages
from .models import University,Head,Department,EventCoordinator,Student
from django.contrib.auth import login,logout
import random
import string
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate
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
                num = random.randint(1000000000000, 9999999999999)#13
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
            return render(request,'UniDashboard.html')
        else:
            print("user_form errors:", user_form.errors)
            print("uni_form errors:", uni_form.errors)
            messages.error(request, "Form is not valid. Enter your details accordingly!")
    else:
        user_form = UserRegistrationForm()
        uni_form = UniversityRegistrationForm()
    context = {'user_form': user_form, 'uni_form': uni_form}
    return render(request, 'university.html', context)    

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
                            return redirect('dashboard')
                        else:
                            messages.error(request, 'University is not approved yet.')
                    except University.DoesNotExist:
                        messages.error(request, 'Invalid University ID or credentials.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UniversityLoginForm()
    return render(request, 'customlog.html', {'form': form})

@login_required
def university_dashboard(request,university):
    if not university.is_approved:
       messages.warning(request,"This University Account is pending for approval.")
       return render(request,'pending_uni.html')
    
    try:
        head_data = Head.objects.get(university=university)  
    except:
        head_data = None 
        if request.method == "POST":
            user_form = UserRegistrationForm(request.POST)
            head_form = HeadRegistrationForm(request.POST, request.FILES)
            if user_form.is_valid() and head_form.is_valid():
                user = user_form.save()    
                used_numbers = set(Head.objects.values_list('head_id', flat=True))
                while True:
                    num = random.randint(100000000000, 999999999999)#12
                    if num not in used_numbers:
                        used_numbers.add(num)
                        print(num)
                        break
                chars = string.ascii_letters + string.digits
                password = ''.join(random.choice(chars) for _ in range(13))    
                head = head_form.save(commit=False)
                head.user = user
                head.head_id = num
                head.passkey=password
                head.university=university
                head.save()
                messages.success(request, 'University Event Head registered successfully!.Head can Log in now from Custom Login')
                return render(request,'UniDashboard.html')
            else:
                print("user_form errors:", user_form.errors)
                print("head_form errors:", head_form.errors)
                messages.error(request, "Form is not valid. Enter your details accordingly!")
        else:
            user_form = UserRegistrationForm()
            head_form = HeadRegistrationForm()
        context = {'user_form': user_form, 'head_form': head_form}
        return render(request, 'UniDashboard.html', context)                

    #will add more...    
    context = {'head_data':head_data}
    return render(request, 'UniDashboard.html', context)     

@login_required   
def Head_Register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        head_form = HeadRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and head_form.is_valid():
            user = user_form.save()    
            used_numbers = set(Head.objects.values_list('head_id', flat=True))
            while True:
                num = random.randint(100000000000, 999999999999)#12
                if num not in used_numbers:
                    used_numbers.add(num)
                    print(num)
                    break
            chars = string.ascii_letters + string.digits
            password = ''.join(random.choice(chars) for _ in range(13))    
            head = head_form.save(commit=False)
            head.user = user
            head.head_id = num
            head.passkey=password
            
            head.save()
            messages.success(request, 'University Event Head registered successfully!.Head can Log in now from Custom Login')
            return render(request,'UniDashboard.html')
        else:
            print("user_form errors:", user_form.errors)
            print("head_form errors:", head_form.errors)
            messages.error(request, "Form is not valid. Enter your details accordingly!")
    else:
        user_form = UserRegistrationForm()
        head_form = HeadRegistrationForm()
    context = {'user_form': user_form, 'head_form': head_form}
    return render(request, 'UniDashboard.html', context)     
 

def student_registration(request):
    ...

def custom_login(request):
    uni_form=UniversityLoginForm()
    head_form = HeadLoginForm()
    return render(request,'customlog.html',{'uni_form':uni_form,'head_form':head_form})


@login_required
def delete_head(request, head_id):
    head = get_object_or_404(Head, head_id=head_id)
    user = head.user
    head.delete()
    user.delete()  # Optionally delete the associated user account
    messages.success(request, "Head profile deleted successfully.")
    return redirect('dashboard')

def Head_login(request):
    if request.method == 'POST':
        form = HeadLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            uni_id = form.cleaned_data['head_id']
            passkey = form.cleaned_data['passkey']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                    try:
                        head = Head.objects.get(user=user, head_id=uni_id, passkey=passkey)
                        login(request, user)
                        return render(request,'head.html')
                    except Head.DoesNotExist:
                        messages.error(request, 'Invalid credentials.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UniversityLoginForm()
    return render(request, 'customlog.html', {'form': form})
def Department_login(request):
    ...
def coordinator_login(request):
    ...
def loginstudent(request):
    return render(request,'login.html')

@login_required
def dashboard(request):
    user = request.user
    try:
        university = University.objects.get(user=user)
        return university_dashboard(request,university)
    except University.DoesNotExist:
        pass
    
    try:
        head = Head.objects.get(user=user)
        return render(request, 'head_dashboard.html', {'head': head})
    except Head.DoesNotExist:
        pass
    
    try:
        department = Department.objects.get(user=user)
        return render(request, 'department_dashboard.html', {'department': department})
    except Department.DoesNotExist:
        pass
    
    try:
        coordinator = EventCoordinator.objects.get(user=user)
        return render(request, 'coordinator_dashboard.html', {'coordinator': coordinator})
    except EventCoordinator.DoesNotExist:
        pass

    messages.error(request,'🛑You are not authorized to access this page!🛑')
    return redirect('homepage')

@login_required
def delete_profile(request):
    user = request.user
    try:
        # Delete related profiles if they exist
        if hasattr(user, 'student'):
            user.student.delete()
        if hasattr(user, 'head'):
            user.head.delete()
        if hasattr(user, 'university'):
            user.university.delete()
        if hasattr(user, 'department'):
            user.department.delete()
        if hasattr(user, 'eventcoordinator'):
            user.eventcoordinator.delete()
    except Exception as e:
        # Optionally handle errors
        pass
    user.delete()
    logout(request)
    return redirect('homepage')  # Make sure this matches your urls.py

def logout_view(request):
    logout(request) 
    return redirect("homepage")


    