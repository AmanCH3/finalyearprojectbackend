from django.db import models
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() # use the default django User model
class MembershipType(models.Model):
    membership_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100)
    duration = models.IntegerField()  # in months
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.type_name

class Members(models.Model):
    member_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    membership_start_date = models.DateField(null=True, blank=True)
    membership_end_date = models.DateField(null=True, blank=True)
    membership_type = models.ForeignKey(MembershipType, on_delete=models.CASCADE, related_name='members',null=True, blank=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='attendance_records')  
    date = models.DateField(auto_now_add=True)
    time_in = models.TimeField(auto_now_add=True)
    time_out = models.TimeField(null=True, blank=True)  # Allow null for time_out

    def __str__(self):
        return f"Attendance for {self.member.username} on {self.date}"

