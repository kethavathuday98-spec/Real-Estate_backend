from rest_framework import serializers
from .models import Appointment
from properties.serializers import PropertySerializer
from agents.serializers import AgentSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True)
    property_location = serializers.CharField(source='property.location', read_only=True)
    property_price = serializers.DecimalField(source='property.price', max_digits=14, decimal_places=2, read_only=True)
    property_main_image = serializers.CharField(source='property.main_image', read_only=True)
    agent_name = serializers.CharField(source='agent.name', read_only=True, default='')

    class Meta:
        model = Appointment
        fields = [
            'id', 'property', 'property_title', 'property_location',
            'property_price', 'property_main_image', 'customer', 'agent',
            'agent_name', 'customer_name', 'customer_email', 'customer_phone',
            'appointment_date', 'time_slot', 'status', 'notes', 'created_at'
        ]
