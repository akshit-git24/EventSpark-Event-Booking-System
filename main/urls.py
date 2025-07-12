from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('university-register/',views.UniversityRegister,name='University-Register'),
    path('pending-approval-university/' ,views.pending_approval_university,name='pending-approval-university'),
    path('login/',views.loginstudent,name='login-student'),
    path('custom-login/',views.custom_login,name='custom-login'),
    path('university-login/', views.university_login, name='university-login'),
    path('unidashboard/', lambda request: render(request, 'UniDashboard.html'), name='UniDashboard'),
    
    # path('university-portal/',views.UniversityDashboard,name='University-Dashboard'),
]
