from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Agent
from .serializers import AgentSerializer

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all().order_by('-rating', 'name')
    serializer_class = AgentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'agency_name']
    ordering_fields = ['rating', 'experience_years', 'name']
