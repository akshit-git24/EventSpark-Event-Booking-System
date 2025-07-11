from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uni_id=models.PositiveIntegerField(unique=True,default=0)
    address = models.TextField()
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    contact_phone = models.CharField(max_length=10)
    is_approved = models.BooleanField(default=False)
    uni_document = models.FileField(upload_to='university_verify/', verbose_name="University Verification Document", help_text="Upload your university verification document",null=True,blank=True)
    
    def __str__(self):
        return self.name