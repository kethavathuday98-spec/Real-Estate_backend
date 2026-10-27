from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import UserProfile
from agents.models import Agent
from customers.models import Customer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response({
                'message': 'Account registered successfully.',
                'user': user_data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user_data = UserSerializer(user).data
            return Response({
                'message': 'Logged in successfully.',
                'user': user_data,
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class DemoLoginView(APIView):
    """
    Convenient one-click login for demonstration:
    POST /api/auth/demo-login/ with body: { "role": "seller" | "customer" | "admin" }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        target_role = request.data.get('role', 'customer').lower()
        if target_role not in ['customer', 'seller', 'admin']:
            return Response({'error': 'Invalid role for demo login.'}, status=status.HTTP_400_BAD_REQUEST)

        username = f"demo_{target_role}"
        email = f"{target_role}@primerestates.demo"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': 'Demo',
                'last_name': target_role.capitalize(),
                'is_staff': (target_role == 'admin'),
                'is_superuser': (target_role == 'admin'),
            }
        )

        if created:
            user.set_password('demo1234')
            user.save()

        # Link or update profile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = target_role

        if target_role == 'seller':
            profile.avatar = 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=600&q=80'
            profile.company_name = 'Bespoke Realty International'
            agent = Agent.objects.first()
            if agent:
                profile.agent = agent
        elif target_role == 'customer':
            profile.avatar = 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
            customer = Customer.objects.first()
            if customer:
                profile.customer = customer
        elif target_role == 'admin':
            profile.avatar = 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=300&q=80'

        profile.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'message': f'Signed in as Demo {target_role.capitalize()}',
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
