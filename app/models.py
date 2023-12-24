

from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from httpx import request


# Create your models here.
class Teacher(models.Model):
    name=models.CharField(max_length=100)
    best=models.IntegerField(default=0)
    average=models.IntegerField(default=0)
    worst=models.IntegerField(default=0)
    def __str__(self):
        return self.name
    


class CustomUser(models.Model):
    username =models.EmailField(max_length=254,unique=True)
    review_count = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])
    otp=models.CharField(max_length=4)
    def __str__(self):
        return self.username
    