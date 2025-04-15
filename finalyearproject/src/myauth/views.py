from rest_framework import status
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from django.contrib.auth import login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from django.contrib.auth import authenticate, get_user_model
from member.models import MembershipType,Attendance
from trainers.models import Trainer
from member.serializers import Members,MemberSerializer
class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny] 
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserLoginView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             login(request, user)
#             return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
    


# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'userId': user.pk,
#             'role': user.role,
#         })


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)



class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'role': user.role
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserDashboardView(APIView):
    permission_classes = [permissions.AllowAny]  # Allows anyone to access

    def get(self, request, user_id):
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
            user_serializer = UserSerializer(user)

            try:
                # Assuming Member model has an 'email' field that matches the User model
                member = Members.objects.get(email=user.email)
                member_serializer = MemberSerializer(member)
                attendance=Attendance.objects.filter(member=member).count()
                # Combine the data from both serializers into a single response
                combined_data = {
                    'user': user_serializer.data,
                    'member': member_serializer.data,
                    'attendance':attendance
                }
                return Response(combined_data, status=status.HTTP_200_OK)

            except Members.DoesNotExist:
                # Handle the case where a Member object doesn't exist for the given email
                combined_data = {
                    'user': user_serializer.data,
                    'member': None  # Or some default value
                }
                return Response(combined_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
class AnalyticsViewSet(APIView):
    """
    ViewSet for providing analytics data.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Returns a summary of analytics data.
        """

        num_trainers = Trainer.objects.count()
        num_members = Members.objects.count()
        total_trainer_salary = Trainer.objects.all().aggregate(Sum('salary'))['salary__sum'] or 0  # Sum trainer salaries
        total_member_fees = MembershipType.objects.all().aggregate(Sum('price'))['price__sum'] or 0  # Sum member fees
        total_premium=Members.objects.filter(membership_type="3").count()
        total_standard=Members.objects.filter(membership_type="2").count()
        total_basic=Members.objects.filter(membership_type="1").count()    
        analytics_data = {
            "trainer_count": num_trainers,
            "member_count": num_members,
            "total_expenses": total_trainer_salary,
            "total_income": total_member_fees,
            "total_premium":total_premium,
            "total_standard":total_standard,
            "total_basic":total_basic
        }

        return Response({
            "data": analytics_data,
            "statusCode": 200,
            "message": "Analytics data retrieved successfully!"
        })