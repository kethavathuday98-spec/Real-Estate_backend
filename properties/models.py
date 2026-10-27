from django.db import models
from agents.models import Agent

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('villa', 'Luxury Villa'),
        ('apartment', 'Apartment'),
        ('house', 'Single Family House'),
        ('penthouse', 'Penthouse Suite'),
        ('commercial', 'Commercial Space'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('pending', 'Pending Contract'),
    ]

    PURPOSE_CHOICES = [
        ('buy', 'For Sale'),
        ('rent', 'For Rent'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default='villa')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES, default='buy')
    bedrooms = models.PositiveIntegerField(default=3)
    bathrooms = models.PositiveIntegerField(default=2)
    area_sqft = models.PositiveIntegerField(default=1800)
    location = models.CharField(max_length=255, help_text="City or Neighborhood (e.g. Beverly Hills, CA)")
    address = models.CharField(max_length=300, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=34.073620)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=-118.400352)
    featured = models.BooleanField(default=False)
    year_built = models.PositiveIntegerField(default=2022)
    main_image = models.CharField(max_length=500, blank=True)
    amenities = models.JSONField(default=list, blank=True, help_text="List of amenities strings")
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - ${self.price}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='gallery')
    image_url = models.CharField(max_length=500)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.property.title} (#{self.order})"
