from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Trainer


class TrainerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Trainer
        fields = ['id','name', 'email', 'salary', 'type', 'password']
