from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('university-register/',views.UniversityRegister,name='University-Register')
]
