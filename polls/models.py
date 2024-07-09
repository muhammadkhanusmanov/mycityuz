from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    branch_choices = [
        ('Ijara','IJARA'),
        ('Oldi-sotdi','OLDI-SOTDI'),
        ('Ishchi','ISHCHI')
    ]
    
    title = models.CharField(max_length=50)
    branch = models.CharField(max_length=12,choices=branch_choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    description = models.CharField(max_length=350)
    location = models.CharField(max_length=80)
    pic1 = models.CharField(max_length=80)
    pic2 = models.CharField(max_length=80, blank=True, null=True)
    pic3 = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
