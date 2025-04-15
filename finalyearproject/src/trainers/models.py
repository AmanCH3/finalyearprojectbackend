from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer

# Model
class Trainer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name