from django.http import JsonResponse
from django.urls import path, include


def test_api(request):
    return JsonResponse({"message": "Django is connected to Vue!"})

urlpatterns = [
    path("test/", test_api, name="test-api"),
    path('api/', include('internship.urls')),
]