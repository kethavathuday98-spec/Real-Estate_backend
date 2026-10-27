from django.contrib import admin
from .models import Agent

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'experience_years', 'rating']
    search_fields = ['name', 'email']
