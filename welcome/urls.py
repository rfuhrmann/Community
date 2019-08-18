from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('registration/', views.signup, name='registration'),
]
