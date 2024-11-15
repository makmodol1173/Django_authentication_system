from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # Add a trailing slash after 'login'
]
