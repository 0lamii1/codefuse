from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from utilities.base_model import BaseModel
from django.utils import timezone


class AppUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number=None, password=None):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        if not username:
            raise ValueError("Username is required")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, password=None):
        user = self.create_user(
            email=email,
            username=username,
            phone_number=phone_number,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=18, null=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number'] 
    objects = AppUserManager()

    class Meta:
        ordering = ['created_at', 'updated_at']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):  
        from app.models import Wallet
        is_new = self._state.adding 
        super().save(*args, **kwargs)
        if self.is_verified and is_new and not Wallet.objects.filter(user=self).exists():
            Wallet.objects.create(user=self)
