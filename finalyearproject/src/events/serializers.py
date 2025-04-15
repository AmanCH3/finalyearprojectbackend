from rest_framework import serializers
from .models import Event, Due

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class DueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Due
        fields = '__all__'
