from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    GENDER_CHOICES = (
        ('M','male'),
        ('F','female'),
        ('O','others')
    )
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    address = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
