from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('member', 'Member'),
        ('receptionist', 'Receptionist'),
        ('accountant', 'Accountant'),
        ('manager', 'Manager'),
    )
    role = models.CharField(max_length=15, choices=ROLES, default='member')

    def __str__(self):
        return self.username