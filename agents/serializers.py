from rest_framework import serializers
from .models import Agent

class AgentSerializer(serializers.ModelSerializer):
    active_listings_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Agent
        fields = [
            'id', 'name', 'email', 'phone', 'bio', 'avatar',
            'experience_years', 'rating', 'rating_count', 'agency_name',
            'active_listings_count', 'created_at'
        ]
