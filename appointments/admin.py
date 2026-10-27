from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'property', 'appointment_date', 'time_slot', 'status']
    list_filter = ['status', 'appointment_date']
    search_fields = ['customer_name', 'customer_email', 'property__title']
