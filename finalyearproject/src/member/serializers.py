from rest_framework import serializers
from .models import Members  , MembershipType, Attendance
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() # use the default django User model
# Serializers define the API representation.
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'


#==MemberType serializers======
class MembershipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipType
        fields = '__all__'



class AttendanceSerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(queryset=Members.objects.all(), required=False, allow_null=True)  # Use Members.objects.all()

    class Meta:
        model = Attendance
        fields = ['id', 'member', 'date', 'time_in', 'time_out']
        read_only_fields = ['id', 'date', 'time_in']  
