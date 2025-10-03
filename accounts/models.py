from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    # Replace username with email
    username = None
    email = models.EmailField(unique=True)

    # Role field (basic RBAC)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('volunteer', 'Volunteer'),
        ('community', 'Community Member'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='community')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Removes username requirement

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

# Create your models here.
