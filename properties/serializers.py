from rest_framework import serializers
from .models import Property, PropertyImage
from agents.serializers import AgentSerializer

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image_url', 'caption', 'order']


class PropertySerializer(serializers.ModelSerializer):
    gallery = PropertyImageSerializer(many=True, read_only=True)
    agent_details = AgentSerializer(source='agent', read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'price', 'property_type',
            'status', 'purpose', 'bedrooms', 'bathrooms', 'area_sqft',
            'location', 'address', 'latitude', 'longitude', 'featured',
            'year_built', 'main_image', 'amenities', 'agent', 'agent_details',
            'gallery', 'created_at', 'updated_at'
        ]
