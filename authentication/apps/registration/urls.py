from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.signaction, name='registration'),
]
