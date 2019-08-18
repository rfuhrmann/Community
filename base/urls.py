from django.urls import path, include
from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout_view'),

]
