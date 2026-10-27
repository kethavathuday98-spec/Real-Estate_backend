from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Avg

from .models import Property, PropertyImage
from .serializers import PropertySerializer, PropertyImageSerializer
from .filters import PropertyFilter
from customers.models import Customer
from appointments.models import Appointment

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().select_related('agent').prefetch_related('gallery').order_by('-created_at')
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'location', 'address', 'property_type']
    ordering_fields = ['price', 'created_at', 'area_sqft', 'bedrooms']

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'profile'):
            if user.profile.role == 'customer':
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Customer accounts are view-only. Only Seller or Agent accounts can list properties.")
            if user.profile.agent:
                serializer.save(agent=user.profile.agent)
                return
        serializer.save()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Dashboard statistics endpoint"""
        total_properties = Property.objects.count()
        available = Property.objects.filter(status='available').count()
        sold = Property.objects.filter(status='sold').count()
        rented = Property.objects.filter(status='rented').count()
        total_customers = Customer.objects.count()
        total_appointments = Appointment.objects.count()
        pending_appointments = Appointment.objects.filter(status='pending').count()

        # Sales volume
        total_sales_volume = Property.objects.filter(status='sold').aggregate(total=Sum('price'))['total'] or 0
        avg_property_price = Property.objects.aggregate(avg=Avg('price'))['avg'] or 0

        # Type distribution
        type_distribution = list(
            Property.objects.values('property_type').annotate(count=Count('id')).order_by('-count')
        )

        # Status distribution
        status_distribution = list(
            Property.objects.values('status').annotate(count=Count('id')).order_by('-count')
        )

        return Response({
            'total_properties': total_properties,
            'available_properties': available,
            'sold_properties': sold,
            'rented_properties': rented,
            'total_customers': total_customers,
            'total_appointments': total_appointments,
            'pending_appointments': pending_appointments,
            'total_sales_volume': float(total_sales_volume),
            'avg_property_price': float(avg_property_price),
            'type_distribution': type_distribution,
            'status_distribution': status_distribution,
        })

    @action(detail=True, methods=['post'])
    def add_gallery_image(self, request, pk=None):
        """Add an image to a property gallery"""
        prop = self.get_object()
        image_url = request.data.get('image_url')
        caption = request.data.get('caption', '')
        order = request.data.get('order', prop.gallery.count())
        if not image_url:
            return Response({'error': 'image_url is required'}, status=status.HTTP_400_BAD_REQUEST)
        img = PropertyImage.objects.create(property=prop, image_url=image_url, caption=caption, order=order)
        return Response(PropertyImageSerializer(img).data, status=status.HTTP_201_CREATED)
