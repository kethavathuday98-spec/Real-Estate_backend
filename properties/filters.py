import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_bedrooms = django_filters.NumberFilter(field_name="bedrooms", lookup_expr='gte')
    min_area = django_filters.NumberFilter(field_name="area_sqft", lookup_expr='gte')
    location = django_filters.CharFilter(field_name="location", lookup_expr='icontains')
    property_type = django_filters.CharFilter(field_name="property_type", lookup_expr='exact')
    status = django_filters.CharFilter(field_name="status", lookup_expr='exact')
    purpose = django_filters.CharFilter(field_name="purpose", lookup_expr='exact')

    class Meta:
        model = Property
        fields = ['property_type', 'status', 'purpose', 'bedrooms', 'location']
