from django.urls import path
from . import views
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('university-register/',views.UniversityRegister,name='University-Register'),
    path('login/',views.loginstudent,name='login-student'),
    path('custom-login/',views.custom_login,name='custom-login'),
    path('university-login/', views.university_login, name='university-login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('Head-login/', views.Head_login, name='head-login'),
    path('delete_head/<int:head_id>/', views.delete_head, name='delete_head'),
    path('create-event/', views.create_event, name='create-event'),
    path('events/', views.university_events, name='university-events'),
    path('department-login/', views.Department_login, name='department-login'),
    path('approve-coordinator/<int:coord_id>/', views.approve_coordinator, name='approve-coordinator'),
    path('coordinator-login/', views.coordinator_login, name='coordinator-login'),
    path('about/', views.about_page, name='about'),
    path('register-student/', views.register_student, name='register_student'),
    path("approve-event/<int:id>/", views.approve_event, name="approve_event"),
    path("reject-event/<int:id>/", views.reject_event, name="reject_event"),
    path("register-event/<int:id>/", views.register_event, name="register"),
    path("payment/<int:id>/create-order", views.create_payment_order, name="payment"),
    path("approve-student/<int:student_id>/", views.approve_student, name="approve_student"),
    path("reject-student/<int:student_id>/", views.reject_student, name="reject_student"),
    path("my-tickets/", views.student_tickets, name="student_tickets"),
    path('assign_department/<int:student_id>/', views.assign_department, name='assign_department'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),
    path('verify_student/<int:student_id>/', views.verify_student, name='verify_student'),
    path('rusticate/<int:student_id>/', views.rusticate, name='rusticate'),
    path('rm-rusticate/<int:student_id>/', views.remove_rusticate, name='rm-rusticate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)