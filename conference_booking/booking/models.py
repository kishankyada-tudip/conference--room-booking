import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
            
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    
class Room(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=32, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)    
    
class Slot(models.Model):
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="created_slots", on_delete=models.CASCADE)
    booked_by = models.ForeignKey(User, null=True, blank=True, related_name="booked_slots", on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_available = models.BooleanField(default=False, null=False, blank=False)