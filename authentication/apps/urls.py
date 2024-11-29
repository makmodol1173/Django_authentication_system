from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include('apps.login.urls')),
    path("", include('apps.registration.urls')),
    path("", include('apps.profile.urls')),
]
    