from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from agents.models import Agent
from customers.models import Customer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role', 'phone', 'avatar', 'company_name', 'agent', 'customer']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    role = serializers.CharField(source='profile.role', read_only=True)
    phone = serializers.CharField(source='profile.phone', read_only=True)
    avatar = serializers.CharField(source='profile.avatar', read_only=True)
    company_name = serializers.CharField(source='profile.company_name', read_only=True)
    full_name = serializers.SerializerMethodField()
    agent_id = serializers.SerializerMethodField()
    customer_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'role', 'phone', 'avatar', 'company_name',
            'agent_id', 'customer_id', 'is_staff', 'profile'
        ]

    def get_full_name(self, obj):
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name if name else obj.username

    def get_agent_id(self, obj):
        if hasattr(obj, 'profile') and obj.profile.agent:
            return obj.profile.agent.id
        return None

    def get_customer_id(self, obj):
        if hasattr(obj, 'profile') and obj.profile.customer:
            return obj.profile.customer.id
        return None


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    full_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=['customer', 'seller'], default='customer')
    phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    company_name = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        full_name = validated_data.get('full_name', '').strip()
        role = validated_data.get('role', 'customer')
        phone = validated_data.get('phone', '')
        company_name = validated_data.get('company_name', '')

        first_name = ''
        last_name = ''
        if full_name:
            parts = full_name.split(' ', 1)
            first_name = parts[0]
            if len(parts) > 1:
                last_name = parts[1]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        agent_record = None
        customer_record = None

        if role == 'seller':
            agent_record, _ = Agent.objects.get_or_create(
                email=email,
                defaults={
                    'name': full_name or username,
                    'phone': phone,
                    'agency_name': company_name or 'Prime Realty Partner',
                    'experience_years': 3,
                    'rating': 5.0,
                    'avatar': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&q=80',
                }
            )
        else:
            customer_record, _ = Customer.objects.get_or_create(
                email=email,
                defaults={
                    'name': full_name or username,
                    'phone': phone,
                    'customer_type': 'buyer',
                    'status': 'active',
                    'avatar': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
                }
            )

        UserProfile.objects.create(
            user=user,
            role=role,
            phone=phone,
            company_name=company_name,
            agent=agent_record,
            customer=customer_record,
            avatar='https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&q=80' if role == 'seller' else 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Allow logging in with either username or email
        user = authenticate(username=username, password=password)
        if not user and '@' in username:
            try:
                user_obj = User.objects.get(email__iexact=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if not user:
            raise serializers.ValidationError("Invalid credentials. Please check your username and password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        # Ensure user profile exists
        if not hasattr(user, 'profile'):
            role = 'admin' if user.is_staff or user.is_superuser else 'customer'
            UserProfile.objects.create(user=user, role=role)

        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
