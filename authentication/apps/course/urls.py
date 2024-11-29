from django.urls import path
from . import views

urlpatterns = [
    path('course/', views.add_course_view, name='course'),
]
