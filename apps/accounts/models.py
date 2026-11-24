from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        FARMER = 'FARMER', 'Farmer / Krishi Utpadak'
        BUYER = 'BUYER', 'Buyer / Trader'
        FPO_ADMIN = 'FPO_ADMIN', 'FPO Administrator'
        PLATFORM_ADMIN = 'PLATFORM_ADMIN', 'Platform Administrator'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FARMER)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    preferred_language = models.CharField(max_length=10, default='hi')
    is_phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_farmer(self):
        return self.role == self.Role.FARMER

    def is_buyer(self):
        return self.role == self.Role.BUYER

    def is_fpo(self):
        return self.role == self.Role.FPO_ADMIN

    def is_admin_user(self):
        return self.role == self.Role.PLATFORM_ADMIN or self.is_superuser

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
