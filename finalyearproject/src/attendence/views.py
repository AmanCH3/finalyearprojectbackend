from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from .models import Attendance , Transaction
from member.models import Members
from .serializers import AttendanceSerializer , TransactionSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny

class AttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Attendance records.
    Provides CRUD operations and custom actions for marking attendance.
    """
    queryset = Attendance.objects.all().order_by("-check_in")
    serializer_class = AttendanceSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        """
        Create a new attendance record.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "statusCode": 201,
                "message": "Attendance recorded successfully!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        List all attendance records.
        """
        attendance = self.get_queryset()
        serializer = self.get_serializer(attendance, many=True)
        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Attendance records retrieved successfully!"
        })

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific attendance record.
        """
        attendance = get_object_or_404(Attendance, pk=pk)
        serializer = self.get_serializer(attendance)
        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Attendance record retrieved successfully!"
        })

    def update(self, request, pk=None):
        """
        Update an attendance record.
        """
        attendance = get_object_or_404(Attendance, pk=pk)
        serializer = self.get_serializer(attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "statusCode": 200,
                "message": "Attendance record updated successfully!"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete an attendance record.
        """
        attendance = get_object_or_404(Attendance, pk=pk)
        attendance.delete()
        return Response({
            "data": "ok",
            "statusCode": 204,
            "message": "Attendance record deleted successfully!"
        }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def mark_attendance(self, request, pk=None):
        """
        Mark attendance (Check-in or Check-out).
        """
        member = get_object_or_404(Members, id=pk)
        today_attendance = Attendance.objects.filter(member=member, check_in__date=now().date()).first()

        if today_attendance and today_attendance.check_out is None:
            today_attendance.check_out = now()
            today_attendance.save()
            return Response({
                "message": f"{member.full_name} checked out successfully!",
                "statusCode": 200
            })
        else:
            Attendance.objects.create(member=member)
            return Response({
                "message": f"{member.full_name} checked in successfully!",
                "statusCode": 201
            })

    @action(detail=False, methods=["get"])
    def get_todays_attendance(self, request):
        """
        Get today's attendance records.
        """
        attendance = Attendance.objects.filter(check_in__date=now().date())
        serializer = self.get_serializer(attendance, many=True)
        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Today's attendance retrieved successfully!"
        })

    @action(detail=False, methods=["get"])
    def get_member_attendance(self, request):
        """
        Get all attendance records for a specific member.
        """
        member_id = request.query_params.get("member_id")
        member = get_object_or_404(Members, id=member_id)
        attendance = Attendance.objects.filter(member=member)
        serializer = self.get_serializer(attendance, many=True)
        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Member's attendance records retrieved successfully!"
        })

class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Transaction records.
    Provides CRUD operations and custom actions for transactions.
    """
    queryset = Transaction.objects.all().order_by("-transaction_date")
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Create a new transaction record.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "statusCode": 201,
                "message": "Transaction recorded successfully!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        List all transaction records.
        """
        transactions = self.get_queryset()
        serializer = self.get_serializer(transactions, many=True)
        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Transaction records retrieved successfully!"
        })
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific transaction record.
        """
        transaction = get_object_or_404(Transaction, pk=pk)
        serializer = self.get_serializer(transaction)
        return Response({
            "data": serializer.data,
            "statusCode": 200,
            "message": "Transaction record retrieved successfully!"
        })
    
    def update(self, request, pk=None):
        """
        Update a transaction record.
        """
        transaction = get_object_or_404(Transaction, pk=pk)
        serializer = self.get_serializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "statusCode": 200,
                "message": "Transaction record updated successfully!"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Delete a transaction record.
        """
        transaction = get_object_or_404(Transaction, pk=pk)
        transaction.delete()
        return Response({
            "data": "ok",
            "statusCode": 204,
            "message": "Transaction record deleted successfully!"
        }, status=status.HTTP_204_NO_CONTENT)
    