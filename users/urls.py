from django.urls import path, include
from . import views

urlpatterns = [
    # path('<str:username>/', views.user_view, name='user_view'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('<str:username>/remove_user/', views.remove_user, name='remove_user'),
    path('profile/<str:username>/accept_friendship/<int:pk>/', views.accept_friendship, name='accept_friendship'),
    path('profile/<str:username>/decline_friendship/<int:pk>/', views.decline_friendship, name='decline_friendship'),
    path('profile/<str:username>/remove_friendship/<int:pk>/', views.remove_friendship, name='remove_friendship'),
]
