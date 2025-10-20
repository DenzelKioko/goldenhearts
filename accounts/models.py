import os
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model using email as the unique identifier.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with email login.
    Default role is Patron (general user).
    """
    username = None
    email = models.EmailField(unique=True)
    # Images will be stored in media/profile_pics/
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        null=True, 
        blank=True,
    )

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('patron', 'Patron'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patron')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_patron(self):
        return self.role == 'patron'

    def get_profile_picture_url(self):
        """Safely get profile picture URL"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            try:
                # Check if file exists
                if os.path.exists(self.profile_picture.path):
                    return self.profile_picture.url
            except (ValueError, FileNotFoundError):
                pass
        return None 