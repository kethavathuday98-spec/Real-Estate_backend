from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        "status": "online",
        "service": "Prime Real Estate API",
        "endpoints": {
            "properties": "/api/properties/",
            "agents": "/api/agents/",
            "customers": "/api/customers/",
            "appointments": "/api/appointments/",
            "reviews": "/api/reviews/",
            "auth": "/api/auth/",
            "admin": "/admin/"
        }
    })

urlpatterns = [
    path('', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/agents/', include('agents.urls')),
    path('api/customers/', include('customers.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
