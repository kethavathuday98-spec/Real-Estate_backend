from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.CharField(max_length=500, blank=True, help_text="Image URL or relative static path")
    experience_years = models.PositiveIntegerField(default=1)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.8)
    rating_count = models.PositiveIntegerField(default=12)
    agency_name = models.CharField(max_length=200, default="Prime Realty Group")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def active_listings_count(self):
        return self.properties.filter(status='available').count()
