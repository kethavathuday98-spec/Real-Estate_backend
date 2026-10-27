from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, CurrentUserView, DemoLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('me/', CurrentUserView.as_view(), name='auth_me'),
    path('demo-login/', DemoLoginView.as_view(), name='auth_demo_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
