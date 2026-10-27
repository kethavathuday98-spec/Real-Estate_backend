from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'property_type', 'status', 'purpose', 'location', 'bedrooms']
    list_filter = ['property_type', 'status', 'purpose', 'location']
    search_fields = ['title', 'location', 'address']
    inlines = [PropertyImageInline]

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'image_url', 'order']
