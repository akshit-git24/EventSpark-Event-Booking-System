from django.shortcuts import render,redirect,get_object_or_404
from .forms import (UserRegistrationForm,UniversityRegistrationForm,
UniversityLoginForm,HeadRegistrationForm,HeadLoginForm,StudentForm,
EventForm,DepartmentLoginForm,DepartmentForm,EventCoordinatorForm,CoordinatorLoginForm)
from django.contrib import messages
from .models import University,Head,Department,EventCoordinator,Student
from django.contrib.auth import login,logout
import random
import string
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Event
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
                num = random.randint(1000000000000, 9999999999999)  #13
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
            login(request, user)
            messages.success(request, 'University registered successfully! Waiting for admin approval.')
            return render(request,'pending_uni.html',{'university':university})
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
        uni_form = UniversityLoginForm(request.POST)
        if uni_form.is_valid():
            username = uni_form.cleaned_data['username']
            password = uni_form.cleaned_data['password']
            uni_id = uni_form.cleaned_data['uni_id']
            passkey = uni_form.cleaned_data['passkey']
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
        uni_form = UniversityLoginForm()
    return render(request, 'customlog.html', {'uni_form': uni_form})

@login_required
def university_dashboard(request,university):
    if not university.is_approved:
       messages.warning(request,"This University Account is pending for approval.")
       return render(request,'pending_uni.html',{'university':university})
    
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
                   
    departments=Department.objects.filter(university=university)
    students = Student.objects.filter(university=university)  # <-- Add this line
    if request.method == "POST":
        dept_form = DepartmentForm(request.POST, request.FILES)
        user_form = UserRegistrationForm(request.POST)
        if dept_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            used_numbers = set(Department.objects.values_list('uni_id', flat=True))
            while True:
                num = random.randint(1000000000, 9999999999)  #10
                if num not in used_numbers:
                    used_numbers.add(num)
                    print(num)
                    break
            chars = string.ascii_letters + string.digits
            password = ''.join(random.choice(chars) for _ in range(10))  
            department = dept_form.save(commit=False)
            department.university = university
            department.user = user
            department.department_id = num
            department.passkey = password
            department.save()
            messages.success(request, "Department created successfully!")
            return redirect('dashboard')
    else:
        dept_form = DepartmentForm()
        user_form = UserRegistrationForm()
    context = {'dept_form': dept_form,'departments':departments,'head_data':head_data,'user_form':user_form, 'students': students}  # <-- Add students to context
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
    dept_form = DepartmentLoginForm()
    coord_form=CoordinatorLoginForm()
    messages.error(request, "🛑Only Staff login allowed!🛑")
    return render(request,'customlog.html',{'uni_form':uni_form,'head_form':head_form,'dept_form':dept_form,'coord_form':coord_form})

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
        head_form = HeadLoginForm(request.POST)
        if head_form.is_valid():
            username = head_form.cleaned_data['username']
            password = head_form.cleaned_data['password']
            uni_id = head_form.cleaned_data['head_id']
            passkey = head_form.cleaned_data['passkey']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                    try:
                        head = Head.objects.get(user=user, head_id=uni_id, passkey=passkey)
                        login(request, user)
                        return redirect('dashboard')
                    except Head.DoesNotExist:
                        messages.error(request, 'Invalid credentials.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        head_form = HeadLoginForm()
    return render(request, 'customlog.html', {'head_form': head_form})

def Department_login(request):
    if request.method == 'POST':
        dept_form = DepartmentLoginForm(request.POST)
        if dept_form.is_valid():
            username = dept_form.cleaned_data['username']
            password = dept_form.cleaned_data['password']
            department_id = dept_form.cleaned_data['department_id']
            passkey = dept_form.cleaned_data['passkey']   
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    department = Department.objects.get(user=user, department_id=department_id, passkey=passkey)
                    login(request, user)
                    return redirect('dashboard')
                except Department.DoesNotExist:
                    messages.error(request, 'Invalid credentials.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        dept_form = DepartmentLoginForm()
    return render(request, 'customlog.html', {'dept_form': dept_form})

def coordinator_login(request):
    if request.method=="POST":
       coord_form=CoordinatorLoginForm(request.POST)
       if coord_form.is_valid():
            username = coord_form.cleaned_data['username']
            password = coord_form.cleaned_data['password']
            coord_id = coord_form.cleaned_data['coord_id']
            passkey = coord_form.cleaned_data['passkey'] 
            user=authenticate(request, username=username , password=password)
            if user is not None:
                try:
                    coordinator=EventCoordinator.objects.get(user=user,coord_id=coord_id,passkey=passkey)
                    login(request,user)
                    return redirect('dashboard')
                except:
                    messages.error(request,'Invalid credentials for Coordinator Form!')
            else:
                messages.error(request, 'Invalid username or password.')        
    else:
       coord_form=CoordinatorLoginForm()
       
    return render(request,'customlog.html',{'coord_form':coord_form})          

def loginstudent(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')

        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                student = Student.objects.get(user=user)
                university = student.university
                student_with_id = Student.objects.get(university=university, student_id=student_id)
                if student_with_id.user == user and student.is_approved:
                    login(request, user)
                    messages.success(request, "Welcome student!")
                    return redirect('/')
                else:
                    messages.error(request, "Student ID does not match your account.")
            except Student.DoesNotExist:
                messages.error(request, "Invalid student or student ID.")
        else:
            messages.error(request, "Invalid username or password.")
        auth_form = AuthenticationForm()
        std_form = StudentForm()
        return render(request, 'login.html', {'auth_form': auth_form, 'std_form': std_form})
    else:
        auth_form = AuthenticationForm()
        std_form = StudentForm()
    return render(request, 'login.html', {'auth_form': auth_form, 'std_form': std_form})
    
@login_required
def dashboard(request):
    user = request.user
    try:
        university = University.objects.get(user=user)
        return university_dashboard(request,university)
    except University.DoesNotExist:
        pass

    try:
        head_details = Head.objects.get(user=user)
        students = Student.objects.filter(university=head_details.university)
        departments = Department.objects.filter(university=head_details.university)
        coordinators = EventCoordinator.objects.filter(is_approved=False,department__in=departments)
        return render(request, 'head.html', {'head_details': head_details, 'students': students, 'coordinators': coordinators})
    except Head.DoesNotExist:
        pass

    try:
        department = Department.objects.get(user=user)
        return department_dashboard(request,department)
    except Department.DoesNotExist:
        pass
    
    try:
        coordinator = EventCoordinator.objects.get(user=user)
        return render(request, 'coordinator.html', {'coordinator': coordinator})
    except EventCoordinator.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        return render(request, 'coordinator_dashboard.html', {'coordinator': coordinator})
    except Student.DoesNotExist:
         pass
    messages.error(request,'🛑You are not authorized to access this page!,or you are a superuser.If super user,login to admin panel🛑')
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
    return redirect('homepage')  
###########3
def logout_view(request):
    logout(request) 
    return redirect("homepage")

@login_required
def create_event(request):
    try:
        university = University.objects.get(user=request.user)
    except University.DoesNotExist:
        messages.error(request, 'Only university users can create events.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.university = university
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('dashboard')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

@login_required
def university_events(request):
    try:
        university = University.objects.get(user=request.user)
    except University.DoesNotExist:
        messages.error(request, 'Only university users can view their events.')
        return redirect('dashboard')
    events = Event.objects.filter(university=university).order_by('-created')
    return render(request, 'event.html', {'events': events})

@login_required
def department_dashboard(request,department):
    try:
        coord_data = EventCoordinator.objects.get(department=department)
    except:
          coord_data = None
          if request.method == 'POST':
                user_form = UserRegistrationForm(request.POST)
                coordinator_form = EventCoordinatorForm(request.POST, request.FILES)
                if user_form.is_valid() and coordinator_form.is_valid():
                    user = user_form.save()
                    used_numbers = set(EventCoordinator.objects.values_list('coord_id', flat=True))
                    while True:
                        num = random.randint(10000000, 99999999)  #13
                        if num not in used_numbers:
                            used_numbers.add(num)
                            print(num)
                            break
                    chars = string.ascii_letters + string.digits
                    password = ''.join(random.choice(chars) for _ in range(8))  
                    coordinator = coordinator_form.save(commit=False)
                    coordinator.user = user
                    coordinator.department = department
                    coordinator.coord_id = num
                    coordinator.passkey = password
                    coordinator.save()
                    messages.success(request, 'Event coordinator registered successfully!,Waiting for Head Approval🤗')
                    return redirect('dashboard')
                else:
                    print("user_form errors:", user_form.errors)
                    print("coordinator_form errors:", coordinator_form.errors)
                    messages.error(request, "Form is not valid. Enter your details accordingly!")
          else:
                user_form = UserRegistrationForm()
                coordinator_form = EventCoordinatorForm()
          context = {'user_form': user_form, 'coordinator_form': coordinator_form}
          return render(request, '.html', context) 
    return render(request, 'department.html', {'department':department,'coord_data':coord_data})

@login_required
def approve_coordinator(request,coord_id):
    coord = get_object_or_404(EventCoordinator,coord_id=coord_id)
    coord.is_approved=True
    coord.save()
    messages.success(request, "Coordinator Approved successfully.They can now login to Coordinator Dashboard! ")
    return redirect('dashboard')

def head_dashboard(request):
    head_details=Head.objects.get(user=request.user)
    
def about_page(request):
    return render(request, 'about.html')
    