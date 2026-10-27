from django.db import models
from django.contrib.auth.models import User
from agents.models import Agent
from customers.models import Customer

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer / Buyer'),
        ('seller', 'Seller / Agent'),
        ('admin', 'Administrator'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=50, blank=True)
    avatar = models.CharField(
        max_length=500,
        blank=True,
        default='https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
    )
    company_name = models.CharField(max_length=200, blank=True)
    agent = models.OneToOneField(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_account')
    customer = models.OneToOneField(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_account')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
