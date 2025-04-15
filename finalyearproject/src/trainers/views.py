from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Trainer
from .serializers import TrainerSerializer
from django.shortcuts import get_object_or_404
User = get_user_model()
class TrainerViewSet(viewsets.ViewSet): #Or viewsets.ModelViewSet (if you want all CRUD operations)
    permission_classes = [AllowAny]
    queryset = Trainer.objects.all()

    def list(self, request):
        queryset = Trainer.objects.all()
        serializer = TrainerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Trainer.objects.all()
        trainer = get_object_or_404(queryset, pk=pk)
        serializer = TrainerSerializer(trainer)
        return Response(serializer.data)

    def create(self, request):
        # Directly access username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        name = request.data.get('name')
        salary=request.data.get('salary')
        type=request.data.get('type')

        if not username or not password or not email or not name:
            return Response({'error': 'Username, password, email and name are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create the Django User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name
            )

            # Create the Trainer.  Assumes all fields for Trainer are in request.data

            trainer = Trainer.objects.create(
                name=name,
                email=email,
                salary=salary,
                type=type
            )


            # Return success response. Include user data in the response if needed.
            return Response({'message': 'Trainer created successfully', 'username': username, 'email': email, 'id':trainer.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = Trainer.objects.all()
        trainer = get_object_or_404(queryset, pk=pk)
        serializer = TrainerSerializer(trainer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Trainer.objects.all()
        trainer = get_object_or_404(queryset, pk=pk)
        trainer.delete()
        return Response({'message': 'Trainer deleted'}, status=status.HTTP_204_NO_CONTENT)