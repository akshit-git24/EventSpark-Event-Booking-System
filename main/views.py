from django.shortcuts import render,redirect,get_object_or_404
from .forms import (UserRegistrationForm,UniversityRegistrationForm,
UniversityLoginForm,HeadRegistrationForm,HeadLoginForm,StudentForm,
EventForm,DepartmentLoginForm,DepartmentForm,EventCoordinatorForm,CoordinatorLoginForm,StudentLoginForm)
from django.contrib import messages
from .models import University,Head,Department,EventCoordinator,Student,Event,Ticket
from django.contrib.auth import login,logout
import random
import string
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
import json
from datetime import datetime
from django.utils import timezone

client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

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
            used_numbers = set(Department.objects.values_list('department_id', flat=True))
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
                    if coordinator.is_approved :
                        login(request,user)
                        return redirect('dashboard')
                    else:
                        messages.error(request,'Your id isnt appproved by the University Event head!')
                except:
                    messages.error(request,'Invalid credentials for Coordinator Form!')
            else:
                messages.error(request, 'Invalid username or password.')        
    else:
       coord_form=CoordinatorLoginForm() 
    return render(request,'customlog.html',{'coord_form':coord_form})          

def loginstudent(request):
    if request.method == 'POST':
        std_form=StudentLoginForm(request.POST)
        if std_form.is_valid():
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
                        return redirect('dashboard')
                    else:
                        messages.error(request, "Student ID does not match your account.")
                except Student.DoesNotExist:
                    messages.error(request, "Invalid student or student ID.")
            else:
                messages.error(request, "Invalid username or password.")
            std_form = StudentLoginForm()
            return render(request, 'login.html', {'std_form': std_form})
    else:
        std_form = StudentLoginForm()
    return render(request, 'login.html',{'std_form': std_form})
    
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
        events=Event.objects.filter(university=head_details.university,is_approved=True)
        pend_events=Event.objects.filter(university=head_details.university,is_approved=False)
        return render(request,'head.html', {'head_details': head_details, 'students': students, 'coordinators': coordinators,'events':events,'pend_events':pend_events,'departments':departments})   
    except Head.DoesNotExist:
        pass

    try:
        department = Department.objects.get(user=user)
        return department_dashboard(request,department)
    except Department.DoesNotExist:
        pass
    
    try:
        coordinator = EventCoordinator.objects.get(user=user)
        events=Event.objects.filter(university=coordinator.department.university,is_approved=True)
        students=Student.objects.filter(department=coordinator.department)
        return render(request, 'coordinator.html', {'coordinator': coordinator,'events':events,'students':students})   
    except EventCoordinator.DoesNotExist:
        pass
    try:
        student = Student.objects.get(user=user)
        return student_dashboard(request,student)
    except Student.DoesNotExist:
        pass
    messages.error(request,'🛑You are not authorized to access this page!,or you are a superuser.If superuser,login to admin panel🛑')
    return redirect('homepage')



def approve_event(request,id):
    event = get_object_or_404(Event, id=id)
    event.is_approved = True
    event.save()
    messages.success(request, "Event Approved successfully✅")
    return redirect("dashboard")

def reject_event(request,id):
    event = get_object_or_404(Event, id=id)
    event.delete()
    messages.success(request, "Event Rejected successfully✅")
    return redirect("dashboard")

def logout_view(request):
    logout(request) 
    return redirect("homepage")

@login_required
def create_event(request):
    user = request.user
    coordinator = EventCoordinator.objects.get(user=user)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.department = coordinator.department
            event.university = coordinator.department.university
            event.save()
            messages.success(request, "Event created successfully!")
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
    students=Student.objects.filter(department=department)
    return render(request, 'department.html', {'department':department,'coord_data':coord_data,'students':students})

@login_required
def approve_coordinator(request,coord_id):
    coord = get_object_or_404(EventCoordinator,coord_id=coord_id)
    coord.is_approved=True
    coord.save()
    messages.success(request, "Coordinator Approved successfully.They can now login to Coordinator Dashboard! ")
    return redirect('dashboard')
 
def about_page(request):
    return render(request, 'about.html')
    
def register_student(request):
    if request.method =="POST":
        user_form=UserRegistrationForm(request.POST)
        std_form=StudentForm(request.POST,request.FILES)
        if user_form.is_valid() and std_form.is_valid():
            user = user_form.save()
            student = std_form.save(commit=False)
            student.user=user
            student.save()
            login(request,user)
            messages.success(request, 'University Event Head registered successfully!.Head can Log in now from Custom Login')
            return render(request,'home.html')
        else:
            messages.error(request,"Invalid form! Enter the details accordingly.")
    else:
        user_form=UserRegistrationForm()
        std_form=StudentForm()       
    return render(request,'student_register.html',{'user_form':user_form,'std_form':std_form})

def student_dashboard(request,student):
    if not student.is_approved:
       messages.warning(request,"This University Account is pending for approval.")
       return render(request,'pending_student.html',{'student':student})
    
    if not student.is_verified:
       messages.warning(request,"This Account is pending for approval by your University Event Head.")
       return render(request,'pending_veri.html',{'student':student})
    
    if student.is_rusticated:
       messages.error(request,'You are Rusticated from using this website!')
       return render(request,'rusticated.html',{'student':student})
    
    events=Event.objects.filter(university=student.university,is_approved=True)
    return render(request, 'student_dashboard.html',{'student': student,'events':events})

