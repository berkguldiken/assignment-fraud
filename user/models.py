from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Role (models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        NORMAL_USER = "GENERIC", 'Generic'
        ALLOWED_USER = "ALLOWED_USER", 'AllowedUser'
    
    base_role = Role.ADMIN

    role = models.CharField(max_length=100, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args,**kwargs)
