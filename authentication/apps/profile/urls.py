from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]
