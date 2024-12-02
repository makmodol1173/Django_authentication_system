from django.urls import path
from .views import change_password
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
]