@login_required
def register_event(request, id):
    try:
        student = Student.objects.get(user=request.user)
        event = get_object_or_404(Event, id=id, is_approved=True)

        existing_ticket = Ticket.objects.filter(
            user=student.user, event=event, payment_status='completed'
        ).first()
        if existing_ticket:
            messages.warning(request, 'You are already registered for this event!')
            return redirect('dashboard')

        
        if event.tickets is not None and event.tickets <= 0:
            messages.error(request, 'No tickets available for this event!')
            return redirect('dashboard')

       
        if event.fee == 0:
            ticket = Ticket.objects.create(
                event=event,
                user=student.user,
                amount_paid=0,
                payment_status='completed'
            )
            
            if event.tickets is not None:
                event.tickets -= 1
                event.save()
            messages.success(request, f'Registered for {event.name}! Your ticket ID is {ticket.ticket_id}.')
            return redirect('student_tickets')

        context = {'event': event,'student': student,'razorpay_key': settings.RAZORPAY_API_KEY}
        return render(request, 'event_register.html', context)

    except Student.DoesNotExist:
        messages.error(request, 'Only students can register for events.')
        return redirect('dashboard')

@login_required
def create_payment_order(request, id):
    if request.method=="POST":
        try:
            student = Student.objects.get(user=request.user)
            event = get_object_or_404(Event, id=id, is_approved=True)
            existing_ticket = Ticket.objects.filter(user=student.user,event=event,payment_status='completed').first()
            if existing_ticket:
                return JsonResponse({'error': 'Already registered for this event'}, status=400)
           
            if event.tickets is not None and event.tickets <= 0:
                return JsonResponse({'error': 'No tickets available for this event!'}, status=400)
                
            ticket = Ticket.objects.create(event=event,user=student.user,amount_paid=event.fee,payment_status='pending')
            amount = int(event.fee * 100)
            razorpay_order = client.order.create({'amount': amount,'currency': 'INR','payment_capture': '1','notes': {'ticket_id': ticket.ticket_id,'event_id': str(event.id),'student_id': str(student.student_id)}})
           
            ticket.payment_id = razorpay_order['id']
            ticket.save()
            return JsonResponse({'order_id': razorpay_order['id'],'amount': amount,'currency': 'INR','ticket_id': ticket.ticket_id})
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            try:
                client.utility.verify_payment_signature(params_dict)

                
                ticket = Ticket.objects.get(payment_id=razorpay_order_id)
                ticket.payment_status = 'completed'
                ticket.time = timezone.now() 
                ticket.save()

                
                event = ticket.event
                if event.tickets is not None and event.tickets > 0:
                    event.tickets -= 1
                    event.save()

               
                student = Student.objects.get(user=ticket.user)

                
                request.session['ticket_success'] = f'Payment successful! You are registered for {event.name}. Ticket ID: {ticket.ticket_id}'
                return JsonResponse({'redirect_url': '/my-tickets/'})

            except razorpay.errors.SignatureVerificationError:
              
                ticket = Ticket.objects.get(payment_id=razorpay_order_id)
                ticket.payment_status = 'failed'
                ticket.save()

                return JsonResponse({
                    'success': False,
                    'message': 'Payment verification failed'
                })

        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Ticket not found'})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Student not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def approve_student(request,student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student.is_approved = True
    student.save()
    messages.success(request, "Student approved successfully!")
    return redirect('dashboard')

@login_required
def reject_student(request,student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student.delete()
    messages.success(request, "Student rejected successfully!")
    return redirect('dashboard')

@login_required
def student_tickets(request):
    """View all tickets for the logged-in student"""
    try:
        student = Student.objects.get(user=request.user)
       
        Ticket.objects.filter(user=request.user, payment_status='pending').delete()
        tickets = Ticket.objects.filter(user=request.user).order_by('-registration_time')
        ticket_success = request.session.pop('ticket_success', None)
        context = {
            'student': student,
            'tickets': tickets,
            'ticket_success': ticket_success
        }
        return render(request, 'student_tickets.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Only students can view tickets.')
        return redirect('dashboard')

@login_required
def assign_department(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        department_id = request.POST.get('department')
        if department_id:
            department = get_object_or_404(Department, id=department_id)
            student.department = department
            student.save()
            messages.success(request, f"Assigned {department.name} to {student.full_name}.")
        else:
            student.department = None
            student.save()
            messages.info(request, f"Removed department assignment for {student.full_name}.")
    return redirect('dashboard')

@login_required
def delete_department(request,department_id):
    department = get_object_or_404(Department, department_id=department_id)
    department.user.delete()
    messages.success(request, "Department Deleted Successfully!")
    return redirect('dashboard')

@login_required
def verify_student(request,student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student.is_verified = True
    student.save()
    messages.success(request, "Student Verified successfully!")
    return redirect('dashboard')
    
@login_required
def rusticate(request,student_id):
    student=get_object_or_404(Student,student_id=student_id)
    student.is_rusticated=True
    student.save()
    messages.success(request, "Student Rusticated successfully!")
    return redirect('dashboard')
    
@login_required
def remove_rusticate(request,student_id):
    student=get_object_or_404(Student,student_id=student_id)
    student.is_rusticated=False
    student.save()
    messages.success(request, "Student Dashboard Restored successfully!")
    return redirect('dashboard')
