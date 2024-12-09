from django.urls import path
from .views import change_password
from .views import upload_picture
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('upload_picture/', views.upload_picture, name='upload_picture'),
]
