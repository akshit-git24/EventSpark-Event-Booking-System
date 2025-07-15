from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uni_id = models.PositiveIntegerField(unique=True,default=0)
    address = models.TextField()
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    contact_phone = models.CharField(max_length=10)
    is_approved = models.BooleanField(default=False)
    uni_document = models.FileField(upload_to='university_verify/', verbose_name="University Verification Document", help_text="Upload your university verification document",null=True,blank=True)
    passkey = models.CharField(max_length=15,default=123456789012345)
    photo = models.ImageField(upload_to='Universities_profile_photos/', null=True, blank=True)
    admin_photo = models.ImageField(upload_to='Universities_Admin_profile_photos/', null=True, blank=True)
    def __str__(self):
        return self.name
    
class Head(models.Model):
    name = models.CharField(max_length=25)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university=models.OneToOneField(University,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    contact_phone = models.CharField(max_length=10)
    head_id = models.PositiveIntegerField(unique=True,default=0)    
    head_document = models.FileField(upload_to='head/', verbose_name="University Event head Document", help_text="University Event Head verification document(optional)",null=True,blank=True)
    passkey = models.CharField(max_length=13,default=1234567890123)
    photo = models.ImageField(upload_to='head_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} (University: {self.university.name},ID: {self.head_id})"
    

class Department(models.Model):
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='departments')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department_id = models.PositiveIntegerField(unique=True,default=0)#10
    passkey = models.CharField(max_length=10,default=1234567890)#10
    photo = models.ImageField(upload_to='Department_photos/', null=True, blank=True)
    Department_admin = models.ImageField(upload_to='Department_Admin_photos/', null=True, blank=True)
    
    class Meta:
        unique_together = ('name', 'university')
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.name} ({self.university.name})"


class EventCoordinator(models.Model):
    name = models.CharField(max_length=100)
    department=models.OneToOneField(Department, on_delete = models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coord_id = models.PositiveIntegerField(unique=True,default=0)
    passkey = models.CharField(max_length=10,default=12345678)
    contact=models.PositiveIntegerField(max_length=10)
    document = models.FileField(upload_to='Coordinator/', verbose_name="Coordinaotr verification Document", help_text="Coordinator verification document(must for verification)",default=True)
    photo = models.ImageField(upload_to='EventCoordinator_Profile_Photos/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} (Department: {self.department}, ID: {self.coord_id})"
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    is_approved = models.BooleanField(default=False)#FOR department admin approval
    document = models.FileField(upload_to='student_documents/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)#FOR university head approval
    created_at = models.DateTimeField(auto_now_add=True)
    student_id=models.PositiveIntegerField(null=True, blank=True)
    document2 = models.FileField(upload_to='student_verified_head_document/',verbose_name="Verification Document",help_text="Upload your university verification document")
    photo = models.ImageField(upload_to='Student_Profile_photos/', null=True, blank=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    class Meta:
        unique_together = ('university', 'student_id')

    def __str__(self):
        return self.full_name

class Event(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    about=models.CharField(max_length=255,default=None)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    banner = models.ImageField(upload_to='event_banners/', null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    venue=models.CharField(default=None)
    details=models.CharField(default=None)
    # is_approved = models.BooleanField(default=False)#FOR university head approval
    
    def __str__(self):
        return f"{self.name} ({self.university.name})"


