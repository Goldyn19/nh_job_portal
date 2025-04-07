from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUserManger(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)

        if extra_field.get('is_staff') is not True:
            raise ValueError('The User has to be a staff')
        if extra_field.get('is_superuser') is not True:
            raise ValueError('is_superuser must be true')
        return self.create_user(email=email, password=password, **extra_field)


class User(AbstractUser):
    USER_TYPE_OPTION = (
        ('job_seeker', 'Job_Seeker'),
        ('employer', 'Employer')
    )
    username = None
    email = models.EmailField(max_length=80, unique=True)
    first_name = models.CharField(null=True, blank=True, max_length=45)
    last_name = models.CharField(null=True, blank=True, max_length=45)
    profile_picture = models.URLField(null=True, blank=True,)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_OPTION)
    contact = models.CharField(max_length=25, null=True, blank=True)
    bio = models.TextField(null=True, blank=True,)
    company_name = models.CharField(null=True, blank=True, max_length=70)
    company_website = models.URLField(null=True, blank=True)
    objects = CustomUserManger()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.first_name, self.last_name


