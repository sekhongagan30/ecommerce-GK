from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser): # this is basically a table
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email # this return is applied on db model show of this table User on admin url

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # oneToOne means whenever we del user, its profile will be deleted
    # auth_token = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="image", default='', blank=True)
    full_name=models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=100, default='')
    is_verified = models.BooleanField(default=False) # verified from email
    def __str__(self):
        return self.full_name
