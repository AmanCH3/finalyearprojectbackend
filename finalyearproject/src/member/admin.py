from django.contrib import admin
from .models import MembershipType, Members
# Register your models here.

admin.site.register(MembershipType)
admin.site.register(Members)