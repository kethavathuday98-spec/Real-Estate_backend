from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True)
    avatar = models.CharField(max_length=500, blank=True)
    preferred_location = models.CharField(max_length=200, blank=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    customer_type = models.CharField(
        max_length=20,
        choices=[('buyer', 'Buyer'), ('renter', 'Renter'), ('investor', 'Investor')],
        default='buyer'
    )
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('lead', 'Lead'), ('inactive', 'Inactive')],
        default='active'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
