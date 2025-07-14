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
    path('delete-profile/',views.delete_profile,name='delete-profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('Head-login/', views.Head_login, name='head-login'),
    path('delete_head/<int:head_id>/', views.delete_head, name='delete_head'),
    path('create-event/', views.create_event, name='create-event'),
    path('events/', views.university_events, name='university-events'),
    path('department-login/', views.Department_login, name='department-login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)