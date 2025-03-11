from django.contrib import admin
from django.urls import path, include  # Ensure include is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Ensure api/urls.py exists
    path('internship/', include('internship.urls')),  # Ensure internship/urls.py exists
]
