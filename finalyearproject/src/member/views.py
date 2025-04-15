from datetime import timezone
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Members, MembershipType,Attendance
from trainers.models import Trainer
from .serializers import MemberSerializer, MembershipTypeSerializer,AttendanceSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime
User = get_user_model() # use the default django User model
class MemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Members model.
    """
    queryset = Members.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific member.
        """
        member = get_object_or_404(Members, pk=pk)
        serializer = MemberSerializer(member)
        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Data retrieved successfully!"
        })

    def destroy(self, request, pk=None):
        """
        Delete a specific member.
        """
        member = get_object_or_404(Members, pk=pk)
        member.delete()
        return Response({
            "data": "ok",
            "statusCode": 200,
            "message": "Data deleted successfully!"
        }, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        """
        Update a specific member.
        """
        member = get_object_or_404(Members, pk=pk)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": "updated data",
                "statusCode": 200,
                "message": "Data updated successfully!"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        Create a new member.
        """
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": "ok",
                "statusCode": 200,
                "message": "Member saved successfully!"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        List all members.
        """
        members = Members.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Data retrieved successfully!"
        })

    @action(detail=False, methods=['get'], url_path='count/(?P<type_name>[^/.]+)')
    def count_by_type(self, request, type_name=None):
        """
        Custom action to count members by membership type.
        """
        count = Members.objects.filter(membership_type__type_name=type_name).count()
        return Response({
            "data": count,
            "statusCode": 200,
            "message": "Count retrieved successfully!"
        })

class MembershipTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MembershipType model.
    """
    queryset = MembershipType.objects.all()
    serializer_class = MembershipTypeSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific membership type.
        """
        membership_type = get_object_or_404(MembershipType, pk=pk)
        serializer = MembershipTypeSerializer(membership_type)
        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Data retrieved successfully!"
        })

    def destroy(self, request, pk=None):
        """
        Delete a specific membership type.
        """
        membership_type = get_object_or_404(MembershipType, pk=pk)
        membership_type.delete()
        return Response({
            "data": "ok",
            "statusCode": 200,
            "message": "Membership type deleted successfully!"
        }, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        """
        Update a specific membership type.
        """
        membership_type = get_object_or_404(MembershipType, pk=pk)
        serializer = MembershipTypeSerializer(membership_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": "updated data",
                "statusCode": 200,
                "message": "Data updated successfully!"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        Create a new membership type.
        """
        serializer = MembershipTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": "ok",
                "statusCode": 200,
                "message": "Membership type saved successfully!"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        List all membership types.
        """
        membership_types = MembershipType.objects.all()
        serializer = MembershipTypeSerializer(membership_types, many=True)
        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Data retrieved successfully!"
        })
class AttendanceViewSet(viewsets.ViewSet):
    """
    ViewSet for managing attendance records.  Username-based check-in (less secure).
    """
    permission_classes = [permissions.AllowAny] # Removed authentication

    def create(self, request):
        """
        Check-in: Creates a new attendance record based on the provided username.
        """
        username = request.data.get('username') # Get username from request

        if not username:
            return Response({
                "data": None,
                "statusCode": 400,
                "message": "Username is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user=User.objects.get(username=username)
            member = Members.objects.get(email=user.email)  # Try to find the user by username
        except Members.DoesNotExist:
            return Response({
                "data": None,
                "statusCode": 404,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        # Check if the member has already checked in today
        today = timezone.now().date()
        if Attendance.objects.filter(member=member, date=today, time_out=None).exists():
            return Response({
                "data": None,
                "statusCode": 400,
                "message": "Member already checked in today."
            }, status=status.HTTP_400_BAD_REQUEST)


        attendance_data = {'member': member.pk} #Data to serialize
        serializer = AttendanceSerializer(data=attendance_data)  # NO request in context required for create.
        if serializer.is_valid():
            serializer.save(member=member)
            return Response({
                "data": serializer.data,
                "statusCode": 201,
                "message": "Check-in successful!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def check_out(self, request):
        """
        Check-out: Updates the time_out for the member's current attendance record based on username
        """
        username = request.data.get('username')

        if not username:
            return Response({
                "data": None,
                "statusCode": 400,
                "message": "Username is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            member = Members.objects.get(username=username)
        except Members.DoesNotExist:
            return Response({
                "data": None,
                "statusCode": 404,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)


        today = timezone.now().date()

        try:
            attendance_record = Attendance.objects.get(member=member, date=today, time_out__isnull=True)
        except Attendance.DoesNotExist:
            return Response({
                "data": None,
                "statusCode": 400,
                "message": "No active check-in record found for today."
            }, status=status.HTTP_400_BAD_REQUEST)

        attendance_record.time_out = timezone.now()
        attendance_record.save()

        serializer = AttendanceSerializer(attendance_record)

        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Check-out successful!"
        })

    def list(self, request):
        """
        List attendance records for a specific user (provide username in query params)
        """
        username = request.query_params.get('username')
        if not username:
          return Response({"data": None, "statusCode": 400, "message": "Username must be provided in query parameters"})

        try:
          user = User.objects.get(username=username)
          member=Members.objects.get(email=user.email)
        except User.DoesNotExist:
          return Response({"data": None, "statusCode": 404, "message": "Member not found"})

        attendance_records = Attendance.objects.filter(member=member).order_by('-date', '-time_in') # Order by date and time
        serializer = AttendanceSerializer(attendance_records, many=True)

        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Attendance records retrieved successfully."
        })

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific attendance record. Requires username parameter for validation
        """

        username = request.query_params.get('username')
        if not username:
          return Response({"data": None, "statusCode": 400, "message": "Username must be provided in query parameters"})

        try:
          user = User.objects.get(username=username)
          member=Members.objects.get(email=user.email)
        except User.DoesNotExist:
          return Response({"data": None, "statusCode": 404, "message": "Member not found"})

        try:
            attendance_record = Attendance.objects.get(pk=pk, member=member) # Ensure the member owns the record
        except Attendance.DoesNotExist:
            return Response({
                "data": None,
                "statusCode": 404,
                "message": "Attendance record not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AttendanceSerializer(attendance_record)
        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Attendance record retrieved successfully."
        })

