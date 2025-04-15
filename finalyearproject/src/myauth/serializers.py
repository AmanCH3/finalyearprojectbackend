from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from member.models import Members
from django.core.validators import MinLengthValidator

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role'] # Include the fields you want to expose in the dashboard
        read_only_fields = ['id', 'username', 'role']  # Optional:  Make these read-only
        
class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True, default='')  # Make optional
    last_name = serializers.CharField(required=False, allow_blank=True, default='')   # Make optional
    email = serializers.EmailField(required=False, allow_blank=True, default='')     # Make optional
    phone_number = serializers.CharField(validators=[MinLengthValidator(1)])
    address = serializers.CharField(validators=[MinLengthValidator(1)])
    date_of_birth = serializers.DateField()

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        email = validated_data.get('email','')
        phone_number = validated_data['phone_number']
        address = validated_data['address']
        date_of_birth = validated_data['date_of_birth']

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        member_name = f"{first_name} {last_name}".strip()

        try:
            member = Members.objects.create(  # Store the created member
                name=member_name if member_name else username,
                email=email,
                phone_number=phone_number,
                address=address,
                date_of_birth=date_of_birth,
            )
        except Exception as e:
            user.delete()
            raise serializers.ValidationError(f"Error creating member profile: {str(e)}")

        return user

    def update(self, instance, validated_data):
        # Not needed for registration, but required for a Serializer with save()
        raise NotImplementedError("Update method not supported for registration.")

    def to_representation(self, instance):
       # Customize the representation of the created User object.
        return {
            'id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            # You may want to include member details here as well,
            # if needed, by fetching them from the Members model.
        }

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        return user