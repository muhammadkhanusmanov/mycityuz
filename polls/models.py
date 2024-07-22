from django.db import models
from django.contrib.auth.models import User

class Posts(models.Model):
    branch_choices = [
        ('Ijara','IJARA'),
        ('Oldi-sotdi','OLDI-SOTDI'),
        ('Ishchi','ISHCHI')
    ]
    
    position_choices = [
        ('MIRZO ULUG`BEK','Mirzo Ulug`bek'),
        ('BODOMZOR','Bodomozor'),
        ('KOSMANOVTLAR','Kosmanovtlar'),
    ]
    
    title = models.CharField(max_length=50)
    branch = models.CharField(max_length=12,choices=branch_choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    description = models.CharField(max_length=350)
    position = models.CharField(max_length=60,choices=position_choices)
    location = models.CharField(max_length=80)
    pic1 = models.CharField(max_length=80)
    pic2 = models.CharField(max_length=80, blank=True, null=True)
    pic3 = models.CharField(max_length=80, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='reactions')
    rate = models.PositiveIntegerField(default=1)
    comment = models.CharField(max_length=140,blank=True,null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.post.title}"